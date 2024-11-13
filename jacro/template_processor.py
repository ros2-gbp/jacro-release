"""Jacro: A simple template using jinja2."""

import argparse
import ast
import logging
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import jinja2
from ament_index_python.packages import get_package_share_directory
from rich.logging import RichHandler

REMAP = ":="

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(level=os.getenv("LOG_LEVEL", "INFO").upper())


def parse_list(value: str) -> str:
    """Convert a string representing a list with unquoted elements into a valid Python list string.

    Args:
        value: String representing a list (e.g. "[a, b, c]" or "[1, test, 3]")

    Returns:
        A string representation of the list with proper Python syntax
    """
    # Remove brackets and split into elements
    inner_value = value[1:-1]
    elements = [element.strip() for element in inner_value.split(",")]
    #  Try to preserve types for each element
    parsed_elements = []
    for element in elements:
        try:
            # Try to parse as number or other literal
            ast.literal_eval(element)
            parsed_elements.append(element)
        except (ValueError, SyntaxError):
            # If parsing fails, treat as string
            parsed_elements.append(repr(element))

    return f"[{', '.join(parsed_elements)}]"


def load_mappings(argv: list[str]) -> dict[str, str]:
    """Load name mappings encoded in command-line arguments.

    This will filter out any parameter assignment mappings.

    Args:
        argv: command-line arguments.

    Returns:
        A dictionary of name mappings.
    """
    mappings = {}
    for arg in argv:
        if REMAP in arg:
            key, value = arg.split(":=", 1)
            try:
                # Handle lists with unquoted elements
                if value.startswith("[") and value.endswith("]"):
                    value = parse_list(value)
                # Handle unquoted strings
                elif not (
                    value.startswith(("'", '"')) or value.replace(".", "").isdigit()
                ):
                    value = f"'{value}'"
                mappings[key] = ast.literal_eval(value)
            except (ValueError, SyntaxError):
                mappings[key] = value
    return mappings


def process_args(argv):
    """Process command-line arguments.

    Args:
        argv: command-line arguments.

    Returns:
        A tuple containing the input filename, output filename, and mappings.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", "-o", help="write output to FILE instead of stdout")
    parser.add_argument("input", help="Input file")

    mappings = load_mappings(argv)
    filtered_args = [a for a in argv if REMAP not in a]  # filter-out REMAP args

    options = parser.parse_args(filtered_args)

    return (options.input, options.output, mappings or {})


def ros_pkg_path(package_name: str) -> str:
    """Get the path to a ROS 2 package.

    Args:
        state: The state.
        package_name: The package name.

    Returns:
        The path to the package's share directory.
    """
    return get_package_share_directory(package_name)


def process_text(text: str, mappings: dict | None = None):
    """Process a text with mappings.

    Args:
        text: The text to process.
        mappings: The mappings to apply. Defaults to None.

    Returns:
        The processed text.
    """
    if mappings is None:
        mappings = {}
    jinja2_template = jinja2.Template(
        text,
        undefined=jinja2.make_logging_undefined(LOGGER, jinja2.StrictUndefined),
    )
    jinja2_template.globals["ros_pkg_path"] = ros_pkg_path
    return jinja2_template.render(mappings)


def process_file(
    input_filename: str | Path,
    mappings: dict | None = None,
    *,
    save: bool = False,
):
    """Process a file with mappings.

    Args:
        input_filename: The file to process.
        mappings: The mappings to apply. Defaults to None.
        save: Save the output to a temporary file. Defaults to False.

    Returns:
        Either the processed text or the path to the temporary file if save is True.
    """
    with Path(input_filename).open() as f:
        result = process_text(f.read(), mappings)
    if not save:
        return result
    with NamedTemporaryFile(
        mode="w",
        prefix="jacro_",
        delete=False,
    ) as temporary_file:
        temporary_file_path = temporary_file.name
        temporary_file.write(result)
        return temporary_file_path
