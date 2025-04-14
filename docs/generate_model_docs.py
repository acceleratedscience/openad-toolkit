# python3 docs/generate_model_docs.py

import os
import re
import pandas as pd
import requests

from openad.helpers.output import output_error, output_text, output_success


def generate_model_docs():
    """
    Generate output/available-models.md page for documentation website.
    """

    model_data = _scrape_repos()
    # print(model_data)
    html = generate_md(model_data)
    write_html_file(html)

    # for model in model_data:
    #     output_text(f"<yellow>Name:</yellow> {model['name']}", pad_top=1)
    #     output_text(f"<yellow>Title:</yellow> {model['title']}")
    #     output_text(f"<yellow>Repo name:</yellow> {model['repo_name']}")
    #     output_text(f"<yellow>Url:</yellow> {model['url']}")
    #     output_text(f"<yellow>Compose:</yellow> {model['compose']}")
    #     output_text(f"<yellow>Description:</yellow> {model['description']}"[:100] + "...")


def scrape_repos():
    """
    Loop through docs/source/models.csv and scrape information from GitHub.
    """

    csv = os.path.join(os.path.dirname(__file__), "source", "models.csv")
    df = pd.read_csv(csv)

    results = []
    for _, row in df.iterrows():
        repo_url = row["Repository"]
        name = row["Name"]
        try:
            # Scrape the README.md file
            readme_url = f"{repo_url}/raw/main/README.md"
            repo_name = readme_url.replace("https://github.com/acceleratedscience/", "").split("/")[0]
            output_text(f"<soft>Scraping README for {name}: {repo_name}</soft>")
            readme_response = requests.get(readme_url, timeout=10)
            readme_text = readme_response.text if readme_response.status_code == 200 else ""
            title = readme_text.split("\n")[0] if readme_text else "No title found"
            title = title.replace("<!-- omit from toc -->", "")
            title = re.sub(r"^# ", "", title)
            title = title.strip()
            description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam est risus, euismod vitae dapibus id, aliquam et velit. Nam rutrum gravida euismod. Donec posuere dui sodales massa blandit, et laoreet sapien varius. Fusce ut molestie leo. Nullam facilisis posuere quam, vel pellentesque dui. Donec elementum tincidunt quam vitae eleifend. Curabitur sed eleifend ligula."

            # Check for compose.yml or compose.yaml
            compose_yml_url = f"{repo_url}/raw/main/compose.yml"
            compose_yaml_url = f"{repo_url}/raw/main/compose.yaml"
            compose_yml_exists = requests.get(compose_yml_url, timeout=10).status_code == 200
            compose_yaml_exists = requests.get(compose_yaml_url, timeout=10).status_code == 200
            compose_exists = compose_yml_exists or compose_yaml_exists

            # Append results
            results.append(
                {
                    "name": name,
                    "title": title,
                    "repo_name": repo_name,
                    "url": repo_url,
                    "compose": compose_exists,
                    "description": description,
                }
            )
        except Exception as e:
            print(f"Error processing {name}: {e}")

    return results


def _scrape_repos():
    return [
        {
            "name": "gen",
            "title": "No title found",
            "repo_name": "generation_inference_service",
            "url": "https://github.com/acceleratedscience/generation_inference_service",
            "compose": False,
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam est risus, euismod vitae dapibus id, aliquam et velit. Nam rutrum gravida euismod. Donec posuere dui sodales massa blandit, et laoreet sapien varius. Fusce ut molestie leo. Nullam facilisis posuere quam, vel pellentesque dui. Donec elementum tincidunt quam vitae eleifend. Curabitur sed eleifend ligula.",
        },
        {
            "name": "prop",
            "title": "No title found",
            "repo_name": "property_inference_service",
            "url": "https://github.com/acceleratedscience/property_inference_service",
            "compose": False,
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam est risus, euismod vitae dapibus id, aliquam et velit. Nam rutrum gravida euismod. Donec posuere dui sodales massa blandit, et laoreet sapien varius. Fusce ut molestie leo. Nullam facilisis posuere quam, vel pellentesque dui. Donec elementum tincidunt quam vitae eleifend. Curabitur sed eleifend ligula.",
        },
        {
            "name": "moler",
            "title": "No title found",
            "repo_name": "moler_inference_service",
            "url": "https://github.com/acceleratedscience/moler_inference_service",
            "compose": False,
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam est risus, euismod vitae dapibus id, aliquam et velit. Nam rutrum gravida euismod. Donec posuere dui sodales massa blandit, et laoreet sapien varius. Fusce ut molestie leo. Nullam facilisis posuere quam, vel pellentesque dui. Donec elementum tincidunt quam vitae eleifend. Curabitur sed eleifend ligula.",
        },
        {
            "name": "molf",
            "title": "Molformer Inference Service",
            "repo_name": "molformer_inference_service",
            "url": "https://github.com/acceleratedscience/molformer_inference_service",
            "compose": False,
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam est risus, euismod vitae dapibus id, aliquam et velit. Nam rutrum gravida euismod. Donec posuere dui sodales massa blandit, et laoreet sapien varius. Fusce ut molestie leo. Nullam facilisis posuere quam, vel pellentesque dui. Donec elementum tincidunt quam vitae eleifend. Curabitur sed eleifend ligula.",
        },
        {
            "name": "smi-ted",
            "title": "SMI-TED Inference for SMILES",
            "repo_name": "openad-model-smited",
            "url": "https://github.com/acceleratedscience/openad-model-smited",
            "compose": True,
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam est risus, euismod vitae dapibus id, aliquam et velit. Nam rutrum gravida euismod. Donec posuere dui sodales massa blandit, et laoreet sapien varius. Fusce ut molestie leo. Nullam facilisis posuere quam, vel pellentesque dui. Donec elementum tincidunt quam vitae eleifend. Curabitur sed eleifend ligula.",
        },
        {
            "name": "bmfm-sm",
            "title": "BMFM Small Molecules Inference for Smiles",
            "repo_name": "bmfm-sm",
            "url": "https://github.com/acceleratedscience/bmfm-sm",
            "compose": True,
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam est risus, euismod vitae dapibus id, aliquam et velit. Nam rutrum gravida euismod. Donec posuere dui sodales massa blandit, et laoreet sapien varius. Fusce ut molestie leo. Nullam facilisis posuere quam, vel pellentesque dui. Donec elementum tincidunt quam vitae eleifend. Curabitur sed eleifend ligula.",
        },
        {
            "name": "bmfm-pm",
            "title": "BMFM MAMMAL Inference for Proteins",
            "repo_name": "bmfm_mammal_inference",
            "url": "https://github.com/acceleratedscience/bmfm_mammal_inference",
            "compose": True,
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam est risus, euismod vitae dapibus id, aliquam et velit. Nam rutrum gravida euismod. Donec posuere dui sodales massa blandit, et laoreet sapien varius. Fusce ut molestie leo. Nullam facilisis posuere quam, vel pellentesque dui. Donec elementum tincidunt quam vitae eleifend. Curabitur sed eleifend ligula.",
        },
    ]


def generate_md(model_data):
    """
    Generate the markdown code for the page, based off of the scraped model data.
    """

    output = []
    for model in model_data:
        # Parse
        title = model["title"]
        description = model["description"]
        repo_name = model["repo_name"]
        url = model["url"]
        btn_github = f"[:carbon-icn-github: {repo_name}](#{url}){{ .md-button }}"
        btn_compose = (
            f"[compose.yml]({url}/raw/main/compose.yaml){{ .md-button .md-button--primary download='compose.yml' }}"
            if model["compose"]
            else "--REMOVE-LINE--"
        )
        instructions_url_container = "/docs/model-service/prepackaged-models-beta/#deployment-via-container"
        instructions_url_compose = "/docs/model-service/prepackaged-models-beta/#deployment-via-container-composeyml"
        instructions_url = instructions_url_compose if model["compose"] else instructions_url_container
        btn_instructions = f"[Instructions]({instructions_url}){{ .md-button .md-button--tertiary }}  "

        # Compile
        html_block = [
            f"<details markdown><summary>{title}</summary>",
            "<div markdown>",
            "",
            btn_github,
            btn_compose,
            btn_instructions,
            "",
            description,
            "",
            "</div>",
            "</details>",
            "",
        ]
        if "--REMOVE-LINE--" in html_block:
            html_block.remove("--REMOVE-LINE--")

        # Join
        output.append("\n".join(html_block))

    return "\n".join(output)


def write_html_file(html):
    """
    Write markdown file to disk.
    """

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    output_file = os.path.join(output_dir, "available-models.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Available Models\n\n" + html)

    output_success("Generated model documentation")


if __name__ == "__main__":
    generate_model_docs()
