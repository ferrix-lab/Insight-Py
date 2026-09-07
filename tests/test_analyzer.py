from insight.analyzer import extract_code_stats


def test_inline_block_comment_does_not_hide_following_code() -> None:
    stats = extract_code_stats(
        "sample.js",
        "int count = 0; /* inline comment */\nint next = 1;\n",
    )

    assert stats["comments"] == 1


def test_async_functions_are_counted() -> None:
    stats = extract_code_stats(
        "sample.py",
        "async def fetch():\n    return 1\n",
    )

    assert stats["functions"] == 1


def test_relative_imports_are_rendered_without_none_values() -> None:
    stats = extract_code_stats("sample.py", "from . import utils\n")

    assert stats["imports"] == ["."]
