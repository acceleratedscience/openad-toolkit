<!--

DO NOT EDIT
-----------
This file is auto-generated.
To update it, consult instructions:
https://github.com/acceleratedscience/open-ad-toolkit/tree/main/docs

-->

# OpenAD Commands

This is the full list of available commands.

!!! info
    
    To run a commands in Jupyter Notebook, prepend it with `%openad` - more [information here](getting-started.md#getting-started-jupyter).

## Table of Contents
  - [Macromolecules](#macromolecules)
  - [General](#general)
  - [Workspaces](#workspaces)
  - [Toolkits](#toolkits)
  - [Runs](#runs)
  - [Utility](#utility)
  - [GUI](#gui)
  - [LLM](#llm)
  - [File System](#file-system)
  - [Help](#help)
  - [Model](#model)


<br>

[Expand all commands](#){ .md-button .md-button--primary onclick="Array.from(document.getElementsByTagName('details')).forEach(elm => elm.setAttribute('open', true)); return false" }

### Macromolecules

<details markdown code>
<summary markdown>
show mmol|protein <fasta> | '<pdb_id>'
</summary>
Launch the molecule viewer to visualize your macromolecule and inspect its properties.

#### Examples { .disable-anchor }

Show a protein by its PDBe ID:
```shell
show mmol '2g64'
```

Show a protein by its FASTA string:
```shell
show protein MAKWVCKICGYIYDEDAGDPDNGISPGTKFEELPDDWVCPICGAPKSEFEKLED
```
</details>

### General

<details markdown code>
<summary markdown>
openad
</summary>
Display the openad splash screen.
</details>

<details markdown code>
<summary markdown>
get status
</summary>
Display the currently selected workspace and toolkit.
</details>

<details markdown code>
<summary markdown>
display history
</summary>
Display the last 30 commands run in your current workspace.
</details>

<details markdown code>
<summary markdown>
clear sessions
</summary>
Clear any other sessions that may be running.
</details>

### Workspaces

<details markdown code>
<summary markdown>
set workspace <workspace_name>
</summary>
Change the current workspace.
</details>

<details markdown code>
<summary markdown>
get workspace [ <workspace_name> ]
</summary>
Display details a workspace. When no workspace name is passed, details of your current workspace are displayed.
</details>

<details markdown code>
<summary markdown>
create workspace <workspace_name> [ description('<description>') on path '<path>' ]
</summary>
Create a new workspace with an optional description and path.
</details>

<details markdown code>
<summary markdown>
remove workspace <workspace_name>
</summary>
Remove a workspace from your registry. Note that this doesn't remove the workspace's directory.
</details>

<details markdown code>
<summary markdown>
list workspaces
</summary>
Lists all your workspaces.
</details>

### Toolkits

<details markdown code>
<summary markdown>
set context <toolkit_name> [ reset ]
</summary>
Set your context to the chosen toolkit. By setting the context, the selected toolkit functions become available to you. The optional parameter <cmd>reset</cmd> can be used to reset your login information.
</details>

### Runs

<details markdown code>
<summary markdown>
create run
</summary>
Start recording a run.
</details>

<details markdown code>
<summary markdown>
remove run <run_name>
</summary>
remove a run.
</details>

<details markdown code>
<summary markdown>
save run as <run_name>
</summary>
Stop recording a run and save it.
</details>

<details markdown code>
<summary markdown>
run <run_name>
</summary>
Execute a previously recorded run. This will execute every command and continue regardless of any failures.
</details>

<details markdown code>
<summary markdown>
list runs
</summary>
List all runs saved in the current workspace.
</details>

<details markdown code>
<summary markdown>
display run <run_name>
</summary>
Display the commands stored in a certain run.
</details>

### Utility

<details markdown code>
<summary markdown>
display data '<filename.csv>'
</summary>
Display data from a csv file.
</details>

<details markdown code>
<summary markdown>
result save [as '<filename.csv>']
</summary>
Save table data to csv file.
</details>

<details markdown code>
<summary markdown>
result open
</summary>
Explore table data in the browser.
        
If you append <cmd>-d</cmd> to the end of the command <cmd>result open -d</cmd> display will result to data viewer.
</details>

<details markdown code>
<summary markdown>
result edit
</summary>
Edit table data in the browser.
        
If you append <cmd>-d</cmd> to the end of the command <cmd>result open -d</cmd> display will result to data viewer.
</details>

<details markdown code>
<summary markdown>
result copy
</summary>
Copy table data to clipboard, formatted for spreadheet.
</details>

<details markdown code>
<summary markdown>
result display
</summary>
Display the result in the CLI.
      
If you append <cmd>-d</cmd> to the end of the command <cmd>result open -d</cmd> display will result to data viewer.
</details>

<details markdown code>
<summary markdown>
result as dataframe
</summary>
Return the result as dataframe (only for Jupyter Notebook)
</details>

<details markdown code>
<summary markdown>
edit config '<json_config_file>' [ schema '<schema_file>']
</summary>
Edit any JSON file in your workspace directly from the CLI. If a schema is specified, it will be used for validation and documentation.
</details>

### GUI

<details markdown code>
<summary markdown>
install gui
</summary>
Install the OpenAD GUI (graphical user interface).

The graphical user interface allows you to browse your workspace and visualize your datasets and molecules.
</details>

<details markdown code>
<summary markdown>
launch gui
</summary>
Launch the OpenAD GUI (graphical user interface).
</details>

<details markdown code>
<summary markdown>
restart gui
</summary>
Terminate and then restart the GUI server.
</details>

<details markdown code>
<summary markdown>
quit gui
</summary>
Terminate the GUI server.
</details>

### LLM

<details markdown code>
<summary markdown>
tell me <how to do xyz>
</summary>
Ask your AI assistant how to do anything in OpenAD.
</details>

<details markdown code>
<summary markdown>
set llm  <language_model_name>
</summary>
Set the target language model name for the <cmd>tell me</cmd> command.
</details>

<details markdown code>
<summary markdown>
clear llm auth
</summary>
Clear the language model's authentication file.
</details>

### File System

<details markdown code>
<summary markdown>
list files [ path ]
</summary>
List al directories and files in your current workspace.
</details>

<details markdown code>
<summary markdown>
import from '<external_source_file>' to '<workspace_file>'
</summary>
Import a file from outside OpenAD into your current workspace.
</details>

<details markdown code>
<summary markdown>
export from '<workspace_file>' to '<external_file>'
</summary>
Export a file from your current workspace to anywhere on your hard drive.
</details>

<details markdown code>
<summary markdown>
copy file '<workspace_file>' to '<other_workspace_name>'
</summary>
Export a file from your current workspace to another workspace.
</details>

<details markdown code>
<summary markdown>
remove '<filename>'
</summary>
Remove a file from your current workspace.
</details>

<details markdown code>
<summary markdown>
open '<filename>'
</summary>
Open a file or dataframe in the graphical user interface.

#### Examples { .disable-anchor }

```shell
open 'base_molecules.sdf'
```
```shell
open my_dataframe
```
</details>

### Help

<details markdown code>
<summary markdown>
intro
</summary>
Display an introduction to the OpenAD CLI.
</details>

<details markdown code>
<summary markdown>
docs
</summary>
Open the documentation webpage.
</details>

<details markdown code>
<summary markdown>
?
</summary>
List all available commands.
</details>

<details markdown code>
<summary markdown>
? ...<soft>
</summary>
List all commands containing "..."</soft>
</details>

<details markdown code>
<summary markdown>
... ?<soft>
</summary>
List all commands starting with "..."</soft>
</details>

### Model

<details markdown code>
<summary markdown>
model auth list
</summary>
List authentication groups that have been added.
</details>

<details markdown code>
<summary markdown>
model auth add group <auth_group> with '<auth_token>'
</summary>
Add an authentication group for model services to use.

Single quotes are required for your <cmd><auth_token></cmd> but optional for <cmd><auth_group></cmd> in case it contains a space or special character.

Authorization is required to connect to IBM-hosted models (IBM partners only). Using an auth group allows you to authorize multiple models at once, and is the recommended authorization method.

#### Examples { .disable-anchor }

1. Copy your authentication token from <link>http://open.accelerate.science</link> (or your custom URL if your company us running its own instance).
2. Create an auth group, e.g. 'default':
```shell
model auth add group default with '<auth_token>'
```
3. Catalog your services with the auth_group provided:
```shell
model service catalog from remote 'https://open.accelerate.science/proxy' as gen using (inference-service=generation auth_group=default)
```

You can also add a cataloged model to a group after you've created it:
```shell
model auth add service gen to group default
```
</details>

<details markdown code>
<summary markdown>
model auth remove group <auth_group>
</summary>
Remove an authentication group.

Single quotes are optional in case <cmd>auth_group</cmd> contains a space or special character.

#### Examples { .disable-anchor }

```shell
model auth remove group default
```
```shell
model auth remove group 'my group'
```
</details>

<details markdown code>
<summary markdown>
model auth add service <service_name> to group <auth_group>
</summary>
Ad a model service to an authentication group.

Single quotes are optional for both <cmd><service_name></cmd> and <cmd><auth_group></cmd> in case they contain a space or special character.

#### Examples { .disable-anchor }

<cmd>model auth add service molf to group default<cmd>
<cmd>model auth add service 'my molf' to group 'my group'<cmd>
</details>

<details markdown code>
<summary markdown>
model auth remove service <service_name>
</summary>
Detach a model service from an authentication group.

Single quotes are optional in case <cmd>service_name</cmd> contains a space or special character.

#### Examples { .disable-anchor }

```shell
model auth remove service molf
```
```shell
model auth remove service 'my molf'
```
</details>

<details markdown code>
<summary markdown>
model service status
</summary>
Get the status of your currently cataloged services.
</details>

<details markdown code>
<summary markdown>
model service describe <service_name>
</summary>
Get a service's configuration details.

Single quotes are optional in case <cmd>service_name</cmd> contains a space or special character.

#### Examples { .disable-anchor }

```shell
model service describe gen
```
```shell
model service describe 'my gen'
```
</details>

<details markdown code>
<summary markdown>
model service list
</summary>
List your currently cataloged services.
</details>

<details markdown code>
<summary markdown>
model service uncatalog <service_name>
</summary>
Uncatalog a model service.

Single quotes are optional in case <cmd>service_name</cmd> contains a space or special character.

#### Examples { .disable-anchor }

```shell
uncatalog model service 'gen'
```
```shell
uncatalog model service 'my gen'
```
</details>

<details markdown code>
<summary markdown>
model service catalog from [ remote ] '<path>|<github>|<service_url>' as <service_name> USING (<parameter>=<value> <parameter>=<value>)
</summary>
Catalog a model service from a local path, from GitHub or from an hosted service URL.

            
<h1>Parameters</h1>

<cmd><path>|<github>|<service_url></cmd>
    The location of the model service, to be provided in single quotes.
    This can be a local path, a GitHub SSH URI, or a URL for an existing remote service:
    <soft>...</soft><cmd>from '/path/to/service'</cmd>
    <soft>...</soft><cmd>from 'git@github.com:acceleratedscience/generation_inference_service.git'</cmd>
    <soft>...</soft><cmd>from remote '0.0.0.0:8080'</cmd> <soft>// Note: 'remote' is required for cataloging a remote service</soft>

<cmd><service_name></cmd>
    How you will be refering to the service when using it. Keep it short, e.g. <cmd>prop</cmd> for a service that calculates properties.
    Single quotes are optional in case you want to used a space or special character.

    
<h1>The USING Clause</h1>

The parameters below are only needed when connecting to an IBM-hosted service (IBM partners only).

<cmd>inference-service=<string></cmd> (required)
    The name of the inference service you want to connect to, eg. generation ot molformer.
Authorization:
    To authorize to an IBM-hosted service (IBM partners only), you have two options:
    1. <cmd>authorization='<auth_token>'</cmd>
        Provide your authorzation token directly.
        Note: to use this option, <cmd>auth_group</cmd> can not be defined.
    2. <cmd>auth_group=<auth_group_name></cmd>
        The name of an authorization group which contains your <cmd>auth_token</cmd>.
        This is recommended if you will be using more than one model service.
        For instructions on how to set up an auth group, run <cmd>model auth add group ?</cmd>
        Note: to use this option, <cmd>authorization</cmd> can not be defined.


#### Examples { .disable-anchor }


Catalog a model using SkyPilot deployment
```shell
catalog model service from 'git@github.com:acceleratedscience/generation_inference_service.git' as gen
```

Catalog a model using a authentication group
<cmd>catalog model service from remote 'https://open.accelerate.science/proxy' as molf
USING (inference-service=molformer auth_group=default)</cmd>

Catalog a model using an authorization token
<cmd>openad catalog model service from remote 'https://open.accelerate.science/proxy' as gen
USING (inference-service=generation authorization='<auth_token>')</cmd>

Catalog a remote service that was shared with you:
```shell
catalog model service from remote 'http://54.235.3.243:3001' as gen
```
</details>

<details markdown code>
<summary markdown>
model service up <service_name> [ no_gpu ]
</summary>
Launch a model service, after it was cataloged using <cmd>model service catalog</cmd>.

Single quotes are optional in case <cmd>service_name</cmd> contains a space or special character.

If you don't want your service to use GPU you can append the <cmd>no_gpu</cmd> clause.

#### Examples { .disable-anchor }

```shell
model service up gen
```
```shell
model service up 'my gen'
```
```shell
model service up gen no_gpu
```
</details>

<details markdown code>
<summary markdown>
model service local up <service_name> [ no_gpu ]
</summary>
Launch a model service locally.

Single quotes are optional in case <cmd>service_name</cmd> contains a space or special character.

If you don't want your service to use GPU you can append the <cmd>no_gpu</cmd> clause.

#### Examples { .disable-anchor }

```shell
 model service local up gen
```
```shell
 model service local up 'my gen'
```
```shell
 model service local up gen no_gpu
```
</details>

<details markdown code>
<summary markdown>
model service down <service_name>
</summary>
Deactivate a model service.

Single quotes are optional in case <cmd>service_name</cmd> contains a space or special character.

#### Examples { .disable-anchor }

```shell
model service down gen
```
```shell
model service down 'my gen'
```
</details>

<details markdown code>
<summary markdown>
model service get result <service_name> '<result_id>'
</summary>
Retrieve a result from a model service.
            
Single quotes are optional in case <cmd>service_name</cmd> contains a space or special character.

#### Examples { .disable-anchor }

<cmd>get model service gen result 'xyz'
<cmd>get model service 'my gen' result 'xyz'
</details>

