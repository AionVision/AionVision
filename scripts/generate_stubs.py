#!/usr/bin/env python3
"""
Stub generator for the Aionvision SDK documentation repository.

Reads SDK source files using the `ast` module and produces stub files that
contain only the public API surface: class definitions, method signatures
(with full type annotations, defaults, and decorators), docstrings, and
dataclass field definitions.  All method/function bodies are replaced with
``...`` (Ellipsis).

Usage:
    python scripts/generate_stubs.py

Re-run whenever the SDK source changes to keep stubs in sync.
"""

from __future__ import annotations

import ast
import os
import sys
import textwrap
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Resolve paths relative to this script's location
_SCRIPT_DIR = Path(__file__).resolve().parent
_DOCS_ROOT_DIR = _SCRIPT_DIR.parent

# Update these paths to point to your local SDK source checkout
SDK_ROOT = Path(os.environ.get(
    "AION_SDK_SOURCE",
    str(_DOCS_ROOT_DIR.parent / "app" / "sdk" / "python" / "aion"),
))
DOCS_ROOT = _DOCS_ROOT_DIR / "sdk" / "python" / "aion"

# Files to stub (relative to SDK_ROOT)
CLIENT_FILES = [
    "client.py",
    "sync.py",
    "config.py",
    "exceptions.py",
    "pipeline.py",
]

# Resource files to stub (relative to SDK_ROOT/resources/)
RESOURCE_EXCLUDES = {"_file_utils.py", "__pycache__"}

# Type files to copy nearly as-is (relative to SDK_ROOT/types/)
TYPE_EXCLUDES = {"serialization.py", "file_resolver.py", "__pycache__"}

# Internal modules to skip entirely
INTERNAL_PREFIXES = ("_",)

# Excluded type modules whose imports should be stripped from stubs
EXCLUDED_TYPE_MODULES = {"serialization", "file_resolver"}


# ---------------------------------------------------------------------------
# AST Helpers
# ---------------------------------------------------------------------------

def _get_source_segment(source_lines: list[str], node: ast.AST) -> str:
    """Get the original source text for an AST node."""
    start = node.lineno - 1
    end = node.end_lineno
    lines = source_lines[start:end]
    if lines:
        # De-indent based on col_offset
        col = node.col_offset
        lines = [line[col:] if len(line) > col else line for line in lines]
    return "\n".join(lines)


def _unparse_node(node: ast.AST) -> str:
    """Unparse an AST node back to source code."""
    return ast.unparse(node)


def _get_docstring(node: ast.AST) -> str | None:
    """Extract docstring from a class or function node."""
    if (
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and node.body
        and isinstance(node.body[0], ast.Expr)
        and isinstance(node.body[0].value, (ast.Constant,))
        and isinstance(node.body[0].value.value, str)
    ):
        return node.body[0].value.value
    return None


def _format_docstring(docstring: str, indent: str) -> str:
    """Format a docstring with proper indentation."""
    lines = docstring.split("\n")
    if len(lines) == 1:
        return f'{indent}"""{docstring}"""'

    result = [f'{indent}"""']
    for line in lines:
        if line.strip():
            result.append(f"{indent}{line.rstrip()}")
        else:
            result.append("")
    # Ensure closing quotes are on their own line
    if result[-1].strip():
        result.append(f'{indent}"""')
    else:
        result[-1] = f'{indent}"""'
    return "\n".join(result)


def _format_decorator(dec: ast.AST) -> str:
    """Format a decorator node back to source."""
    return f"@{_unparse_node(dec)}"


def _format_arguments(args: ast.arguments) -> str:
    """Format function arguments back to source."""
    parts: list[str] = []

    # posonlyargs
    posonlyargs = args.posonlyargs or []
    # regular args
    regular_args = args.args or []
    # defaults are right-aligned to args
    defaults = args.defaults or []
    # kwonlyargs
    kwonlyargs = args.kwonlyargs or []
    kw_defaults = args.kw_defaults or []

    num_no_default = len(regular_args) - len(defaults)

    # Positional-only args
    for i, arg in enumerate(posonlyargs):
        s = arg.arg
        if arg.annotation:
            s += f": {_unparse_node(arg.annotation)}"
        parts.append(s)

    if posonlyargs:
        parts.append("/")

    # Regular args
    for i, arg in enumerate(regular_args):
        s = arg.arg
        if arg.annotation:
            s += f": {_unparse_node(arg.annotation)}"
        default_idx = i - num_no_default
        if default_idx >= 0 and default_idx < len(defaults):
            s += f" = {_unparse_node(defaults[default_idx])}"
        parts.append(s)

    # *args or bare *
    if args.vararg:
        s = f"*{args.vararg.arg}"
        if args.vararg.annotation:
            s += f": {_unparse_node(args.vararg.annotation)}"
        parts.append(s)
    elif kwonlyargs:
        parts.append("*")

    # Keyword-only args
    for i, arg in enumerate(kwonlyargs):
        s = arg.arg
        if arg.annotation:
            s += f": {_unparse_node(arg.annotation)}"
        if i < len(kw_defaults) and kw_defaults[i] is not None:
            s += f" = {_unparse_node(kw_defaults[i])}"
        parts.append(s)

    # **kwargs
    if args.kwarg:
        s = f"**{args.kwarg.arg}"
        if args.kwarg.annotation:
            s += f": {_unparse_node(args.kwarg.annotation)}"
        parts.append(s)

    return ", ".join(parts)


def _stub_function(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    indent: str = "",
    source_lines: list[str] | None = None,
) -> str:
    """Generate stub for a function/method."""
    parts: list[str] = []

    # Decorators
    for dec in node.decorator_list:
        parts.append(f"{indent}{_format_decorator(dec)}")

    # Function signature
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    args_str = _format_arguments(node.args)
    returns = f" -> {_unparse_node(node.returns)}" if node.returns else ""
    sig = f"{indent}{prefix} {node.name}({args_str}){returns}:"
    parts.append(sig)

    # Docstring
    docstring = _get_docstring(node)
    if docstring:
        parts.append(_format_docstring(docstring, indent + "    "))

    # Body is just ...
    parts.append(f"{indent}    ...")

    return "\n".join(parts)


def _stub_class(
    node: ast.ClassDef,
    indent: str = "",
    source_lines: list[str] | None = None,
) -> str:
    """Generate stub for a class."""
    parts: list[str] = []

    # Decorators
    for dec in node.decorator_list:
        parts.append(f"{indent}{_format_decorator(dec)}")

    # Class definition
    bases = ", ".join(_unparse_node(b) for b in node.bases)
    keywords = ", ".join(
        f"{kw.arg}={_unparse_node(kw.value)}" for kw in node.keywords
    )
    all_bases = ", ".join(filter(None, [bases, keywords]))
    if all_bases:
        parts.append(f"{indent}class {node.name}({all_bases}):")
    else:
        parts.append(f"{indent}class {node.name}:")

    # Class docstring
    docstring = _get_docstring(node)
    if docstring:
        parts.append(_format_docstring(docstring, indent + "    "))

    inner_indent = indent + "    "
    has_body = bool(docstring)

    for item in node.body:
        # Skip the docstring node (already handled)
        if (
            isinstance(item, ast.Expr)
            and isinstance(item.value, ast.Constant)
            and isinstance(item.value.value, str)
            and item.value.value == docstring
        ):
            continue

        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Skip private methods (keep dunder methods like __init__, __aenter__, etc.)
            if item.name.startswith("_") and not item.name.startswith("__"):
                continue
            parts.append("")
            parts.append(_stub_function(item, inner_indent, source_lines))
            has_body = True

        elif isinstance(item, ast.ClassDef):
            parts.append("")
            parts.append(_stub_class(item, inner_indent, source_lines))
            has_body = True

        elif isinstance(item, ast.AnnAssign):
            # Type-annotated class variable (e.g., in dataclasses)
            parts.append(f"{inner_indent}{_unparse_node(item)}")
            has_body = True

        elif isinstance(item, ast.Assign):
            # Class variable assignment
            parts.append(f"{inner_indent}{_unparse_node(item)}")
            has_body = True

        elif isinstance(item, ast.ImportFrom):
            # In-class imports (e.g., AionVision imports exceptions as class attrs)
            parts.append(f"{inner_indent}{_unparse_node(item)}")
            has_body = True

    if not has_body:
        parts.append(f"{inner_indent}...")

    return "\n".join(parts)


def _is_type_alias(node: ast.AST) -> bool:
    """Check if an assignment is a type alias."""
    if isinstance(node, ast.Assign):
        # e.g., MyType = Union[str, int]
        if isinstance(node.value, (ast.Subscript, ast.Name, ast.Attribute)):
            return True
    if isinstance(node, ast.AnnAssign):
        return True
    return False


# ---------------------------------------------------------------------------
# Stub Generation
# ---------------------------------------------------------------------------

def generate_stub(source_path: Path, is_type_file: bool = False) -> str:
    """
    Generate a stub from a Python source file.

    For type files (dataclass definitions), we preserve more of the
    original structure since they are mostly type definitions anyway.
    """
    source = source_path.read_text()
    tree = ast.parse(source)
    source_lines = source.split("\n")
    parts: list[str] = []

    # Module docstring
    docstring = _get_docstring(tree)
    if docstring:
        parts.append(f'"""{docstring}"""')
        parts.append("")

    # Collect all top-level nodes
    for node in ast.iter_child_nodes(tree):
        # Skip module docstring (already handled)
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
            and node.value.value == docstring
        ):
            continue

        if isinstance(node, (ast.Import, ast.ImportFrom)):
            import_str = _unparse_node(node)
            # Skip internal imports (e.g., from ._http import ...)
            if isinstance(node, ast.ImportFrom) and node.module:
                module = node.module
                # For relative imports (level > 0), node.module won't have the dot
                # e.g., `from ._http import X` -> module="_http", level=1
                if module.startswith("_") and node.level and node.level > 0:
                    continue
                # For absolute internal imports
                if "._" in module:
                    continue
                # Skip imports from excluded type modules
                if node.level and node.level > 0 and module in EXCLUDED_TYPE_MODULES:
                    continue
            parts.append(import_str)

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Top-level functions
            parts.append("")
            parts.append(_stub_function(node, "", source_lines))

        elif isinstance(node, ast.ClassDef):
            parts.append("")
            parts.append("")
            parts.append(_stub_class(node, "", source_lines))

        elif isinstance(node, ast.Assign):
            # Top-level assignments (constants, type aliases)
            # Keep things like ENV_API_KEY = "AIONVISION_API_KEY"
            parts.append(_unparse_node(node))

        elif isinstance(node, ast.AnnAssign):
            # Top-level annotated assignments
            parts.append(_unparse_node(node))

        elif isinstance(node, ast.If):
            # Handle TYPE_CHECKING blocks
            if (
                isinstance(node.test, ast.Name)
                and node.test.id == "TYPE_CHECKING"
            ):
                parts.append("")
                parts.append("if TYPE_CHECKING:")
                for child in node.body:
                    parts.append(f"    {_unparse_node(child)}")

    # Ensure file ends with newline
    result = "\n".join(parts).rstrip() + "\n"

    # Clean up multiple blank lines
    while "\n\n\n\n" in result:
        result = result.replace("\n\n\n\n", "\n\n\n")

    return result


def generate_init_stub(source_path: Path) -> str:
    """
    Generate a stub for __init__.py files.

    These are mostly re-exports, so we keep them largely intact.
    """
    source = source_path.read_text()
    tree = ast.parse(source)
    parts: list[str] = []

    docstring = _get_docstring(tree)
    if docstring:
        parts.append(f'"""{docstring}"""')
        parts.append("")

    for node in ast.iter_child_nodes(tree):
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
            and node.value.value == docstring
        ):
            continue

        if isinstance(node, (ast.Import, ast.ImportFrom)):
            import_str = _unparse_node(node)
            # Skip internal imports
            if isinstance(node, ast.ImportFrom) and node.module:
                module = node.module
                if module.startswith("_") and node.level and node.level > 0:
                    continue
                if "._" in module:
                    continue
                # Skip imports from excluded type modules
                if node.level and node.level > 0 and module in EXCLUDED_TYPE_MODULES:
                    continue
            parts.append(import_str)

        elif isinstance(node, ast.Assign):
            # __all__ and other assignments
            parts.append("")
            parts.append(_unparse_node(node))

    result = "\n".join(parts).rstrip() + "\n"
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def stub_file(src: Path, dst: Path, is_type_file: bool = False) -> None:
    """Generate a stub from src and write to dst."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.name == "__init__.py":
        content = generate_init_stub(src)
    else:
        content = generate_stub(src, is_type_file=is_type_file)
    dst.write_text(content)
    print(f"  {dst.relative_to(DOCS_ROOT.parent.parent.parent)}")


def main() -> None:
    print("Generating SDK stubs...")
    print(f"  Source: {SDK_ROOT}")
    print(f"  Output: {DOCS_ROOT}")
    print()

    # --- Client files ---
    print("Client files:")
    for name in CLIENT_FILES:
        src = SDK_ROOT / name
        dst = DOCS_ROOT / name
        if src.exists():
            stub_file(src, dst)
        else:
            print(f"  SKIP (not found): {name}")

    # --- __init__.py for main package ---
    print("\nPackage __init__.py:")
    src = SDK_ROOT / "__init__.py"
    dst = DOCS_ROOT / "__init__.py"
    if src.exists():
        stub_file(src, dst)

    # --- Resources ---
    print("\nResource files:")
    resources_src = SDK_ROOT / "resources"
    resources_dst = DOCS_ROOT / "resources"

    # resources __init__.py
    src = resources_src / "__init__.py"
    dst = resources_dst / "__init__.py"
    if src.exists():
        stub_file(src, dst)

    for src_file in sorted(resources_src.glob("*.py")):
        if src_file.name in RESOURCE_EXCLUDES:
            continue
        if src_file.name == "__init__.py":
            continue
        if src_file.name.startswith("_"):
            continue
        dst_file = resources_dst / src_file.name
        stub_file(src_file, dst_file)

    # --- Types ---
    print("\nType files:")
    types_src = SDK_ROOT / "types"
    types_dst = DOCS_ROOT / "types"

    # types __init__.py
    src = types_src / "__init__.py"
    dst = types_dst / "__init__.py"
    if src.exists():
        stub_file(src, dst)

    for src_file in sorted(types_src.glob("*.py")):
        if src_file.name in TYPE_EXCLUDES:
            continue
        if src_file.name == "__init__.py":
            continue
        if src_file.name.startswith("_"):
            continue
        dst_file = types_dst / src_file.name
        stub_file(src_file, dst_file, is_type_file=True)

    print("\nDone!")


if __name__ == "__main__":
    main()
