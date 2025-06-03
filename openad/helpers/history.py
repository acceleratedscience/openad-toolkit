import os
import readline
from openad.helpers.output import output_text, output_error, output_success

DEBUG_HIST = False


def init_history(cmd_pointer):
    """
    Load history content from the .cmd_history file:
    - On startup
    - When switching workspaces
    """
    readline.set_history_length(cmd_pointer.histfile_size)
    if readline and os.path.exists(cmd_pointer.histfile):
        try:
            is_startup = readline.get_current_history_length() == 0
            if is_startup:
                readline.read_history_file(cmd_pointer.histfile)
                if DEBUG_HIST:
                    output_success(f"load_history_file: {cmd_pointer.histfile}", return_val=False)
        except Exception as err:  # pylint: disable=broad-exception-caught
            if DEBUG_HIST:
                output_error(["load_history_file", err], return_val=False)
    elif DEBUG_HIST:
        output_error(
            [
                f"load_history_file - .cmd_history not found in {cmd_pointer.settings['workspace']}",
                cmd_pointer.histfile,
            ],
            return_val=False,
        )


def clear_memory_history(cmd_pointer):
    """
    Clear the in-memory history without removing the history file.
    Used when switching workspaces.

    Workaround needed because readline doesn't let you clear in-memory
    history without also deleting the history file.
    """
    try:
        readline.write_history_file(cmd_pointer.histfile + "--temp")
        readline.clear_history()
        os.remove(cmd_pointer.histfile + "--temp")
    except Exception as err:  # pylint: disable=broad-exception-caught
        if DEBUG_HIST:
            output_error(["refresh_history", err], return_val=False)


def add_history_entry(cmd_pointer, inp):
    """
    Add the current command to the in-memory history.
    This is called when a command is executed.
    """
    try:
        # Ignore super long commands
        if len(str(str(inp).strip())) < int(4096):
            readline.add_history(str(str(inp).strip()))

        # Cap the in-memory history
        # Without this, it will keep on growing until you switch workspaces or restart kernel
        if readline.get_current_history_length() > cmd_pointer.histfile_size:
            readline.remove_history_item(0)

        if DEBUG_HIST:
            output_text(f"add_history_entry #{cmd_pointer.histfile_size}: {inp}", return_val=False)
    except Exception as err:  # pylint: disable=broad-exception-caught
        if DEBUG_HIST:
            output_error(["add_history_entry", err], return_val=False)


def update_history_file(cmd_pointer):
    """
    Write in-memory history to disk.
    """
    try:
        readline.write_history_file(cmd_pointer.histfile)
        if DEBUG_HIST:
            output_text(f"update_history_file: {cmd_pointer.histfile}", return_val=False)
    except Exception as err:  # pylint: disable=broad-exception-caught
        if DEBUG_HIST:
            output_error(["update_history_file", err], return_val=False)
