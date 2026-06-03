import pytest
from clauder.github import _filter_paths, _detect_language


def test_filter_paths_skips_node_modules():
    paths = [
        "src/index.ts",
        "node_modules/lodash/index.js",
        "package.json",
        "dist/bundle.js",
        "README.md",
    ]
    result = _filter_paths(paths, max_files=10)
    assert "node_modules/lodash/index.js" not in result
    assert "dist/bundle.js" not in result
    assert "src/index.ts" in result
    assert "package.json" in result


def test_filter_paths_skips_binaries():
    paths = ["logo.png", "font.woff2", "main.py", "data.zip"]
    result = _filter_paths(paths, max_files=10)
    assert "logo.png" not in result
    assert "font.woff2" not in result
    assert "data.zip" not in result
    assert "main.py" in result


def test_filter_paths_max_files():
    paths = [f"src/file{i}.py" for i in range(200)]
    result = _filter_paths(paths, max_files=50)
    assert len(result) <= 50


def test_filter_paths_priority_ordering():
    paths = ["src/util.py", "README.md", "package.json", "Dockerfile"]
    result = _filter_paths(paths, max_files=10)
    assert result[0] == "README.md"
    assert result[1] in {"package.json", "Dockerfile"}


def test_detect_language_python():
    assert _detect_language("main.py") == "Python"


def test_detect_language_typescript():
    assert _detect_language("app.ts") == "TypeScript"


def test_detect_language_dockerfile():
    assert _detect_language("Dockerfile") == "Dockerfile"


def test_detect_language_unknown():
    assert _detect_language("binary.xyz") is None
