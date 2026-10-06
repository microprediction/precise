"""Every tracked path must be checkable-out on Windows.

Twelve legacy research scripts once had URL query strings for names
(``stocks?topic=...&k=int:3.py``). Git on Windows refuses to check such a path out, so the
repository could not be cloned there and the weekly ``install-smoke`` job failed on its Windows
runner at the checkout step. This test fails if a path Windows rejects is tracked again.

Rules (per path component): none of ``<>:"|?*\\`` or ASCII control characters; no trailing dot or
space; not a reserved DOS device name (``CON``, ``NUL``, ``COM1`` ... with or without an extension).
"""

import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent

ILLEGAL_CHARS = re.compile(r'[<>:"|?*\\\x00-\x1f]')
RESERVED = re.compile(r"^(CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9])(\..*)?$", re.IGNORECASE)


def windows_problems(path: str) -> list[str]:
    """Return the reasons, if any, that Windows would reject ``path`` (a ``/``-separated path)."""
    problems = []
    for part in path.split("/"):
        bad = sorted(set(ILLEGAL_CHARS.findall(part)))
        if bad:
            problems.append(f"{part!r} contains {bad}")
        if part.endswith((".", " ")):
            problems.append(f"{part!r} ends with a dot or space")
        if RESERVED.match(part):
            problems.append(f"{part!r} is a reserved Windows device name")
    return problems


def tracked_paths() -> list[str]:
    if shutil.which("git") is None:
        pytest.skip("git is not installed")
    try:
        out = subprocess.run(
            ["git", "-c", "core.quotepath=off", "ls-files", "-z"],
            cwd=REPO,
            capture_output=True,
            check=True,
        ).stdout
    except subprocess.CalledProcessError:
        pytest.skip("not running from a git checkout")
    return [p for p in out.decode("utf-8", errors="replace").split("\0") if p]


def test_tracked_paths_are_windows_safe():
    offenders = {p: windows_problems(p) for p in tracked_paths()}
    offenders = {p: why for p, why in offenders.items() if why}
    assert not offenders, "paths Windows cannot check out:\n" + "\n".join(
        f"  {p}: {'; '.join(why)}" for p, why in offenders.items()
    )


@pytest.mark.parametrize(
    "path",
    [
        "a/stocks?topic=stocks.py",
        "a/n_dim=int:3.py",
        'a/"quoted".txt',
        "a/b|c",
        "a/star*.py",
        "a/trailing.",
        "a/trailing /b",
        "a/CON",
        "a/nul.txt",
        "a/back\\slash",
    ],
)
def test_checker_rejects(path):
    assert windows_problems(path)


@pytest.mark.parametrize("path", ["precise/ewa.py", "a/b c/d.e.f", "a/CONSOLE.py", "a/.github"])
def test_checker_accepts(path):
    assert not windows_problems(path)
