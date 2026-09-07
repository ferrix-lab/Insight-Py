from pathlib import Path

from insight.reporter import generate_report


def test_reports_keep_same_basenames_distinct_and_linkable(tmp_path: Path) -> None:
    analysis = [
        {
            "file": "pkg_a/user.py",
            "total_lines": 1,
            "explanation": "first file",
            "preview": [],
        },
        {
            "file": "pkg_b/user.py",
            "total_lines": 2,
            "explanation": "second file",
            "preview": [],
        },
    ]

    generate_report(analysis, tmp_path)

    first_report = tmp_path / "pkg_a_user.py.md"
    second_report = tmp_path / "pkg_b_user.py.md"
    summary = (tmp_path / "summary.md").read_text(encoding="utf-8")

    assert first_report.read_text(encoding="utf-8").count("first file") == 1
    assert second_report.read_text(encoding="utf-8").count("second file") == 1
    assert "- [pkg_a_user.py.md](pkg_a_user.py.md) (1 lines)" in summary
    assert "- [pkg_b_user.py.md](pkg_b_user.py.md) (2 lines)" in summary
