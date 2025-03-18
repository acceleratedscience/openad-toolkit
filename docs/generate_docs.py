"""
Generate documentation files for the OpenAD Toolkit.
For more information, consult the README.md file in the docs folder.

python3 docs/generate_docs.py

"""

############################################################
# region - setup

import os
import re
import pyperclip

# Add the root directory to the sys.path
# root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# if str(root_dir) not in sys.path:
#     sys.path.append(root_dir)
# for path in sys.path:
#     print("*", path)

from copy_docs import copy_docs  # This resolves when running the script directly
from openad.app.main import RUNCMD as cmd_pointer
from openad.app.global_var_lib import _all_toolkits
from openad.core.help import organize_commands
from openad.toolkit.toolkit_main import load_toolkit
from openad.plugins.style_parser import tags_to_markdown
from openad.helpers.output import output_error, output_text, output_success
from openad.helpers.output_msgs import msg
from openad.helpers.files import open_file, write_file

# Get the repo path, this python file's parent folder.
# REPO_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) %%
FLAG_SUCCESS = f"<on_green> SUCCESS </on_green>"
FLAG_ERROR = f"<on_red> FAILED </on_red>"
DO_NOT_EDIT = (
    "<!--\n\n"
    "DO NOT EDIT\n"
    "-----------\n"
    "This file is auto-generated.\n"
    "To update it, consult instructions:\n"
    "https://github.com/acceleratedscience/open-ad-toolkit/tree/main/docs\n\n"
    "-->"
)
DO_NOT_EDIT_PYPI = (
    "<!--\n\n"
    "DO NOT EDIT\n"
    "-----------\n"
    "This file is auto-generated with modified links for PyPI.\n"
    "To update it, consult instructions:\n"
    "https://github.com/acceleratedscience/open-ad-toolkit/tree/main/docs\n\n"
    "-->"
)

# endregion

############################################################
# region - README.md (GitHub)


# Update the README.md file with OpenAD description.
def update_github_readme_md(filename="README.md"):
    output_text(f"<h1>Updating <yellow>{filename}</yellow> with OpenAD description</h1>", pad_top=2)

    # Read README.md file content
    readme_md, err_msg = open_file(filename, return_err=True)
    if not readme_md:
        output_text(FLAG_ERROR, pad_top=1)
        output_error(err_msg)
        return

    # Read description source file content
    description_txt, err_msg = open_file("openad/docs_src/description.txt", return_err=True)
    if not description_txt:
        output_text(FLAG_ERROR, pad_top=1)
        output_error(err_msg)
        return

    # Insert description
    readme_md_1 = readme_md.split("<!-- description -->")[0]
    readme_md_2 = readme_md.split("<!-- /description -->")[1]
    readme_md = readme_md_1 + "<!-- description -->\n" + description_txt + "\n<!-- /description -->" + readme_md_2

    # Write to output file
    success, err_msg = write_file(filename, readme_md, return_err=True)
    if success:
        output_text(FLAG_SUCCESS)
        output_text(f"<soft>Updated</soft> <reset>/{filename}</reset>")
    else:
        output_text(FLAG_ERROR)
        output_error(err_msg, pad=0)


# endregion

############################################################
# region - README/plugins.md (GitHub)


# Update the README_plugins.md file with the about_plugin description
def update_github_readme_plugins_md(filename="plugins.md"):
    output_text(f"<h1>Updating <yellow>{filename}</yellow> with about_plugin description</h1>", pad_top=2)

    # Read README.md file content
    readme_plugin_md, err_msg = open_file(f"README/{filename}", return_err=True)
    if not readme_plugin_md:
        output_text(FLAG_ERROR, pad_top=1)
        output_error(err_msg)
        return

    # Read about_plugin source file content
    about_plugin_txt, err_msg = open_file("openad/docs_src/about_plugin.txt", return_err=True)
    if not about_plugin_txt:
        output_text(FLAG_ERROR, pad_top=1)
        output_error(err_msg)
        return

    # Add some extra formatting to the about_plugin text
    about_plugin_txt = re.sub(r"^Note: ", "> **Note:** ", about_plugin_txt, flags=re.MULTILINE)

    # Insert about_plugin text
    readme_md_1 = readme_plugin_md.split("<!-- about_plugin -->")[0]
    readme_md_2 = readme_plugin_md.split("<!-- /about_plugin -->")[1]
    readme_plugin_md = (
        readme_md_1 + "<!-- about_plugin -->\n" + about_plugin_txt + "\n<!-- /about_plugin -->" + readme_md_2
    )

    # Write to output file
    success, err_msg = write_file(f"README/{filename}", readme_plugin_md, return_err=True)
    if success:
        output_text(FLAG_SUCCESS)
        output_text(f"<soft>Updated</soft> <reset>/README/{filename}</reset>")
    else:
        output_text(FLAG_ERROR)
        output_error(err_msg, pad=0)


# endregion

############################################################
# region - README/commands.md (GitHub)


# Update the README/commands.md with auto-generated commands
def generate_github_readme_commands_md():
    generate_commands_md("commands.md", for_github=True)


# endregion

############################################################
# region - base-concepts.md


# Generate the base-concepts.md file for the documentation website.
def generate_base_concepts_md(filename="base-concepts.md"):
    output_text(f"<h1>Generating <yellow>{filename}</yellow></h1>", pad_top=2)

    # Read base-concepts.md input file content
    base_concepts_md, err_msg = open_file("docs/input/base-concepts.md", return_err=True)
    if not base_concepts_md:
        output_text(FLAG_ERROR, pad_top=1)
        output_error(err_msg)
        return

    # Read about_workspace.txt source file content
    about_workspace, err_msg = open_file("openad/docs_src/about_workspace.txt", return_err=True)
    if not about_workspace:
        output_text(FLAG_ERROR, pad_top=1)
        output_error(err_msg)
        return

    # Read about_mws.txt source file content (molecule working set)
    about_mws, err_msg = open_file("openad/docs_src/about_mws.txt", return_err=True)
    if not about_mws:
        output_text(FLAG_ERROR, pad_top=1)
        output_error(err_msg)
        return

    # Read about_plugin.txt source file content
    about_plugin, err_msg = open_file("openad/docs_src/about_plugin.txt", return_err=True)
    if not about_plugin:
        output_text(FLAG_ERROR, pad_top=1)
        output_error(err_msg)
        return

    # Read about_context.txt source file content
    about_context, err_msg = open_file("openad/docs_src/about_context.txt", return_err=True)
    if not about_context:
        output_text(FLAG_ERROR, pad_top=1)
        output_error(err_msg)
        return

    # Read about_run.txt source file content
    about_run, err_msg = open_file("openad/docs_src/about_run.txt", return_err=True)
    if not about_run:
        output_text(FLAG_ERROR, pad_top=1)
        output_error(err_msg)
        return

    # Insert DO NOT EDIT comment
    base_concepts_md = re.sub(r"{{DO_NOT_EDIT}}", DO_NOT_EDIT, base_concepts_md, flags=re.DOTALL)

    # Insert descriptions
    base_concepts_md = re.sub(r"{{ABOUT_WORKSPACE}}", about_workspace, base_concepts_md, flags=re.DOTALL)
    base_concepts_md = re.sub(r"{{ABOUT_MWS}}", about_mws, base_concepts_md, flags=re.DOTALL)
    base_concepts_md = re.sub(r"{{ABOUT_PLUGIN}}", about_plugin, base_concepts_md, flags=re.DOTALL)
    base_concepts_md = re.sub(r"{{ABOUT_CONTEXT}}", about_context, base_concepts_md, flags=re.DOTALL)
    base_concepts_md = re.sub(r"{{ABOUT_RUN}}", about_run, base_concepts_md, flags=re.DOTALL)

    # Write to file
    success, err_msg = write_file(f"docs/output/markdown/{filename}", base_concepts_md, return_err=True)
    if success:
        output_text(FLAG_SUCCESS)
        output_text(f"<soft>Exported to</soft> <reset>/docs/output/markdown/{filename}</reset>")
    else:
        output_text(FLAG_ERROR)
        output_error(err_msg, pad=0)


# endregion

############################################################
# region - commands.md


# Loop through all commands and export them to a markdown file
# that is ready to be included in the just-the-docs documentation.
def generate_commands_md(filename="commands.md", for_github=False):
    output_text(f"<h1>Generating <yellow>{filename}</yellow> from help</h1>", pad_top=2)

    toc = []  # Table of content
    md_output = []  # Markdown

    # Parse main commands
    # - - -
    # For now, plugin commands are not included, but once we bring
    # them back, we'll want to organize the commands in sections.
    # - - -
    # md_output.append("\n\n## Main Commands\n")
    # toc.append(_toc_link("Main Commands"))
    cmds = cmd_pointer.current_help.help_current
    cmds_organized = organize_commands(cmds)
    parsed = _parse_section(cmds_organized)
    md_output += parsed["output"]
    toc += parsed["toc"]

    # Compile table of contents
    toc = "## Table of Contents\n" + "\n".join(toc) + "\n"

    # Compile commands
    md_output = "\n".join(md_output)

    # Read commands.md input content
    commands_md, err_msg = open_file("docs/input/commands.md", return_err=True)
    if not commands_md:
        output_text(FLAG_ERROR, pad_top=1)
        output_error(err_msg)
        return

    # Insert DO NOT EDIT comment
    commands_md = re.sub(r"{{DO_NOT_EDIT}}", DO_NOT_EDIT, commands_md, flags=re.DOTALL)

    # Insert table of contents
    commands_md = re.sub(r"{{TOC}}", toc, commands_md, flags=re.DOTALL)

    # Insert commands
    commands_md = re.sub(r"{{COMMANDS}}", md_output, commands_md, flags=re.DOTALL)

    # Write to file
    success, err_msg = write_file(f"docs/output/markdown/{filename}", commands_md, return_err=True)
    if success:
        output_text(FLAG_SUCCESS)
        output_text(f"<soft>Exported to</soft> <reset>/docs/output/markdown/{filename}</reset>")
    else:
        output_text(FLAG_ERROR)
        output_error(err_msg, pad=0)


# Compile all commands of a single section.
def _parse_section(cmds_organized):
    output = []
    toc = []
    for category in cmds_organized:
        output.append(f"### {category}\n")
        toc.append(_toc_link(category, 1))
        for cmd_str, cmd_description in cmds_organized[category]:
            # Break up inline descriptions (For `? ...` and `... ?`)
            if " --> " in cmd_str:
                split = cmd_str.split(" --> ")
                cmd_str = split[0]
                cmd_description = split[1]

            # Replace < and > with &lt; and &gt; so they don't get parsed as HTML tags
            cmd_str = cmd_str.replace("<", "&lt;").replace(">", "&gt;")

            # Compile markdown
            cmd_output = "\n".join(
                [
                    "<details markdown code>",
                    "<summary markdown>",
                    cmd_str.strip(),
                    "</summary>",
                    _parse_description(cmd_description),
                    "</details>\n",
                ]
            )
            output.append(cmd_output)

    return {
        "output": output,
        "toc": toc,
    }


# Prepare the command description for proper rendering.
def _parse_description(description):
    split = description.split("<h1>Examples</h1>")
    if len(split) == 1:
        split = description.split("Examples:")
    if len(split) == 1:
        split = description.split("Example:")
    description_only = split[0]
    examples = split[1] if len(split) > 1 else None

    # Format description:
    lines = description_only.splitlines()
    lines_formatted = []
    for line in lines:
        # Replace <h1> with fake #### h4 so it doesn't show up in the TOC
        line = re.sub(r"^<h1>(.+?)</h1>$", r"**\1**{.fake-h4}", line)
        # Replace style tags
        line = _tags_to_markdown(line)
        lines_formatted.append(line)
    description_only = "\n".join(lines_formatted)

    # Format examples:
    if examples:
        lines = examples.splitlines()
        lines_formatted = []
        for line in lines:
            line = line.strip()
            # Remove leading dash
            line = re.sub(r"^- ", "", line)
            # Wrap commands in code block
            print("*\n", f"--{line}--")
            line = re.sub(r"^<cmd>(.+?)</cmd>$", r"```shell\n\1\n```", line)
            print("*\n", f"--{line}--")
            # Replace style tags
            line = _tags_to_markdown(line)
            # Replace < and > with &lt; and &gt; so they don't get parsed as HTML tags
            if "```shell" not in line:
                line = line.replace("<", "&lt;").replace(">", "&gt;")
            lines_formatted.append(line)
        examples = "\n".join(lines_formatted)

        # Add title
        # Fake #### h4 so it doesn't show up in the TOC
        description = f"{description_only}\n**Examples**{{ .fake-h4 }}\n{examples}"

    # Format total
    description = _tags_to_markdown(description)

    # Convert to markdown
    # description = tags_to_markdown(description)
    # description = description.replace("Examples:", "#### Examples")

    # # Style notes as blockquotes, and ensure they're always
    # # followed by an empty line, to avoid the next lines to
    # # be treated as part of the blockquote.
    # description = re.sub(
    #     r"(\*\*Note:\*\*.+?)(\n{1,})",
    #     lambda match: (
    #         f"  > {match.group(1)}\n\n" if len(match.group(2)) == 1 else f"  > {match.group(1)}{match.group(2)}"
    #     ),
    #     description,
    #     flags=re.MULTILINE,
    # )

    # description = description.splitlines()
    # description = "\n".join([line.strip() for line in description])
    return description.strip()


# Convert a title to a markdown
# link for the table of contents.
# Foo Bar --> #foo-bar
def _toc_link(title, level=0):
    dash = "  " * level + "- "
    return f"{dash}[{title}](#{title.replace(' ', '-').lower()})"


def _tags_to_markdown(text):
    """
    Convert XML tags to markdown.

    This is forked from style parser, which was designed for Jupyter output
    and has some nuances that interfer with our usecase for MkDocs.
    We'll need to revisit the style parser at some point to be able to handle
    proper HTML output for a GUI terminal, after which this function can be replaced.
    """
    text = re.sub(r"<h1>(.*?)<\/h1>", r"## \1", text)
    text = re.sub(r"<h2>(.*?)<\/h2>", r"### \1", text)
    text = re.sub(r"<link>(.*?)<\/link>", r"[\1](\1)", text)  # Diff
    text = re.sub(r"<bold>(.*?)<\/bold>", r"**\1**", text)
    text = re.sub(r"<cmd>(.*?)<\/cmd>", r"`\1`", text)
    text = re.sub(r"<red>(.*?)<\/red>", r'<span style="color: #d00">\1</span>', text)
    text = re.sub(r"<green>(.*?)<\/green>", r'<span style="color: #090">\1</span>', text)
    text = re.sub(r"<yellow>(.*?)<\/yellow>", r'<span style="color: #dc0">\1</span>', text)
    text = re.sub(r"<blue>(.*?)<\/blue>", r'<span style="color: #00d">\1</span>', text)
    text = re.sub(r"<magenta>(.*?)<\/magenta>", r'<span style="color: #d07">\1</span>', text)
    text = re.sub(r"<cyan>(.*?)<\/cyan>", r'<span style="color: #0cc">\1</span>', text)
    text = re.sub(r"<on_red>(.*?)<\/on_red>", r'<span style="background: #d00; color: #fff">\1</span>', text)
    text = re.sub(r"<on_green>(.*?)<\/on_green>", r'<span style="background: #090; color: #fff">\1</span>', text)
    text = re.sub(r"<on_yellow>(.*?)<\/on_yellow>", r'<span style="background: #dc0; color: #fff">\1</span>', text)
    text = re.sub(r"<on_blue>(.*?)<\/on_blue>", r'<span style="background: #00d; color: #fff">\1</span>', text)
    text = re.sub(r"<on_magenta>(.*?)<\/on_magenta>", r'<span style="background: #d07; color: #fff">\1</span>', text)
    text = re.sub(r"<on_cyan>(.*?)<\/on_cyan>", r'<span style="background: #0cc; color: #fff">\1</span>', text)
    return text


# endregion

############################################################
# region - commands.csv


# Loop through all commands and export them to a CSV file.
# This is not used for anything in particular, other than
# to have a list of all commands in a file which can be annotated.
def generate_commands_csv(filename="commands.csv", delimiter=";"):
    output_text("<h1>Generating <yellow>commands.csv</yellow> from help</h1>", pad_top=2)
    output = [["Command", "Category"]]

    # Parse main commands
    cmds_main = cmd_pointer.current_help.help_current
    cmds_organized = organize_commands(cmds_main)

    # Parse tookit commands
    for toolkit_name in _all_toolkits:
        success, toolkit = load_toolkit(toolkit_name, from_repo=True)
        if success:
            toolkit_cmds = toolkit.methods_help
            toolkit_cmds_organized = organize_commands(toolkit_cmds)
            cmds_organized.update(toolkit_cmds_organized)

    # Add a row per command.
    for category, cmds in cmds_organized.items():
        for cmd in cmds:
            output.append([cmd[0], category])

    # Convert to CSV string
    output_str = "\n".join([f"{delimiter}".join(row) for row in output])

    # Convert to clipboard CSV string
    output_clipboard = "\n".join([f"\t".join(row) for row in output])
    pyperclip.copy(output_clipboard)

    # Write to file
    success, err_msg = write_file(f"docs/output/csv/{filename}", output_str, return_err=True)
    if success:
        output_text(FLAG_SUCCESS)
        output_text(f"<soft>Exported to</soft> <reset>/docs/output/csv/{filename}</reset>")
    else:
        output_text(FLAG_ERROR)
        output_error(err_msg, pad=0)
    output_success(msg("csv_to_clipboard"), pad=0)


# endregion

############################################################
# region - toolkits -> llm_description.txt


# Update commands in the llm_description.txt file per toolkit.
# Used as training data by the LLM for the "tell me" command.
# - - -
# Note: llm_description.txt needs to be set up with the toolkit
# LLM briefing set up and the following line will define where
# the commands are to be inserted - any text after this line
# will be overwritten:
# "The following commands are available for this toolkit:"
def generate_llm_description_txt(filename="llm_description.txt"):
    output_text("<h1>Updating commands in <yellow>llm_description.txt</yellow> for all toolkits</h1>", pad_top=2)

    # Loop through all toolkits
    for toolkit_name in _all_toolkits:
        flag_toolkit = f"<on_white><black> {toolkit_name} </black></on_white>"
        # Load toolkit
        success, toolkit = load_toolkit(toolkit_name, from_repo=True)
        if not success:
            err_msg = toolkit
            output_text(flag_toolkit + FLAG_ERROR)
            output_error(msg("err_load_toolkit", toolkit_name), pad=0)
            continue

        toolkit_cmds = toolkit.methods_help
        toolkit_cmds_organized = organize_commands(toolkit_cmds)
        output = _compile_commands(toolkit_cmds_organized)

        # Load llm_description.txt
        file_path = f"openad/user_toolkits/{toolkit_name}/{filename}"
        description_txt, err_msg = open_file(file_path, return_err=True)
        if not description_txt:
            output_text(flag_toolkit + FLAG_ERROR)
            # output_error(msg("err_load_toolkit_description", toolkit_name), pad=0) # Maybe overkill
            output_error(err_msg, pad_btm=1)
            continue

        # Insert commands into llm_description.txt
        splitter = "The following commands are available for this toolkit:"
        if splitter not in description_txt:
            output_text(flag_toolkit + FLAG_ERROR)
            output_error(msg("err_invalid_description_txt", toolkit_name, splitter), pad_btm=1)
            continue
        description_txt = description_txt.split(splitter)[0] + splitter + "\n\n"
        description_txt += "\n".join(output)
        description_txt = description_txt.strip()

        # print(("----" * 50) + "\n" + description_txt + "\n" + ("----" * 50))

        # Write to file
        success, err_msg = write_file(file_path, description_txt, return_err=True)
        if success:
            output_text(flag_toolkit + FLAG_SUCCESS)
            output_text(
                f"<soft>Updated in</soft> <reset>/docs/openad/user_toolkits/{toolkit_name}/{filename}</reset>",
                pad_btm=1,
            )
        else:
            output_text(flag_toolkit + FLAG_ERROR)
            output_error(err_msg, pad_btm=1)

    output_text("", pad_btm=2)


# Compile all commands for a single toolkit's llm_description.txt.
def _compile_commands(cmds_organized):
    output = []
    for category in cmds_organized:
        output.append(category + ":")
        for cmd_str, cmd_description in cmds_organized[category]:
            # Add command
            output.append(f"\t`{cmd_str.strip()}`")

            # Add command description
            cmd_description = tags_to_markdown(cmd_description).strip()
            cmd_description = cmd_description.replace("<br>", "")
            cmd_description = cmd_description.splitlines()
            cmd_description = "\n\t\t".join([line.strip() for line in cmd_description])
        output.append("")

    return output


# endregion

############################################################

if __name__ == "__main__":
    generate_commands_md()
    copy_docs(["commands.md"], dest_dir="../openad-website/main/documentation")

    # # Update existing README files
    # output_text("<magenta>Updating existing README files</magenta>", pad_top=4)
    # update_github_readme_md()
    # update_github_readme_plugins_md()

    # # Generate README files
    # output_text("<magenta>Generating README files</magenta>", pad_top=4)
    # generate_github_readme_commands_md()

    # # Generate additional bespoke pages for documentation website
    # output_text("<magenta>Generate additional doc website pages</magenta>", pad_top=4)
    # generate_base_concepts_md()
    # generate_commands_md()

    # # Render additional files
    # output_text("<magenta>Generate additional files</magenta>", pad_top=4)
    # generate_commands_csv()
    # generate_llm_description_txt()

    # # For testing
    # # _render_docs_page("index.md")

    # # Move all generated markdown files to the documentation repo
    # docs = []
    # for filename in os.listdir(f"docs/output/markdown"):
    #     docs.append(filename)
    # copy_docs(docs)
