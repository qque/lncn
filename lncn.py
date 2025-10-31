import argparse
import os
import re

from pathlib import Path

USE_COLOR: int = not os.system("color")

def throw(process: str = "argparse") -> None:
    if process == "argparse":
        err = f"ERROR: Could not parse the given arguments, check the syntax of your command"
    
    if USE_COLOR:
        err = "\033[91m {}\033[00m".format(err)
    
    print(err)

def list_files_recursive(path: str) -> list[str]:
    files: list[str] = []

    if os.path.isfile(path):
        return [path]

    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            files.extend(list_files_recursive(full_path))
        else:
            files.append(full_path)

    return files

def file_count(path: str,
               ignore_empty_line: bool = True,
               ignore_multi_line_comments: bool = True,
               ignore_single_line_comments: bool = True,
               ignore_bracket_only_lines: bool = True) -> int:
    
    c_style_avoid_python = path.endswith((".c",".h",".cpp","hpp",".cc",".hh",".c++",".h++",".m",".mm",".C",".M"))

    if "_KEEPB" in globals():
        ignore_bracket_only_lines = False

    with open(path, "r") as file:
        count = 0
        
        content = file.read()

        if ignore_multi_line_comments:
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL) # C-style multi line
            content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL) # HTML-style multi line
            content = re.sub(r'^""".*?"""', '', content, flags=re.DOTALL) # Python-style multi line
            content = re.sub(r'^@doc raw""".*?"""', '', content, flags=re.DOTALL) # Julia version of Python-style

        for line in content.splitlines():
            if ignore_single_line_comments:
                line = line.strip()

                # if the file possibly has preprocessor commands, don't check python-style comments to avoid false positives
                if not c_style_avoid_python: 
                    line = re.sub(r'^#.*$', '', line) # Python-style single line

                line = re.sub(r'^//.*$', '', line) # C-style single line
                line = re.sub(r'^!.*$', '', line) # Fortran-style single line
                line = re.sub(r'^;.*$', '', line) # Assembly-style single line

            if ignore_bracket_only_lines:
                line = re.sub("|".join([r'\{', r'\}', r'\[', r'\]', r'\(', r'\)', r';']), '', line)

            if ignore_empty_line and not line:
                continue

            count += 1

    return count

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="lncn",
        description="Simple Python CLI to count SLOC in a codebase"
    )

    parser.add_argument(
        "path",
        type=str,
        default=None,
        help="Path to the directory or file that will be counted"
    )

    parser.add_argument(
        "-i", "--ignore",
        nargs="+",
        default=[],
        help="File/directory paths to ignore in the count"
    )

    parser.add_argument(
        "-b", "--braces",
        action="store_true",
        help="Keep lines with only braces and/or brackets as part of the count"
    )

    args = parser.parse_args()

    path = args.path
    
    ignore = []
    for i in args.ignore:
        if os.path.isfile(i):
            ignore.append(i)
        else:
            for r in list_files_recursive(i):
                ignore.append(r)

    if args.braces:
        global _KEEPB
        _KEEPB = True

    if path is None:
        throw()
        return 1
    else:
        if os.path.isfile(path):
            count = file_count(path)
        else:
            all_files = [f for f in list_files_recursive(path) if not any(Path(f) == Path(i) for i in ignore)]
            count = sum(map(file_count, all_files))
        
    print(count)
    return 0

if __name__ == "__main__":
    main()