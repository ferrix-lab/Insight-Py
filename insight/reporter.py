import os


def _report_filename(file_path):
    normalized_path = os.path.normpath(file_path)
    if os.altsep:
        normalized_path = normalized_path.replace(os.altsep, "_")
    return normalized_path.replace(os.sep, "_").replace(":", "_") + ".md"


def save_file_report(file_info, output_dir):
    filename = _report_filename(file_info["file"])
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w") as f:
        f.write(f"# Report for `{file_info['file']}`\n\n")
        f.write(f"- **Total lines:** {file_info['total_lines']}\n")
        f.write(f"- **File type:** {os.path.splitext(file_info['file'])[1]}\n\n")

        f.write("## Explanation\n")
        f.write(file_info["explanation"] + "\n\n")

        f.write("## Code Preview (first 30 lines)\n")
        code_preview = "\n".join(file_info.get("preview", []))
        f.write("```text\n" + code_preview + "\n```\n")

def generate_report(analysis, output_dir="report"):
    os.makedirs(output_dir, exist_ok=True)

    for file_info in analysis:
        save_file_report(file_info, output_dir)

    summary_path = os.path.join(output_dir, "summary.md")
    total_lines = sum(f["total_lines"] for f in analysis)

    with open(summary_path, "w") as f:
        f.write("# Insight Codebase Summary\n\n")
        f.write(f"**Total files analyzed:** {len(analysis)}\n")
        f.write(f"**Total lines of code:** {total_lines}\n\n")
        f.write("## Files Included\n")
        for file_info in analysis:
            report_name = _report_filename(file_info["file"])
            f.write(f"- [{report_name}]({report_name}) ({file_info['total_lines']} lines)\n")
