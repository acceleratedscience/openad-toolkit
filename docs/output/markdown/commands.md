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
show mmol|protein &lt;fasta&gt; | '&lt;pdb_id&gt;'
</summary>
Launch the molecule viewer to visualize your macromolecule and inspect its properties.

**Examples**{ .fake-h4 }

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
set workspace &lt;workspace_name&gt;
</summary>
Change the current workspace.
</details>

<details markdown code>
<summary markdown>
get workspace [ &lt;workspace_name&gt; ]
</summary>
Display details a workspace. When no workspace name is passed, details of your current workspace are displayed.
</details>

<details markdown code>
<summary markdown>
create workspace &lt;workspace_name&gt; [ description('&lt;description&gt;') on path '&lt;path&gt;' ]
</summary>
Create a new workspace with an optional description and path.
</details>

<details markdown code>
<summary markdown>
remove workspace &lt;workspace_name&gt;
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
set context &lt;toolkit_name&gt; [ reset ]
</summary>
Set your context to the chosen toolkit. By setting the context, the selected toolkit functions become available to you. The optional parameter `reset` can be used to reset your login information.
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
remove run &lt;run_name&gt;
</summary>
remove a run.
</details>

<details markdown code>
<summary markdown>
save run as &lt;run_name&gt;
</summary>
Stop recording a run and save it.
</details>

<details markdown code>
<summary markdown>
run &lt;run_name&gt;
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
display run &lt;run_name&gt;
</summary>
Display the commands stored in a certain run.
</details>

### Utility

<details markdown code>
<summary markdown>
display data '&lt;filename.csv&gt;'
</summary>
Display data from a csv file.
</details>

<details markdown code>
<summary markdown>
result save [as '&lt;filename.csv&gt;']
</summary>
Save table data to csv file.
</details>

<details markdown code>
<summary markdown>
result open
</summary>
Explore table data in the browser.
        
If you append `-d` to the end of the command `result open -d` display will result to data viewer.
</details>

<details markdown code>
<summary markdown>
result edit
</summary>
Edit table data in the browser.
        
If you append `-d` to the end of the command `result open -d` display will result to data viewer.
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
      
If you append `-d` to the end of the command `result open -d` display will result to data viewer.
</details>

<details markdown code>
<summary markdown>
result as dataframe
</summary>
Return the result as dataframe (only for Jupyter Notebook)
</details>

<details markdown code>
<summary markdown>
edit config '&lt;json_config_file&gt;' [ schema '&lt;schema_file&gt;']
</summary>
Edit any JSON file in your workspace directly from the CLI. If a schema is specified, it will be used for validation and documentation.
</details>

### GUI

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
tell me &lt;how to do xyz&gt;
</summary>
Ask your AI assistant how to do anything in OpenAD.
</details>

<details markdown code>
<summary markdown>
set llm  &lt;language_model_name&gt;
</summary>
Set the target language model name for the `tell me` command.
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
import from '&lt;external_source_file&gt;' to '&lt;workspace_file&gt;'
</summary>
Import a file from outside OpenAD into your current workspace.
</details>

<details markdown code>
<summary markdown>
export from '&lt;workspace_file&gt;' to '&lt;external_file&gt;'
</summary>
Export a file from your current workspace to anywhere on your hard drive.
</details>

<details markdown code>
<summary markdown>
copy file '&lt;workspace_file&gt;' to '&lt;other_workspace_name&gt;'
</summary>
Export a file from your current workspace to another workspace.
</details>

<details markdown code>
<summary markdown>
remove '&lt;filename&gt;'
</summary>
Remove a file from your current workspace.
</details>

<details markdown code>
<summary markdown>
open '&lt;filename&gt;'
</summary>
Open a file or dataframe in the graphical user interface.

**Examples**{ .fake-h4 }

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
? ...&lt;soft&gt;
</summary>
List all commands containing "..."</soft>
</details>

<details markdown code>
<summary markdown>
... ?&lt;soft&gt;
</summary>
List all commands starting with "..."</soft>
</details>

### Model

<details markdown code>
<summary markdown>
model auth list
</summary>
List authentication groups that have been created.
</details>

<details markdown code>
<summary markdown>
model auth add group &lt;auth_group&gt; with '&lt;auth_token&gt;'
</summary>
Create a new authentication group for model services to use.

Single quotes are required for your `<auth_token>` but optional for `<auth_group>` in case it contains a space or special character.

Authorization is required to connect to IBM-hosted models (IBM partners only). Using an auth group allows you to authorize multiple models at once, and is the recommended authorization method.

**Examples**{ .fake-h4 }

1. Copy your authentication token from [http://open.accelerate.science](http://open.accelerate.science) (or your custom URL if your company us running its own instance).
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
model auth remove group &lt;auth_group&gt;
</summary>
Remove an authentication group.

Single quotes are optional in case `auth_group` contains a space or special character.

**Examples**{ .fake-h4 }

```shell
model auth remove group default
```
```shell
model auth remove group 'my group'
```
</details>

<details markdown code>
<summary markdown>
model auth add service &lt;service_name&gt; to group &lt;auth_group&gt;
</summary>
Ad a model service to an authentication group.

Single quotes are optional for both `<service_name>` and `<auth_group>` in case they contain a space or special character.

**Examples**{ .fake-h4 }

```shell
model auth add service molf to group default
```
```shell
model auth add service 'my molf' to group 'my group'
```
</details>

<details markdown code>
<summary markdown>
model auth remove service &lt;service_name&gt;
</summary>
Detach a model service from an authentication group.

Single quotes are optional in case `service_name` contains a space or special character.

**Examples**{ .fake-h4 }

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
model service describe &lt;service_name&gt;
</summary>
Get a service's configuration details.

Single quotes are optional in case `service_name` contains a space or special character.

**Examples**{ .fake-h4 }

```shell
model service describe gen
```
```shell
model service describe 'my gen'
```
</details>

<details markdown code>
<summary markdown>
model catalog list
</summary>
List your currently cataloged services.
</details>

<details markdown code>
<summary markdown>
uncatalog model service &lt;service_name&gt;
</summary>
Uncatalog a model service.

Single quotes are optional in case `service_name` contains a space or special character.

**Examples**{ .fake-h4 }

```shell
uncatalog model service 'gen'
```
```shell
uncatalog model service 'my gen'
```
</details>

<details markdown code>
<summary markdown>
catalog model service from [ remote ] '&lt;path&gt;|&lt;github&gt;|&lt;service_url&gt;' as &lt;service_name&gt; USING (&lt;parameter&gt;=&lt;value&gt; &lt;parameter&gt;=&lt;value&gt;)
</summary>
Catalog a model service from a local path, from GitHub or from an hosted service URL.

Use the `remote` clause when cataloging from a hosted service URL.

            
**Parameters**{.fake-h4}

`<path>|<github>|<service_url>`
    The location of the model service, to be provided in single quotes.
    This can be a local path, a GitHub SSH URI, or a URL for an existing remote service:
    `<soft>...</soft>from '/path/to/service'`
    `<soft>...</soft>from 'git@github.com:acceleratedscience/generation_inference_service.git'`
    `<soft>...</soft>from remote '0.0.0.0:8080'` <soft>// Note: 'remote' is required for cataloging a remote service</soft>

`<service_name>`
    How you will be refering to the service when using it. Keep it short, e.g. `prop` for a service that calculates properties.
    Single quotes are optional in case you want to used a space or special character.

    
**The USING Clause**{.fake-h4}

The parameters below are only needed when connecting to an IBM-hosted service (IBM partners only).

`inference-service=<string>` (required)
    The name of the inference service you want to connect to, eg. generation ot molformer.
Authorization:
    To authorize to an IBM-hosted service (IBM partners only), you have two options:
    1. `authorization='<auth_token>'`
        Provide your authorzation token directly.
        Note: to use this option, `auth_group` can not be defined.
    2. `auth_group=<auth_group_name>`
        The name of an authorization group which contains your `auth_token`.
        This is recommended if you will be using more than one model service.
        For instructions on how to set up an auth group, run `model auth add group ?`
        Note: to use this option, `authorization` can not be defined.


**Examples**{ .fake-h4 }


Catalog a model using SkyPilot deployment
```shell
catalog model service from 'git@github.com:acceleratedscience/generation_inference_service.git' as gen
```

Catalog a model using a authentication group
```shell
catalog model service from remote 'https://open.accelerate.science/proxy' as molf USING (inference-service=molformer auth_group=default)
```

Catalog a model using an authorization token
```shell
openad catalog model service from remote 'https://open.accelerate.science/proxy' as gen USING (inference-service=generation authorization='<auth_token>')
```

Catalog a remote service that was shared with you:
```shell
catalog model service from remote 'http://54.235.3.243:3001' as gen
```
</details>

<details markdown code>
<summary markdown>
model service up &lt;service_name&gt; [ no_gpu ]
</summary>
Launch a model service, after it was cataloged using `model service catalog`.

Single quotes are optional in case `service_name` contains a space or special character.

If you don't want your service to use GPU you can append the `no_gpu` clause.

**Examples**{ .fake-h4 }

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
model service local up &lt;service_name&gt; [ no_gpu ]
</summary>
Launch a model service locally.

Single quotes are optional in case `service_name` contains a space or special character.

If you don't want your service to use GPU you can append the `no_gpu` clause.

**Examples**{ .fake-h4 }

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
model service down &lt;service_name&gt;
</summary>
Deactivate a model service.

Single quotes are optional in case `service_name` contains a space or special character.

**Examples**{ .fake-h4 }

```shell
model service down gen
```
```shell
model service down 'my gen'
```
</details>

<details markdown code>
<summary markdown>
get model service &lt;service_name&gt; result '&lt;result_id&gt;'
</summary>
Retrieve a result from a model service.

This is for async inference, which will return a `<result_id>` instead of a result.
            
Single quotes are optional in case `service_name` contains a space or special character.

**Examples**{ .fake-h4 }

```shell
get model service gen result 'xyz'
```
```shell
get model service 'my gen' result 'xyz'
```
</details>

