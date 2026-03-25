"""Utility functions for Morpheus."""

from __future__ import annotations

import re


def parse_code_block(text: str) -> str:
    """Extract code from markdown code blocks."""
    pattern = r"```(?:\w+)?\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches[0].strip() if matches else text.strip()


def extract_functions(code: str) -> list[str]:
    """Extract function names from Python code."""
    pattern = r"^def\s+(\w+)\s*\("
    return re.findall(pattern, code, re.MULTILINE)


def validate_python(code: str) -> tuple[bool, str]:
    """Check if code is valid Python by attempting to compile it."""
    try:
        compile(code, "<string>", "exec")
        return True, "Valid Python"
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"


def format_diff(before: str, after: str) -> str:
    """Generate a simple diff between two strings."""
    before_lines = before.splitlines()
    after_lines = after.splitlines()
    diff_lines: list[str] = []
    for i, (b, a) in enumerate(zip(before_lines, after_lines)):
        if b != a:
            diff_lines.append(f"L{i + 1}: - {b}")
            diff_lines.append(f"L{i + 1}: + {a}")
    return "\n".join(diff_lines) if diff_lines else "No differences"
