"""Run with https://docs.astral.sh/uv/guides/scripts:

.. code-block:: shell
    uv run --no-project .github/workflows/main.py
"""
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "pyyaml",
# ]
# ///

import json
import subprocess
from pathlib import Path

import yaml


REPO_DIR = Path(__file__).parent.parent.parent.absolute()


def main() -> int:
    tags = set(get_existing_tags())
    versions = set(get_prettier_versions())
    expected_tags = {f"v{t}" for t in versions}
    missing_tags = expected_tags - tags
    if not missing_tags:
        print("No new versions found")
        return 0
    for tag in sorted(missing_tags):
        print(f"Updating to {tag}")
        version = _to_version(tag)
        update_files(version)
        stage_commit_and_tag(tag)
    return 0


def _to_version(tag: str) -> str:
    return tag[1:]


def get_existing_tags() -> list[str]:
    tags = git("tag", "--list").splitlines()
    return sorted(t for t in tags if t.startswith("v"))


def get_prettier_versions() -> list[str]:
    prettier_versions = _get_node_package_versions("prettier")
    prettier_versions = [
        v for v in prettier_versions if "alpha" not in v if "beta" not in v
    ]
    return sorted(prettier_versions)


def _get_node_package_versions(package_name: str) -> list[str]:
    cmd = ("npm", "view", package_name, "--json")
    output = json.loads(subprocess.check_output(cmd))
    return output["versions"]


def update_files(new_version: str) -> None:
    _replace_in_pre_commit_hooks(new_version)
    _replace_in_readme(new_version)
    _update_version_file(new_version)


def _replace_in_pre_commit_hooks(new_version: str) -> None:
    with open(REPO_DIR / ".pre-commit-hooks.yaml") as stream:
        pre_commit_hooks = yaml.safe_load(stream)
    pre_commit_hooks[0]["additional_dependencies"] = [f"prettier@{new_version}"]
    with open(REPO_DIR / ".pre-commit-hooks.yaml", "w") as stream:
        yaml.dump(pre_commit_hooks, stream, sort_keys=False)


def _replace_in_readme(new_version: str) -> None:
    with open(REPO_DIR / "README.md") as f:
        readme = f.read()
    current_version = __get_current_version()
    new_readme = readme.replace(current_version, new_version)
    with open(REPO_DIR / "README.md", "w") as f:
        f.write(new_readme)


def __get_current_version() -> str:
    with open(REPO_DIR / ".version") as stream:
        return stream.readline().strip()


def _update_version_file(new_version: str) -> None:
    with open(REPO_DIR / ".version", "w") as stream:
        stream.write(new_version + "\n")


def stage_commit_and_tag(tag: str) -> None:
    git("add", ".pre-commit-hooks.yaml", ".version", "README.md")
    git("commit", "-m", f"MAINT: upgrade to Prettier {tag}")
    git("tag", tag)


def git(*cmd: str) -> str:
    output = subprocess.check_output(("git", "-C", REPO_DIR) + cmd)
    return output.decode()


if __name__ == "__main__":
    raise SystemExit(main())
