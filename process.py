""" Main processing python file"""
import json
import os
from typing import Iterable, List
import errors

# Load programming language extensions
def load_extensions(file_path: str) -> dict:
    """
    Loads the programming language extensions from a JSON file.
    Args:
        file_path (str): Path to the JSON file containing extensions.
    Returns:
        dict: A dictionary mapping file extensions to programming languages.
    """
    with open(file_path, "r", encoding="utf-8") as ext_file:
        return dict(json.load(ext_file))

# Filter directories to ignore
def filter_directories(dirs : List[str], ignore_dirs : List[str]) -> Iterable[str]:
    """
    Removes ignored directories from the directory list.
    Args:
        dirs (list): List of directories to filter.
        ignore_dirs (list): List of directories to ignore.
    """
    return list(filter(lambda d: d not in ignore_dirs, dirs))

# Check if a file should be ignored
def should_ignore_file(file_name : str, ignore_files : List[str]) -> bool:
    """
    Checks if a file should be ignored based on its name.
    Args:
        file_name (str): Name of the file.
        ignore_files (list): List of file names to ignore.
    Returns:
        bool: True if the file should be ignored, False otherwise.
    """
    return file_name in ignore_files

# Process a single file
def process_file(file_path, output, extension, sysout) -> None:
    """
    Processes a single file and appends its content to the Markdown output.
    Args:
        file_path (str): Path to the file to process.
        output (str): Path to the output Markdown file.
        extension (dict): Dictionary mapping file extensions to programming languages.
        sysout (callable): Function to handle output messages.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as code_content:
            c_string = ""
            for line in code_content:
                sysout(line)
                c_string += line
            get_extension = file_path.split(".")[-1]
            programming_lang = extension.get(get_extension, "config")
            content = f'\n### {file_path}\n```{programming_lang} \n{c_string}```\n\n'
            with open(output, 'a+', encoding="utf-8") as file:
                file.write(content)
    except UnicodeDecodeError as e:
        sysout(e)
    except FileNotFoundError as e:
        sysout(f"ERROR [-] {e}")
    except (PermissionError, IsADirectoryError, OSError, errors.FileProcessingException) as e:
        sysout(f"ERROR [-] {e}")

# Main processing function
def processing(dir_name, output: str, sysout=print) -> str:
    """
    Processes the files in a given directory and generates a Markdown file containing
    the content of source code files.
    Args:
        dir_name (str): The directory to process. All subdirectories and files within
                        this directory will be traversed.
        output (str): The path to the output Markdown file. The file must have a `.md` extension.
        sysout (callable, optional): A function to handle output messages. Defaults to `print`.
    Returns:
        str: The path to the output Markdown file if processing is successful.
        errors.ERROR_CODE: An error code if processing fails due to invalid output file extension.
    """
    defaut_ignore_files : List[str] = [
		".DS_Store",
		"desktop.ini",
		"Thumbs.db",
		".git",
		".gitignore",
		".idea",
		".vscode",
	]
    default_ignore_dirs : List[str] = [
		".DS_Store",
		"node_modules"
		"__pycache__",
        ]

    if not output.endswith(".md"):
        raise errors.FileProcessingException(
            "Output file must be a markdown file with .md extension")

    extension : dict = load_extensions("extension.json")

    for root, dirs, files in os.walk(dir_name):
        dirs : List[str] = filter_directories(dirs, default_ignore_dirs)
        for name in files:
            if should_ignore_file(name, defaut_ignore_files):
                continue
            if extension.get(name.split(".")[-1]) is None:
                continue
            file_path = os.path.join(root, name)
            process_file(file_path, output, extension, sysout)
    return output
