try:
    from mcp.server import MCPServer
    from typing import Optional
except Exception as e:
    print("=" * 5, "Import Error", "=" * 5)
    print(e)
    exit()

mcp = MCPServer("swebench")


@mcp.tool()
def read_file(filepath: str, start_line: int,
              end_line: int) -> tuple[str, Optional[str]]:
    """Read the content of a file with line numbers"""
    try:
        with open(filepath, "r") as f:
            lines = f.read().split("\n")
    except Exception as e:
        return ("", str(e))
    return ('\n'.join([f"{line_no}: {lines[line_no]}"
            for line_no in range(start_line, end_line)]),
            None)


@mcp.tool()
def edit_file(filepath: str, old_str: str,
              new_str: str) -> tuple[bool, Optional[str]]:
    """Replace an exact string in a file with a new string"""
    try:
        with open(filepath, "r") as f:
            content = f.read().replace(old_str, new_str)
        with open(filepath, "w") as f:
            f.write(content)
    except Exception as e:
        return (False, str(e))
    return (True, None)


@mcp.tool()
def list_files(directory: str,
               pattern: str) -> tuple[list[str], Optional[str]]:
    """List files in a directory matching a given pattern"""
    from os import walk
    import re
    try:
        files = next(walk(directory, (None, None, [])))[2]
        files = list(filter(lambda x: bool(re.search(pattern, x)), files))
    except Exception as e:
        return ([], str(e))
    return (files, None)


@mcp.tool()
def search_code(pattern: str, file_pattern: str) -> tuple[str, Optional[str]]:
    """Perform a grep-like search in the codebase."""
    from os import walk
    import re
    from pathlib import Path
    answer = []
    try:
        for (dirpath, dirnames, filenames) in walk("."):
            for filename in filenames:
                if (re.match(file_pattern, filename)):
                    path = Path(filename).resolve()
                    with open(path, "r") as f:
                        lines = f.read().split("\n")
                    for line_no, line in enumerate(lines):
                        if (re.search(pattern, line)):
                            answer.append((path, line_no, line))
    except Exception as e:
        return ("", str(e))
    return ("\n".join([f"{file}: {line_no} {line}"
            for (file, line_no, line) in answer]),
            None)


@mcp.tool()
def search_function_or_class_definition_in_code(name):
    """Find the definition of a function or a class."""
    from os import walk
    import re
    from pathlib import Path
    answer = []
    try:
        for (dirpath, dirnames, filenames) in walk("."):
            for filename in filenames:
                path = Path(filename).resolve()
                with open(path, "r") as f:
                    lines = f.read().split("\n")
                for line_no, line in enumerate(lines):
                    if (re.search(
                                fr"^\s*def|class\s+{name}(\s|(|:)$",
                                line)):
                        answer.append((path, line_no, line))
    except Exception as e:
        return ("", str(e))
    return ("\n".join([f"{file}: {line_no} {line}"
            for (file, line_no, line) in answer]),
            None)


@mcp.tool()
def find_references(name, filepath, line):
    """Find all usages of a symbol (function or class)."""
    import re
    answer = []
    try:
        with open(filepath, "r") as f:
            lines = f.read().split("\n")
        for line_no, line in enumerate(lines):
            if (re.search(f"^.*{name}.*$", line)):
                answer.append((filepath, line_no, line))
    except Exception as e:
        return ("", str(e))
    return ("\n".join([f"{file}: {line_no} {line}"
            for (file, line_no, line) in answer]),
            None)


@mcp.tool()
def run_tests():
    """Execute the evaluation script."""


@mcp.tool()
def get_patch():
    """Retrieve the unified git diff of all changes made to the repository,
     depending on the implementation"""


@mcp.tool()
def run_command(command: str, workdir: str) -> tuple[str, str, int]:
    """Execute a shell command in the specified working directory.
    Returns the command's stdout, stderr, and exit code."""
    import subprocess
    result = subprocess.run(f"cd {workdir} && {command}",
                            shell=True, text=True, capture_output=True)
    return (result.stdout, result.stderr, result.returncode())
