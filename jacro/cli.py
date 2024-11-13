"""Command-line interface to jacro."""

import sys
from pathlib import Path

from .template_processor import LOGGER, process_args, process_file


def main():
    """Main function."""
    if (parsed_args := process_args(sys.argv[1:])) is None:
        return

    input_file, output_file, mappings = parsed_args
    LOGGER.info(
        f"Input file: {input_file} with mappings: {mappings} and output file: {output_file}",
    )

    rendered_template = process_file(input_file, mappings)
    if not output_file:
        LOGGER.info(rendered_template)
    else:
        with Path(output_file).open("w") as f:
            f.write(rendered_template)


if __name__ == "__main__":
    main()
