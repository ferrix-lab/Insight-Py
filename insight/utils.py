import os

SUPPORTED_EXTS = (
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".c", ".cpp", ".cs",
    ".go", ".rb", ".php", ".rs", ".swift", ".kt", ".scala", ".dart",
    ".m", ".mm", ".sh", ".bat", ".pl", ".lua", ".r",
    ".html", ".htm", ".css", ".scss", ".less", ".ejs", ".erb", ".mustache", ".vue", ".svelte",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".xml", ".proto", ".graphql",
    ".md", ".rst", ".sql", ".gradle", ".pom", ".makefile", ".cmake", ".dockerfile", ".tf",
    ".ipynb"
)

SUPPORTED_FILENAMES = {"dockerfile", "makefile", "containerfile", "jenkinsfile"}

# Default directories to ignore
DEFAULT_IGNORED_DIRS = {"venv", "node_modules", "__pycache__", ".git", "dist", "build"}

def get_ignored_dirs(path):
    """Combine default ignored dirs with dirs from a .insightignore file."""
    ignored = DEFAULT_IGNORED_DIRS.copy()
    ignore_file = os.path.join(path, ".insightignore")
    
    if os.path.exists(ignore_file):
        try:
            with open(ignore_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Remove trailing slashes for consistent matching
                        ignored.add(line.strip('/'))
        except IOError:
            print(f"Warning: Could not read .insightignore file at {ignore_file}")
            
    return ignored

def list_source_files(path):
    """Yield all supported source files in a directory, skipping ignored dirs."""
    
    # Determine the base path to look for the ignore file
    base_path = path if os.path.isdir(path) else os.path.dirname(path)
    IGNORED_DIRS = get_ignored_dirs(base_path)

    if os.path.basename(os.path.normpath(path)) in IGNORED_DIRS:
        return

    if os.path.isfile(path):
        if os.path.basename(path) not in IGNORED_DIRS:
            yield path
        return

    for root, dirs, files in os.walk(path):
        # This line is key: it modifies the list of directories `os.walk` will visit
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        
        for file in files:
            if file in IGNORED_DIRS:
                continue
            # Check for both extension and exact filename match (for Dockerfile, etc.)
            if file.lower().endswith(SUPPORTED_EXTS) or file.lower() in SUPPORTED_FILENAMES:
                yield os.path.join(root, file)
