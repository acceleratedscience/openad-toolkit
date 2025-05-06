"""Handles file System interactions"""

#!/usr/local/opt/python@3.9/bin/python3.9
#

import os
import shutil
from datetime import datetime

# Expand user path: ~/ --> ../
from pathlib import PosixPath

# Workers
from openad.workers.file_system import fs_get_workspace_files

# Helpers
from openad.helpers.general import confirm_prompt
from openad.helpers.output import output_text, output_error, output_success, output_table, output_warning
from openad.helpers.output_msgs import msg
from openad.helpers.paths import parse_path, prepare_file_path, fs_success, is_abs_path


# Globals
from openad.app.global_var_lib import _date_format


# Importing our own plugins.
# This is temporary until every plugin is available as a public pypi package.


def list_files(cmd_pointer, parser):
    import pprint

    path = parser["path"] if "path" in parser else ""
    data = fs_get_workspace_files(cmd_pointer, path)
    space = [""] if data["dirs"] else []
    files = data["dirs"] + space + data["files"]
    # pprint.pprint(files)
    table = []
    table_headers = ("File Name", "Size", "Last Edited")
    for file in files:
        # Insert space
        if not file:
            table.append(("-", "-", "-"))
            continue

        filetype = file["_meta"]["fileType"]
        filename = file["filename"] + ("/" if filetype == "dir" else "")
        size = file["_meta"]["size"] if "size" in file["_meta"] else None
        timestamp = file["_meta"]["timeEdited"] if "timeEdited" in file["_meta"] else None

        if filename.startswith("."):
            # For now we're jumping over hidden files, though
            # I would like to add an option to display them.
            # Probably `list all files` - moenen
            continue

        if size:
            if size < (1024 * 1024) / 10:
                size = f"{round(size / 1024, 2)} kB"
            else:
                size = f"{round(size / (1024 * 1024), 2)} MB"

        if timestamp:
            timestamp = datetime.fromtimestamp(timestamp / 1000)
            timestamp = timestamp.strftime(_date_format)

        result = (filename, size, timestamp)
        table.append(result)

    # return "OK"
    return output_table(table, is_data=False, headers=table_headers, colalign=("left", "right", "left"))


# External path to workspace path
def import_file(cmd_pointer, parser):
    """Import a file into your current workspace"""

    # Parse source
    file_path = parse_path(cmd_pointer, parser["file_path"])

    # File does not exist
    if not os.path.exists(file_path):
        return output_error(msg("err_file_doesnt_exist", file_path))

    # Parse destination, make sure dir exists etc.
    filename = os.path.basename(file_path)
    dest_path = prepare_file_path(cmd_pointer, filename)
    if not dest_path:
        return output_error("Aborted, no files were imported")

    # Success
    try:
        if os.path.isfile(file_path):
            shutil.copyfile(file_path, dest_path)
        elif os.path.isdir(file_path):
            shutil.copytree(file_path, dest_path)
        else:
            raise FileNotFoundError("No such file or directory")
        return fs_success(cmd_pointer, filename, dest_path)

    # Error
    except Exception as err:  # pylint: disable=broad-except
        return output_error(["Import failed", file_path, err])


def copy_or_move_file(cmd_pointer, parser):
    """Copy or move a file (or dir) from one place to another, possibly renaming it in the process."""

    # Parse command
    src_path = parse_path(cmd_pointer, parser["src_path"])
    dest_path_input = parser["dest_path"]
    action = parser["action"]  # "copy" or "move"
    force = True if "force" in parser else False  # Skip confirmation when renaming

    abort_msg = f"Aborted, no files were {'moved' if action == 'move' else 'copied'}"

    # Source file or directory does not exist
    if not os.path.exists(src_path):
        return output_error(msg("err_file_doesnt_exist", src_path))

    # Rename file if destination path includes filename
    rename = os.path.splitext(os.path.basename(dest_path_input))[1] != ""
    _name_from = os.path.basename(src_path)
    _name_to = os.path.basename(dest_path_input)
    if rename:
        if force or (confirm_prompt(f"Rename file from <reset>{_name_from}</reset> to <reset>{_name_to}</reset>?")):
            dest_path = prepare_file_path(cmd_pointer, dest_path_input)
        else:
            return output_error(abort_msg)

    else:
        filename = os.path.basename(src_path)
        dest_path = prepare_file_path(cmd_pointer, os.path.join(dest_path_input, filename))

    if not dest_path:
        return output_error(abort_msg)

    # Success
    try:
        if action == "move":
            shutil.move(src_path, dest_path)
        elif action == "copy":
            if os.path.isfile(src_path):
                shutil.copyfile(src_path, dest_path)
            elif os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
            else:
                raise FileNotFoundError("No such file or directory")
        return fs_success(cmd_pointer, dest_path_input, dest_path)

    # Error
    except Exception as err:  # pylint: disable=broad-except
        return output_error([f"Failed to {action}", src_path, err])


# Workspace path
def remove_file(cmd_pointer, parser):
    """Remove a file"""

    filename = parser["filename"]
    is_absolute_path = is_abs_path(filename)
    abort_msg = "Aborted, no files were removed"

    file_path = parse_path(cmd_pointer, filename)
    if not file_path:
        return output_error(abort_msg)

    path_type = "file" if os.path.isfile(file_path) else "directory"
    subject = "File" if path_type == "file" else "Directory"

    # Source does not exist
    if not os.path.exists(file_path):
        return output_error(msg("err_file_doesnt_exist", file_path))

    # Confirm prompt
    warning = (
        f"⚠️  You're about to delete a {path_type} outside of your workspace"
        if is_absolute_path
        else f"Permanently deleting {path_type}"
    )
    output_warning([f"{warning}:", file_path], return_val=False)
    if not confirm_prompt("Continue?"):
        return output_error(abort_msg)

    # Success
    try:
        if path_type == "file":
            os.remove(file_path)
        else:
            shutil.rmtree(file_path)
        fs_success(cmd_pointer, filename, file_path, subject=subject, action="removed")

    # Failure
    except Exception as err:  # pylint: disable=broad-except
        return output_error(["Something went wrong deleting this file", err])


# External path to workspace path
def import_file_LEGACY(cmd_pointer, parser):
    """Import a file from thefiles system external to Workspaces"""
    # Reset working directory as it can have changed.
    # os.chdir(_repo_dir)

    workspace_path = cmd_pointer.workspace_path(cmd_pointer.settings["workspace"])
    workspace_name = cmd_pointer.settings["workspace"].upper()
    source_file = parser["source"]
    dest_file = parser["destination"]

    # Expand user path: ~/ --> ../
    # from pathlib import PosixPath # Trash
    # source_file = PosixPath(source_file).expanduser().resolve() # Trash
    source_file = os.path.expanduser(source_file)

    if not os.path.exists(source_file):
        # Source does not exist
        return output_error(msg("err_file_doesnt_exist", source_file))
    elif os.path.exists(workspace_path + "/" + dest_file):
        # Destination already exists
        if not confirm_prompt("Destination file already exists. Overwrite?"):
            return output_error(msg("abort"))

    try:
        # Success
        # shutil.copyfile(PosixPath(source_file).expanduser().resolve(), path + '/' + dest_file) # Trash
        if os.path.isfile(source_file):
            shutil.copyfile(source_file, workspace_path + "/" + dest_file)
        else:
            # @later: Change language to reflect dir instead of file
            shutil.copytree(source_file, workspace_path + "/" + dest_file)
        return output_success(msg("success_import", source_file, workspace_name))
    except Exception as err:
        # Failure
        return output_error(msg("err_import", err))


# Workspace path to external path
def export_file_LEGACY(cmd_pointer, parser):
    """Exports a workspace file to the rechable filesystem"""
    # Reset working directory as it can have changed.
    # os.chdir(_repo_dir)

    workspace = cmd_pointer.workspace_path(cmd_pointer.settings["workspace"])
    source_file = parser["source"]
    dest_file = parser["destination"]
    workspace_name = cmd_pointer.settings["workspace"].upper()

    dest_file = PosixPath(dest_file).expanduser().resolve()

    if not os.path.exists(workspace + "/" + source_file):
        # Source does not exist
        return output_error(msg("err_file_doesnt_exist", workspace + "/" + source_file))

    elif os.path.exists(dest_file) is True:
        # Destination already exists
        if not confirm_prompt("Destination file already exists. Overwrite?"):
            return output_error(msg("abort"))
    try:
        # Success
        shutil.copyfile(workspace + "/" + source_file, dest_file)
        return output_success(msg("success_export", source_file, workspace_name, dest_file))
    except Exception as err:
        # Failure
        return output_error(msg("err_export", err))


# Workspace path to workspace name
def copy_file_LEGACY(cmd_pointer, parser):
    """copy a file betqeen workspaces"""
    # Reset working directory as it can have changed.
    # os.chdir(_repo_dir)

    source_file = parser["source"]
    source_file_path = cmd_pointer.workspace_path(cmd_pointer.settings["workspace"]) + "/" + source_file
    dest_file_path = cmd_pointer.workspace_path(parser["destination"]) + "/" + source_file
    source_workspace_name = cmd_pointer.settings["workspace"].upper()
    dest_workspace_name = parser["destination"].upper()

    if not os.path.exists(source_file_path):
        # Source does not exist
        return output_error(msg("err_file_doesnt_exist", source_file_path))
    elif (
        parser["destination"].upper() != source_workspace_name
        and dest_workspace_name not in cmd_pointer.settings["workspaces"]
    ):
        # Invalid destination
        return output_error(msg("invalid_workpace_destination", parser["destination"].upper()))
    elif os.path.exists(dest_file_path) is True:
        # Destination already exists
        if not confirm_prompt("Destination file already exists. Overwrite?"):
            return output_error(msg("abort"))
    try:
        # Success
        shutil.copyfile(source_file_path, dest_file_path)
        return output_success(msg("success_copy", source_file, source_workspace_name, dest_workspace_name))
    except Exception as err:
        # Failure
        return output_error(msg("err_copy", err))


# Workspace path
def remove_file_LEGACY(cmd_pointer, parser):
    """remove a file from a workspace"""
    workspace = cmd_pointer.workspace_path(cmd_pointer.settings["workspace"])
    file_name = parser["file"]
    file_path = workspace + "/" + file_name
    workspace_name = cmd_pointer.settings["workspace"].upper()

    if not os.path.exists(file_path):
        # Source does not exist
        return output_error(msg("err_file_doesnt_exist", file_path))
    if not confirm_prompt("Are you sure? This cannot be undone."):
        # Confirm prompt
        return output_error(msg("abort"))
    try:
        # Success
        os.remove(file_path)
        return output_success(msg("success_delete", file_name, workspace_name))
    except Exception as err:
        # Failure
        return output_error(msg("err_delete", err))


def open_file(cmd_pointer, parser):
    """
    Open a file in its designated OS application.
    """

    file_path = parse_path(cmd_pointer, parser["file"])
    os.system(f"open '{file_path}'")
