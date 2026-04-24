from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
import hashlib
import math
import shutil
import types
from pathlib import Path
from typing import TYPE_CHECKING
import typing
from urllib.parse import unquote, urlparse

import pypercache.models.apimodel as _apimodel_module
from pypercache.models.validation import _matches_type
from pypercache.utils import typing_cast as _typing_cast
from pypercache.utils.sentinel import UNSET


if TYPE_CHECKING:
    from .client import ValorantAPI


_ASSET_CONTEXT: ContextVar[dict[str, object] | None] = ContextVar("valorant_asset_context", default=None)


@contextmanager
def asset_context(*, api: ValorantAPI, endpoint_path: str):
    token = _ASSET_CONTEXT.set({"api": api, "endpoint_path": endpoint_path})
    try:
        yield
    finally:
        _ASSET_CONTEXT.reset(token)


def get_asset_context() -> dict[str, object] | None:
    return _ASSET_CONTEXT.get()


class CachedMediaAsset(str):
    """String-like media URL with on-demand disk fetch support."""

    def __new__(
        cls,
        url: str,
        *,
        api: ValorantAPI | None = None,
        relative_directory: Path | None = None,
        field_name: str | None = None,
    ) -> CachedMediaAsset:
        obj = super().__new__(cls, url)
        obj._api = api
        obj._relative_directory = relative_directory
        obj._field_name = field_name
        obj._filepath = None
        return obj

    @property
    def url(self) -> str:
        return str(self)

    def __repr__(self) -> str:
        return f"CachedMediaAsset(url={str.__repr__(self)})"

    @property
    def filepath(self) -> Path | None:
        if self._filepath is not None:
            return self._filepath
        if self._api is None:
            return None
        return MediaAssetStore(self._api).cached_path(self.url)

    def cache_to_disk(self) -> CachedMediaAsset:
        self._filepath = MediaAssetStore.require(self._api).fetch(
            self.url,
            relative_directory=self._relative_directory,
            field_name=self._field_name,
        )
        return self

    def fetch_from_disk(self) -> Path:
        return self.cache_to_disk().filepath  # type: ignore[return-value]


class MediaAssetStore:
    def __init__(self, api: ValorantAPI) -> None:
        self._api = api

    @classmethod
    def require(cls, api: ValorantAPI | None) -> MediaAssetStore:
        if api is None:
            raise ValueError("media asset is not attached to an API client")
        return cls(api)

    def wrap(self, url: str, *, relative_directory: Path, field_name: str | None = None) -> CachedMediaAsset:
        return CachedMediaAsset(
            url,
            api=self._api,
            relative_directory=relative_directory,
            field_name=field_name,
        )

    def fetch(self, media_uri: str, *, relative_directory: Path, field_name: str | None = None) -> Path:
        download_directory = self._api.download_directory
        if download_directory is None:
            raise ValueError("download_directory must be configured to fetch media assets")
        if relative_directory is None:
            raise ValueError("media asset is missing its relative directory context")

        target_path = download_directory / relative_directory / self._generated_filename(media_uri, field_name)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        cached_path = self.cached_path(media_uri)
        if cached_path is not None and cached_path.exists():
            if cached_path != target_path:
                target_path = self._relocate(cached_path, target_path)
            self._store_cached_path(media_uri, target_path)
            return target_path

        if target_path.exists():
            self._store_cached_path(media_uri, target_path)
            return target_path

        content = self._api.request("GET", media_uri, expected="bytes", use_cache=False)
        target_path.write_bytes(content)
        self._store_cached_path(media_uri, target_path)
        return target_path

    def cached_path(self, media_uri: str) -> Path | None:
        cache = self._api.cache
        cache_key = self._cache_key(media_uri)
        if cache is None or not cache.has(cache_key):
            return None
        raw_path = cache.get(cache_key).data.get("path")
        if not raw_path:
            return None
        return Path(raw_path)

    def _store_cached_path(self, media_uri: str, path: Path) -> None:
        if self._api.cache is None:
            return
        self._api.cache.store(
            self._cache_key(media_uri),
            {"path": str(path)},
            expiry=math.inf,
        )

    @staticmethod
    def _cache_key(media_uri: str) -> str:
        digest = hashlib.sha256(media_uri.encode("utf-8")).hexdigest()
        return f"media:{digest}"

    @staticmethod
    def _generated_filename(media_uri: str, field_name: str | None) -> str:
        parsed = urlparse(media_uri)
        original_name = Path(unquote(parsed.path)).name
        if not original_name:
            original_name = field_name or "asset"
        suffix = hashlib.sha256(media_uri.encode("utf-8")).hexdigest()[:12]
        stem = Path(original_name).stem or field_name or "asset"
        extension = Path(original_name).suffix
        return f"{stem}-{suffix}{extension}"

    @staticmethod
    def _relocate(source: Path, destination: Path) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.move(str(source), str(destination))
        except PermissionError:
            shutil.copy2(source, destination)
            try:
                source.unlink()
            except PermissionError:
                pass
        return destination


_ORIGINAL_INSTANTIATE_TYPE = _typing_cast.instantiate_type


def _asset_aware_instantiate_type(target_type: type[object], data: object) -> object:
    if data is UNSET or data is None:
        return data

    origin = typing.get_origin(target_type)
    args = typing.get_args(target_type)

    if origin is typing.Annotated:
        return _asset_aware_instantiate_type(args[0], data)

    union_type = getattr(types, "UnionType", None)
    if origin is typing.Union or (union_type is not None and origin is union_type):
        for arg in args:
            if arg is type(None):
                continue
            value = _asset_aware_instantiate_type(arg, data)
            if _matches_type(arg, value):
                return value
        return data

    return _ORIGINAL_INSTANTIATE_TYPE(target_type, data)


_typing_cast.instantiate_type = _asset_aware_instantiate_type
_apimodel_module.instantiate_type = _asset_aware_instantiate_type
