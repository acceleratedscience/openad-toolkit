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
show authentication group mapping
</details>

<details markdown code>
<summary markdown>
model auth add group '<auth_group>'|<auth_group> with '<api_key>'
</summary>
add an authentication group for model services to use
</details>

<details markdown code>
<summary markdown>
model auth remove group '<auth_group>' | <auth_group>
</summary>
remove an authentication group
</details>

<details markdown code>
<summary markdown>
model auth add service '<service_name>'|,service_name> to group '<auth_group>'|<auth_group>
</summary>
Attach an authentication group to a model service
</details>

<details markdown code>
<summary markdown>
model auth remove service '<service_name>'|<service_name>
</summary>
Detatch an authentication group from a model service
</details>

<details markdown code>
<summary markdown>
model service status
</summary>
Get the status of currently cataloged services
</details>

<details markdown code>
<summary markdown>
model service describe '<service_name>'|<service_name>
</summary>
get the configuration of a service
</details>

<details markdown code>
<summary markdown>
model catalog list
</summary>
get the list of currently cataloged services
</details>

<details markdown code>
<summary markdown>
uncatalog model service '<service_name>'|<service_name>
</summary>
uncatalog a model service 

 Example: 
<cmd>uncatalog model service 'gen'</cmd>
</details>

<details markdown code>
<summary markdown>
catalog model service from (remote) '<path> or <github> or <service_url>' as  '<service_name>'|<service_name>   USING (<parameter>=<value> <parameter>=<value>)
</summary>
catalog a model service from a path or github or remotely from an existing OpenAD service.
(USING) optional headers parameters for communication with service backend.
If you are cataloging a service using a model defined in a directory, provide the absolute <cmd> <path> </cmd> of that directory in quotes.

The following options require the <cmd>remote</cmd> option be declared.

If you are cataloging a service using a model defined in github repository, provide the absolute <cmd> <github> </cmd> of that github directory quotes.

If you are cataloging a remote service on a ip address and port provide the remote services ipaddress and port in quoted string e.g. <cmd>'0.0.0.0:8080'</cmd>

<cmd>service_name</cmd>: this is the name of the service as you will define it for your usage. e.g <cmd>prop</cmd> short for properties. 

USING Parameters:

If using a hosted service the following parameters must be supplied:
-<cmd>Inference-Service</cmd>: this is the name of the inference service that is hosted, it is a required parameter if cataloging a remote service.
An authorization parameter is always required if cataloging a hosted service, either Auhtorisation group (<cmd>auth_group</cmd>) or Authorisation bearer_token/api_key (<cmd>Authorization</cmd>):
-<cmd>auth_group</cmd>: this is the name of an authorization group which contains the api_key linked to the service access. This can only be used if <cmd>Authorization</cmd> is not also defined.
OR
-<cmd>Authorization</cmd>: this parameter is designed to be used when a <cmd>auth_group</cmd> is not defined.

Example:

Skypilot Deployment
-<cmd>catalog model service from 'git@github.com:acceleratedscience/generation_inference_service.git' as 'gen'</cmd>

Service using a authentication group 
-<cmd>catalog model service from remote '<service_url>' as  molf  USING (Inference-Service=molformer  )</cmd>
<cmd> model auth add service 'molf' to group 'default'</cmd>

Single Authorisation Service
-<cmd>openad catalog model service from remote '<service_URL>' as 'gen' USING (Inference-Service=generation Authorization='<api_key>')</cmd>

Catalog a remote service shared with you:
-<cmd>catalog model service from remote 'http://54.235.3.243:30001' as gen</cmd>
</details>

<details markdown code>
<summary markdown>
model service up '<service_name>'|<service_name> [no_gpu]}
</summary>
launches a cataloged model service when it was cataloged as a self managed service from a directory or github repository.
If you do not want to launch a service with GPU you should specify <cmd>no_gpu</cmd> at the end of the command.
#### Examples { .disable-anchor }


-<cmd>model service up gen</cmd>

-<cmd>model service up 'gen'</cmd>

-<cmd>model service up gen no_gpu</cmd>
</details>

<details markdown code>
<summary markdown>
model service local up '<service_name>'|<service_name>
</summary>
Launches a model service locally.

            Example:
              <cmd> model service local up gen</cmd>
</details>

<details markdown code>
<summary markdown>
model service down '<service_name>'|<service_name>
</summary>
Bring down a model service  
 #### Examples { .disable-anchor }


```shell
model service down gen
```

```shell
model service down 'gen'
```
</details>

<details markdown code>
<summary markdown>
get model service '<service_name>'|<service_name> result '<result_id>'
</summary>
retrieves a result from a model service  
 #### Examples { .disable-anchor }


<cmd>get model service myservier result 'wergergerg'
</details>

