import ast
import os
import logging
from .detector import explain_code
from .utils import list_source_files

def extract_code_stats(file_path, content):
    stats = {
        "functions": 0,
        "classes": 0,
        "imports": [],
        "comments": 0
    }

    # Count comments based on file type
    lines = content.splitlines()
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".py":
        # Python: # comments and triple-quoted docstrings
        comment_count = 0
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("#"):
                comment_count += 1
            elif '"""' in line or "'''" in line:
                # Count docstring lines (simplified)
                comment_count += 1
        stats["comments"] = comment_count
    elif ext in [".js", ".ts", ".tsx", ".jsx", ".java", ".cpp", ".c", ".cs", ".php"]:
        # C-style languages: // and /* */ comments
        comment_count = 0
        in_block_comment = False
        for line in lines:
            stripped = line.strip()
            if in_block_comment:
                comment_count += 1
                if "*/" in line:
                    in_block_comment = False
            elif stripped.startswith("//"):
                comment_count += 1
            elif "/*" in line:
                comment_count += 1
                if "*/" not in line.split("/*", 1)[1]:
                    in_block_comment = True
        stats["comments"] = comment_count
    else:
        # Default: count lines that look like comments
        stats["comments"] = sum(1 for line in lines if line.strip().startswith(("#", "//", "/*", "*")))

    if file_path.endswith(".py"):
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    stats["functions"] += 1
                elif isinstance(node, ast.ClassDef):
                    stats["classes"] += 1
                elif isinstance(node, ast.Import):
                    stats["imports"].extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    stats["imports"].append(node.module or "." * node.level)
        except Exception as e:
            logging.warning(f"Could not parse {file_path}: {e}")

    return stats

def analyze_file(file_path):
    with open(file_path, "r", errors="ignore") as f:
        content = f.read()

    lines = content.splitlines()
    preview = lines[:30]
    stats = extract_code_stats(file_path, content)
    explanation, ai_score = explain_code(content, file_path)

    return {
        "file": file_path,
        "total_lines": len(lines),
        "preview": preview,
        "explanation": explanation,
        "functions": stats["functions"],
        "classes": stats["classes"],
        "imports": stats["imports"],
        "comments": stats["comments"],
        "ai_score": ai_score
    }

def analyze_codebase(path, limit=None):
    results = []
    files = list(list_source_files(path))
    total_files = len(files)

    for idx, file_path in enumerate(files, start=1):
        if limit and idx > limit:
            break
        print(f"Processing {idx}/{total_files}: {file_path}")
        results.append(analyze_file(file_path))

    return results
