import importlib
from pandas import DataFrame
from pandas.io.formats.style import Styler
from copy import deepcopy
import re
from openad.app.global_var_lib import _all_toolkits
from openad.toolkit.toolkit_main import load_toolkit
from openad.plugins.style_parser import tags_to_markdown
from openad.helpers.output import output_error, output_text, output_success
from openad.core.help import organize_commands


class OpenadAPI:
    """API class for OpenAD with memory leak fixes"""

    main_app = None
    module_name = "openad.app.main"
    name = None

    def __init__(self, name="No Name"):
        # Use instance-level context cache instead of class-level
        self.context_cache = deepcopy({"workspace": None, "toolkit": None})
        self.main_app = self._load_main()
        self.name = name

    def _load_main(self):
        spec = importlib.util.find_spec(self.module_name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def request(self, command, Vars=None, **kwargs):
        """Invokes the Magic command interface for OpenAD with memory cleanup"""
        api_variable = {}
        self.main_app.GLOBAL_SETTINGS["display"] = "api"
        command_list = command.split()
        x = len(command_list)
        i = 1
        if x > 1:
            while i < x:
                if command_list[i - 1].upper() == "DATAFRAME":
                    try:
                        df = kwargs[command_list[i]]
                        if isinstance(df, DataFrame):
                            api_variable[command_list[i]] = df
                    except:
                        pass
                i += 1

        # Execute the command
        result = self.main_app.api_remote(command, self.context_cache, api_variable)

        # MEMORY LEAK FIX: Clean up the global MAGIC_PROMPT after each request
        if hasattr(self.main_app, "MAGIC_PROMPT") and self.main_app.MAGIC_PROMPT is not None:
            magic_prompt = self.main_app.MAGIC_PROMPT

            # Clear accumulated data
            magic_prompt.api_variables.clear()
            # magic_prompt.molecule_list.clear()

            # Clear memory object
            if hasattr(magic_prompt, "memory") and magic_prompt.memory:
                magic_prompt.memory.wipe()

            # Clear global memory
            if hasattr(self.main_app, "MEMORY") and self.main_app.MEMORY:
                self.main_app.MEMORY.wipe()

        if isinstance(result, Styler):
            result = result.data

        return result

    def help_as_markdown(self, command):
        x = self.main_app.RUNCMD().do_help(command, display_info=False, jup_return_format=True)
        return x

    def __del__(self):
        # Clean up when instance is destroyed
        if hasattr(self.main_app, "MAGIC_PROMPT") and self.main_app.MAGIC_PROMPT is not None:
            magic_prompt = self.main_app.MAGIC_PROMPT
            magic_prompt.api_variables.clear()
            magic_prompt.molecule_list.clear()
        return

    def help_dump(self):
        """dumps the help text in markup"""
        # ... (rest of the method unchanged)
        output_text("<h1>Generating <yellow>commands.md</yellow> from help</h1>", pad_top=4)

        output = []
        toc = []

        jtd_identifier = (
            "---",
            "title: Commands",
            "layout: home",
            "nav_order: 4",
            "---",
        )
        output.append("\n".join(jtd_identifier) + "\n")

        comment = (
            "DO NOT EDIT",
            "-----------",
            "This file auto-generated.",
            "To update it, see openad/docs/generate_docs.py",
        )
        comment = "\n".join(comment)
        output.append(f"<!--\n\n{comment}\n\n-->" + "\n")

        output.append("## OpenAD\n")
        toc.append(_toc_link("OpenAD"))
        cmds = self.main_app.RUNCMD().current_help.help_current
        cmds_organized = organize_commands(cmds)
        _compile_section(output, toc, cmds_organized)

        for toolkit_name in _all_toolkits:
            output.append(f"## {toolkit_name}\n\n")
            toc.append(_toc_link(toolkit_name))
            success, toolkit = load_toolkit(toolkit_name, from_repo=True)
            if success:
                toolkit_cmds = toolkit.methods_help
                toolkit_cmds_organized = organize_commands(toolkit_cmds)
                _compile_section(output, toc, toolkit_cmds_organized)

        toc = "### Table of Contents\n" + "\n".join(toc) + "\n"
        output = output[:2] + [toc] + output[2:]
        output = "\n".join(output)
        return output

    def strip_leading_blanks(self, input):
        temp = input.split("\n")
        output = ""
        for x in temp:
            while str(x).startswith("   "):
                x = str(x).replace("   ", "  ")
            output = output + x + "\n"
        return output


# Helper functions (unchanged)
def _compile_section(output, toc, cmds_organized):
    output.append('<details markdown="block">')
    output.append("<summary>See commands</summary>\n")
    for category in cmds_organized:
        output.append(f"### {category}\n")
        toc.append(_toc_link(category, 1))
        for cmd_str, cmd_description in cmds_organized[category]:
            output.append(f"`{cmd_str.strip()}`{{: .cmd }}\n{_parse_description(cmd_description)}<br>\n")
        output.append("<br>\n")
    output.append("</details>\n")


def _parse_description(description):
    description = tags_to_markdown(description)
    description = re.sub(
        r"(\*\*Note:\*\*.+?)(\n{1,})",
        lambda match: (
            f"  > {match.group(1)}\n\n" if len(match.group(2)) == 1 else f"  > {match.group(1)}{match.group(2)}"
        ),
        description,
        flags=re.MULTILINE,
    )
    return description.strip()


def _toc_link(title, level=0):
    dash = "  " * level + "- "
    return f"{dash}[{title}](#{title.replace(' ', '-').lower()})"


if __name__ == "__main__":
    myclass = OpenadAPI("class1")
