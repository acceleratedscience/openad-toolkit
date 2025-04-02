"""
Script to copy generated markdown files to the website repository.

The two repositories should be placed in the same parent folder for this to work:
/my-repos
    /openad-toolkit # <-- this repository
    /openad-website # <-- website repository

"""

import os
import shutil
from openad.helpers.output import output_error, output_warning, output_text, output_success

# Define source and destination directories
SOUCRE_DIR = "docs/output/markdown"
DEST_DIR = "../openad-website/main/docs"
DIR_STRUCTURE = [
    "/my-repos                        ",
    "  /openad-toolkit                ",
    "    /docs                        ",
    "      /output      <-- Source    ",
    "  /openad-website                ",
    "    /main                        ",
    "      /docs       <-- Destination",
]
FLAG_SUCCESS = f"<on_green> COPIED </on_green>"
FLAG_ERROR = f"<on_red> FAILED </on_red>"


def copy_docs(source_dir=SOUCRE_DIR, dest_dir=DEST_DIR):
    # Title
    output_text("\n\n\n<h1>Copying markdown files to the <yellow>openad-website</yellow> repository</h1>")

    # Source folder not found
    if not os.path.exists(source_dir):
        output_warning(
            [
                FLAG_ERROR
                + f" The source folder <error>{source_dir}</error> was not found, no files have been copied.\n"
                "<reset>Make sure your file cursor is pointed at the openad-toolkit repo's root directory.</reset>",
            ],
        )
        return

    # Destination folder not found
    if not os.path.exists(dest_dir):
        output_warning(
            [
                FLAG_ERROR + " The <error>openad-docs</error> repository was not found, no files have been copied.\n"
                "<reset>To have the output files copied automatically, make sure to place the openad-docs repo adjacent to this repo:</reset>",
                "\n".join(DIR_STRUCTURE),
            ],
        )
        return

    # Assemble list of files to copy
    for filename in os.listdir(source_dir):
        # Construct full file path
        source_file = os.path.join(source_dir, filename)
        dest_file = os.path.join(dest_dir, filename)

        if not os.path.exists(source_file):
            output_text(
                FLAG_ERROR + f" <red>{filename}</red> could not be found at <yellow>{source_file}</yellow>.",
                pad_btm=1,
            )
            return

        # Copy the file
        shutil.copy2(source_file, dest_file)
        output_text(
            FLAG_SUCCESS + f" <yellow>{filename}</yellow> to the <reset>openad-docs</reset> repository.",
            pad_btm=1,
        )

        # Remove source file
        os.remove(source_file)
