from pathlib import Path

from insight.utils import list_source_files


def _relative_sources(root: Path) -> set[str]:
    return {
        Path(path).relative_to(root).as_posix() for path in list_source_files(str(root))
    }


def test_list_source_files_respects_ignored_files_and_supports_extensionless_names(
    tmp_path: Path,
) -> None:
    (tmp_path / ".insightignore").write_text(".env\nignored.log\n", encoding="utf-8")
    (tmp_path / ".env").write_text("API_SECRET=do-not-send\n", encoding="utf-8")
    (tmp_path / "ignored.log").write_text("not source\n", encoding="utf-8")
    (tmp_path / "main.py").write_text("print('safe')\n", encoding="utf-8")
    for filename in ("Dockerfile", "Makefile", "Containerfile", "Jenkinsfile"):
        (tmp_path / filename).write_text("source\n", encoding="utf-8")

    ignored_directory = tmp_path / "venv"
    ignored_directory.mkdir()
    (ignored_directory / "secret.py").write_text("secret = True\n", encoding="utf-8")

    sources = _relative_sources(tmp_path)

    assert ".env" not in sources
    assert "ignored.log" not in sources
    assert "venv/secret.py" not in sources
    assert {
        "main.py",
        "Dockerfile",
        "Makefile",
        "Containerfile",
        "Jenkinsfile",
    } <= sources


def test_explicitly_ignored_file_is_not_returned(tmp_path: Path) -> None:
    (tmp_path / ".insightignore").write_text(".env\n", encoding="utf-8")
    ignored_file = tmp_path / ".env"
    ignored_file.write_text("API_SECRET=do-not-send\n", encoding="utf-8")

    assert list(list_source_files(str(ignored_file))) == []
