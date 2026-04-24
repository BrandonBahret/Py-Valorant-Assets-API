from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "valorant_assets_api"
DOCS_DIR = ROOT / "docs" / "reference"
INIT_PATH = PACKAGE_DIR / "__init__.py"
CLIENT_PATH = PACKAGE_DIR / "client.py"
MODELS_PATH = PACKAGE_DIR / "models.py"
ENUMS_PATH = PACKAGE_DIR / "enums.py"

GENERATED_HEADER = "> Generated file. Do not edit by hand. Run `python scripts/generate_reference_docs.py`."


@dataclass(frozen=True)
class MethodDoc:
    name: str
    signature: str
    returns: str | None
    summary: str


@dataclass(frozen=True)
class FieldDoc:
    name: str
    annotation: str
    alias: str | None


@dataclass(frozen=True)
class ModelDoc:
    name: str
    fields: list[FieldDoc]


@dataclass(frozen=True)
class EnumValueDoc:
    name: str
    value: str


@dataclass(frozen=True)
class EnumDoc:
    name: str
    values: list[EnumValueDoc]


def parse_module(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def literal_eval(node: ast.AST) -> object:
    return ast.literal_eval(node)


def parse_exports() -> list[str]:
    module = parse_module(INIT_PATH)
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    return list(literal_eval(node.value))
    raise ValueError("Could not find __all__ in valorant_assets_api.__init__")


def format_signature(function: ast.FunctionDef) -> str:
    args = function.args
    parts: list[str] = []
    positional = list(args.posonlyargs) + list(args.args)
    defaults = [None] * (len(positional) - len(args.defaults)) + list(args.defaults)
    for arg, default in zip(positional, defaults):
        parts.append(format_arg(arg, default))
    if args.vararg:
        parts.append(format_vararg(args.vararg))
    if args.kwonlyargs:
        if not args.vararg:
            parts.append("*")
        for arg, default in zip(args.kwonlyargs, args.kw_defaults):
            parts.append(format_arg(arg, default))
    if args.kwarg:
        parts.append(format_kwarg(args.kwarg))
    return f"({', '.join(parts)})"


def format_arg(arg: ast.arg, default: ast.expr | None) -> str:
    text = arg.arg
    if arg.annotation is not None:
        text += f": {ast.unparse(arg.annotation)}"
    if default is not None:
        text += f" = {ast.unparse(default)}"
    return text


def format_vararg(arg: ast.arg) -> str:
    text = f"*{arg.arg}"
    if arg.annotation is not None:
        text += f": {ast.unparse(arg.annotation)}"
    return text


def format_kwarg(arg: ast.arg) -> str:
    text = f"**{arg.arg}"
    if arg.annotation is not None:
        text += f": {ast.unparse(arg.annotation)}"
    return text


def fallback_summary(method_name: str) -> str:
    special = {
        "get_active_events": "Return the events active at the provided time.",
        "get_current_season": "Return the season active at the provided time.",
        "get_session": "Create a configured HTTP session with default wrapper headers.",
        "get_version": "Fetch the current Valorant version metadata.",
        "list_contract_rewards": "Flatten and return the rewards across all chapters in a contract.",
    }
    if method_name in special:
        return special[method_name]

    if method_name.startswith("list_"):
        resource = humanize_name(method_name.removeprefix("list_"))
        return f"List {resource}."
    if method_name.startswith("get_"):
        resource = humanize_name(method_name.removeprefix("get_"))
        return f"Fetch {indefinite_article(singularize(resource))} {singularize(resource)} by UUID."
    if method_name.startswith("find_"):
        resource = humanize_name(method_name.removeprefix("find_"))
        return f"Find {indefinite_article(singularize(resource))} {singularize(resource)} by display name."
    return f"Call `{method_name}` on the client."


def humanize_name(name: str) -> str:
    return name.replace("_", " ")


def singularize(text: str) -> str:
    words = text.split()
    if not words:
        return text
    last = words[-1]
    if last.endswith("ies"):
        words[-1] = last[:-3] + "y"
    elif last.endswith("s") and not last.endswith("ss"):
        words[-1] = last[:-1]
    return " ".join(words)


def indefinite_article(text: str) -> str:
    if not text:
        return "a"
    return "an" if text[0].lower() in {"a", "e", "i", "o", "u"} else "a"


def parse_client_methods() -> list[MethodDoc]:
    module = parse_module(CLIENT_PATH)
    client_class = next(
        node for node in module.body if isinstance(node, ast.ClassDef) and node.name == "ValorantAPI"
    )
    methods: list[MethodDoc] = []
    for node in client_class.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if node.name.startswith("_") or node.name == "__init__":
            continue
        returns = ast.unparse(node.returns) if node.returns is not None else None
        methods.append(
            MethodDoc(
                name=node.name,
                signature=format_signature(node),
                returns=returns,
                summary=fallback_summary(node.name),
            )
        )
    return methods


def parse_alias(annotation: ast.expr | None) -> str | None:
    if not isinstance(annotation, ast.Subscript):
        return None
    if not isinstance(annotation.value, ast.Name) or annotation.value.id != "Annotated":
        return None
    slice_value = annotation.slice
    values = []
    if isinstance(slice_value, ast.Tuple):
        values = list(slice_value.elts)
    else:
        values = [slice_value]
    for extra in values[1:]:
        if (
            isinstance(extra, ast.Call)
            and isinstance(extra.func, ast.Name)
            and extra.func.id == "Alias"
            and extra.args
            and isinstance(extra.args[0], ast.Constant)
            and isinstance(extra.args[0].value, str)
        ):
            return extra.args[0].value
    return None


def strip_annotated(annotation: ast.expr | None) -> str:
    if annotation is None:
        return "Any"
    if not isinstance(annotation, ast.Subscript):
        return ast.unparse(annotation)
    if not isinstance(annotation.value, ast.Name) or annotation.value.id != "Annotated":
        return ast.unparse(annotation)
    slice_value = annotation.slice
    if isinstance(slice_value, ast.Tuple) and slice_value.elts:
        return ast.unparse(slice_value.elts[0])
    return ast.unparse(annotation)


def parse_models(export_names: set[str]) -> list[ModelDoc]:
    module = parse_module(MODELS_PATH)
    models: list[ModelDoc] = []
    for node in module.body:
        if not isinstance(node, ast.ClassDef) or node.name not in export_names:
            continue
        fields: list[FieldDoc] = []
        for statement in node.body:
            if isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
                fields.append(
                    FieldDoc(
                        name=statement.target.id,
                        annotation=strip_annotated(statement.annotation),
                        alias=parse_alias(statement.annotation),
                    )
                )
        models.append(ModelDoc(name=node.name, fields=fields))
    return models


def parse_enums(export_names: set[str]) -> list[EnumDoc]:
    module = parse_module(ENUMS_PATH)
    enums: list[EnumDoc] = []
    for node in module.body:
        if not isinstance(node, ast.ClassDef) or node.name not in export_names:
            continue
        values: list[EnumValueDoc] = []
        for statement in node.body:
            if (
                isinstance(statement, ast.Assign)
                and len(statement.targets) == 1
                and isinstance(statement.targets[0], ast.Name)
                and isinstance(statement.value, ast.Constant)
                and isinstance(statement.value.value, str)
            ):
                values.append(EnumValueDoc(name=statement.targets[0].id, value=statement.value.value))
        enums.append(EnumDoc(name=node.name, values=values))
    return enums


def render_client(methods: list[MethodDoc]) -> str:
    lines = [
        "# Client Reference",
        "",
        GENERATED_HEADER,
        "",
        "Use this page for quick API lookup. Start with the narrative guides if you are new to the wrapper.",
        "",
    ]
    for method in methods:
        lines.extend(
            [
                f"## `{method.name}`",
                "",
                f"**Signature:** `{method.name}{method.signature}`",
                "",
                f"**Returns:** `{method.returns or 'Any'}`",
                "",
                method.summary,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def render_models(models: list[ModelDoc]) -> str:
    lines = [
        "# Model Reference",
        "",
        GENERATED_HEADER,
        "",
        "Exported models are listed here for quick field lookup. Many nested helper models exist in source even when they are not re-exported at the package root.",
        "",
    ]
    for model in models:
        lines.extend([f"## `{model.name}`", ""])
        if not model.fields:
            lines.extend(["No public fields discovered.", ""])
            continue
        lines.extend(["| Field | Type | API Alias |", "| --- | --- | --- |"])
        for field in model.fields:
            alias = f"`{field.alias}`" if field.alias else "-"
            lines.append(f"| `{field.name}` | `{field.annotation}` | {alias} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_enums(enums: list[EnumDoc]) -> str:
    lines = [
        "# Enum Reference",
        "",
        GENERATED_HEADER,
        "",
        "Exported enums define the string values used by typed fields throughout the wrapper.",
        "",
    ]
    for enum in enums:
        lines.extend([f"## `{enum.name}`", ""])
        for value in enum.values:
            lines.append(f"- `{value.name}` = `{value.value}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    exports = parse_exports()
    export_names = set(exports)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "client.md").write_text(render_client(parse_client_methods()), encoding="utf-8")
    (DOCS_DIR / "models.md").write_text(render_models(parse_models(export_names)), encoding="utf-8")
    (DOCS_DIR / "enums.md").write_text(render_enums(parse_enums(export_names)), encoding="utf-8")


if __name__ == "__main__":
    main()
