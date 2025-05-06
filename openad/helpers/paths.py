import os
import re
from openad.helpers.output import output_error, output_warning, output_success
from openad.helpers.general import confirm_prompt

NOT_ALLOWED_ERR = [
    "Absolute paths are not allowed here",
    "To import this file into your workspace, run <cmd>import '{file_path}'</cmd>",
]


def prepare_file_path(cmd_pointer, file_path, fallback_ext=None, force_ext=None):
    """
    prepare a file path for saving.

    - Parse the path and turn into absolute path
    - Check if there is already a file at this location
        - If yes, ask to overwrite:
            - if yes, return the file path
            - if no, return the file path with the next available filename
        - If no, check if the folder structure exists
            - if yes, return the file path
            - if no, ask to create the folder structure
                - if yes, return the file path
                - if no, print error and return None
    """
    file_path = parse_path(cmd_pointer, file_path, fallback_ext, force_ext)
    file_path = _ensure_file_path(file_path)
    # if not file_path:
    #     output_error("Directory does not exist", return_val=False)
    #     return None
    return file_path


def parse_path(cmd_pointer, file_path, fallback_ext=None, force_ext=None) -> str:
    """
    Parse a path string to a path object.

    - foo:  workspace path
    - /foo: absolute path
    """

    if not file_path:
        return None

    # Detect path type
    is_absolute = file_path.startswith(("/", "\\"))
    is_cwd = file_path.startswith(("./", ".\\"))

    # Normalize the path string to use the appropriate
    # separator for the current system
    file_path = os.path.normpath(file_path)

    # Expand user path: ~/... --> /Users/my-username/...
    file_path = os.path.expanduser(file_path)

    # Separate filename from path
    path = os.path.dirname(file_path)
    filename = os.path.basename(file_path)

    # Force extension
    new_ext = None
    if force_ext:
        stem, ext = os.path.splitext(filename)
        filename = stem + "." + force_ext
        if ext and ext[1:] != force_ext:
            new_ext = force_ext

    # Fallback to default extension if none provided
    elif fallback_ext:
        ext = os.path.splitext(filename)[1]
        filename = filename if ext else filename + "." + fallback_ext

    # Absolute path
    if is_absolute:
        if jup_is_proxy():
            output_error(NOT_ALLOWED_ERR)
            return None
        path = os.path.join(path, filename)

    # Current working directory path
    elif is_cwd:
        path = os.path.normpath(os.path.join(os.getcwd(), path, filename))

    # Default: workspace path
    else:
        workspace_path = cmd_pointer.workspace_path()
        path = os.path.join(workspace_path, path, filename)

    # Display wrning when file extension is changed
    if new_ext:
        output_warning(
            [f"⚠️  File extension changed to <reset>{new_ext}</reset>", f"--> {path if is_absolute else filename}"],
            return_val=False,
        )
    return path


def _ensure_file_path(file_path) -> bool:
    """
    Ensure a file_path is valid.

    - Make sure we won't override an existing file
    - Create folder structure if it doesn't exist yet
    """
    if os.path.exists(file_path):
        # File already exists --> overwrite?
        if not confirm_prompt("The destination file already exists, overwrite?"):
            return _next_available_filename(file_path)
    elif not os.path.exists(os.path.dirname(file_path)):
        # Directory doesn't exist --> create?
        if not confirm_prompt("The destination directory does not exist, create it?"):
            return False
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as err:
            output_error(["Error creating directory", err])
            return False
    return file_path


def _next_available_filename(file_path) -> str:
    """
    Returns the file path with next available filename by appending a number to the filename.
    """
    if not os.path.exists(file_path):
        return file_path

    base = None
    ext = None
    if file_path.lower().endswith(".mol.json"):
        base = re.sub(r"(\.mol\.json)$", "", file_path)
        ext = ".mol.json"
    elif file_path.lower().endswith(".smol.json"):
        base = re.sub(r"(\.smol\.json)$", "", file_path)
        ext = ".smol.json"
    elif file_path.lower().endswith(".mmol.json"):
        base = re.sub(r"(\.mmol\.json)$", "", file_path)
        ext = ".mmol.json"
    elif file_path.lower().endswith(".molset.json"):
        base = re.sub(r"(\.molset\.json)$", "", file_path)
        ext = ".molset.json"
    else:
        base, ext = os.path.splitext(file_path)

    i = 1
    while os.path.exists(f"{base}-{i}{ext}"):
        i += 1
    return f"{base}-{i}{ext}"


def block_absolute(file_path) -> bool:
    """
    Display error when absolute paths are not allowed.

    Usage:
    if block_absolute(file_path):
        return
    """
    if is_abs_path(file_path):
        output_error(NOT_ALLOWED_ERR)
        return True
    return False


def is_abs_path(file_path) -> bool:
    """
    Check if a path is absolute.
    """
    if file_path.startswith(("/", "./", "~/", "\\", ".\\", "~\\")):
        return True
    return False


def fs_success(
    cmd_pointer,
    path_input,  # Destination user input, eg. foo.csv or /home/foo.csv or ./foo.csv
    path_resolved,  # Destination parsed through parse_path, eg. /home/user/foo.csv
    subject="File",
    action="saved",  # saved / removed
):
    """
    Path-type aware success message for saving files.
    """
    # Absolute path
    if is_abs_path(path_input):
        output_success(f"{subject} {action}: <yellow>{path_resolved}</yellow>", return_val=False)

    # Workspace path
    else:
        # Filename may have been modifier with index and extension,
        # so we need to parse it from the file_path instead.
        workspace_path = cmd_pointer.workspace_path()
        within_workspace_path = path_resolved.replace(workspace_path, "").lstrip("/")
        if action == "saved":
            output_success(
                f"{subject} saved to workspace as <yellow>{within_workspace_path}</yellow>", return_val=False
            )
        elif action == "removed":
            output_success([f"{subject} removed from workspace", within_workspace_path], return_val=False)


### ------


# Temp - this is part of openad-tools
def jup_is_proxy():
    import openad.helpers.jupyterlab_settings as jupyter_settings
    from openad.app.global_var_lib import GLOBAL_SETTINGS

    if not GLOBAL_SETTINGS["display"] == "notebook":
        return False

    try:
        jps = jupyter_settings.get_jupyter_lab_config()
        if jps["ServerApp"]["allow_remote_access"] is True and "127.0.0.1" in jps["ServerProxy"]["host_allowlist"]:
            return True
    except Exception:  # pylint: disable=broad-except
        return False
