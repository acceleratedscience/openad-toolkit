# Beginners Guide to OpenAD Model Inference API

## What is OpenAD Model Service?

The OpenAD model inference API provides **inference as a service (IaaS)**, allowing you to run machine learning models without the technical overhead. It offers:

- **Public models**: Available to anyone with an API key.
- **Private models**: Host your own models on the service.
- **Simplified workflow**: No need for local Python packages or model checkpoint downloads

### Key Benefits  

   ✅ Run inference in the cloud instead of locally.  
   ✅ Deploy ML models as services with minimal setup.  
   ✅ Seamless integration with OpenAD Toolkit CLI and notebooks.  
   ✅ Focus on using models, not managing infrastructure.  

## Getting Started: Step-by-Step Guide

### Step 1: Create an Account

1. **Create an IBMid** (if you don't already have one)  
   Visit [IBM's registration page](https://www.ibm.com/docs/en/ibmid?topic=introduction).  
   You only need an email address to register.  

2. **Create an OpenAD Account**  
   Go to [https://open.accelerate.science/](https://open.accelerate.science/).  
   Log in with your IBMid.  
   You'll see, _"Your account is pending to be added to a group"_.  

   <img src="/assets/proxy/openad-portal.png" width="600" title="/assets/proxy/openad-portal.png" alt="OpenAD Portal"/>

3. **Request Group Assignment**  
   Log out and contact your group administrator.  
   If you don't have a group admin, email [openad.toolkit@ibm.com](mailto:openad.toolkit@ibm.com).  
   A system administrator will add you to an appropriate group.  

4. **Verify Account Setup**  
   Log in again after receiving confirmation.  
   Verify your _group_ and _role_ are displayed.  
   This confirms you have an active OpenAD account.  

> **Need Help?** Contact [openad.toolkit@ibm.com](mailto:openad.toolkit@ibm.com) for account or access issues.

### Step 2: Generate an Access Token

1. Log in to the OpenAD portal.
2. Navigate to the **Access Token** tab.
3. If you see _"You do not have a token yet"_, click **Generate Token**.
4. Click anywhere on the token to copy it.

> **Security Warning**: Treat this token like a password. It grants full access to the system under your credentials.

### Step 3: Connect to a Model

**Default Inference URL**: `https://open.accelerate.science/proxy`

#### Installation and Setup

```shell
# Install OpenAD Toolkit (if not already installed)
pip install openad

# Launch OpenAD
openad
```

#### Configure Authentication

```shell
# Add your token as a reusable authentication group
>> model auth add group default with 'YOUR_ACCESS_TOKEN'
```

#### Connect to a Model (Example: Molformer)

```shell
>> catalog model service from remote 'https://open.accelerate.science/proxy' as 'molformer' USING (auth_group=default Inference-Service=molformer)
```

#### Understanding the Connection Command

| Command Component | Description |
|-------------------|-------------|
| `catalog model service from remote` | Connects to a model via URL |
| `'https://open.accelerate.science/proxy'` | The endpoint for model inference |
| `'molformer'` | Your chosen name for this service |
| `USING (auth_group=default ...)` | References your authentication group |
| `USING (... Inference-Service=molformer)` | The model subscription name |

> **Note**: Check your dashboard for available model subscriptions.

### Step 4: Verify the Connection

```shell
>> model service status
```

Expected output:

```text
Service    Status     Endpoint                               Host    Token Expires
---------  ---------  -------------------------------------  ------  -----------------
molformer  Connected  https://open.accelerate.science/proxy  remote  Wed Sep 11, 2030
```

### Step 5: Explore Available Model Functions

```shell
>> molformer ?
```

You'll see available commands for the model:

```text
Commands starting with "molformer"
- molformer get molecule property molformer_classification for [<list of SMILES>] | <SMILES> USING (<parameter>=<value> <parameter>=<value>) (save_as '<filename.csv>')
- molformer get molecule property molformer_multitask_classification for [<list of SMILES>] | <SMILES> USING (<parameter>=<value> <parameter>=<value>) (save_as '<filename.csv>')
- molformer get molecule property molformer_regression for [<list of SMILES>] | <SMILES> USING (<parameter>=<value> <parameter>=<value>) (save_as '<filename.csv>')
```

### Step 6: Run Model Inference

```shell
>> molformer get molecule property molformer_classification for 'OC12COC3=NCC1C23'
```

Expected output:

```text
✔ Request Returned

subject           property                  result
----------------  ------------------------  --------
OC12COC3=NCC1C23  molformer_classification  [1]
```

## Troubleshooting

- **Connection Issues**: Verify your token has not expired and the inference URL is correct
- **Authentication Errors**: Regenerate your token if necessary
- **Model Not Available**: Check your dashboard for available model subscriptions
- **Command Syntax Errors**: Use the `?` command to verify proper syntax

## Best Practices

- Store important results using the `save_as` parameter in commands
- Use descriptive service names when connecting to models
- Organize multiple models and authentication groups logically
- Back up your access token securely

---

For more detailed information on all commands, run `catalog ?` in the OpenAD CLI.
