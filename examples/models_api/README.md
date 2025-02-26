# Beginners Guide to using OpenAD model inference API

## What Does OpenAD Model Service Do?

OpenAD model inference API enables you to run model inference as a service
(IaaS). Public models are available to anyone by connecting to OpenAD model
service with an api key. Private models can also be hosted by the service so you
can run inference without installing Python packages locally, downloading model
checkpoints, and other technical details.

In short, OpenAD model service gives you these benefits:

- Eliminate the need to run inference locally.
- Easily deploy ML models as a service.
- Integrate an ML model so you can use it directly in the OpenAD Toolkit CLI and notebooks.
- Don't worry about infrastructure; just focus on making and using models.

## Getting Started With OpenAD Model Service

To run inference with OpenAD model service, you need to create an account and
generate an access token. First you need an IBMid.

### 1. Create Account

1. To create an IBMid, all you need is an email address. Instructions are
[here](https://www.ibm.com/docs/en/ibmid?topic=introduction).  

2. To create an OpenAD account, login with your IBMid at
https://open.accelerate.science/  

    The first time you login it will say, _Your account is pending to be added to a
    group._  
    
    <img src="/assets/proxy/openad-portal.png" width="600" title="/assets/proxy/openad-portal.png" alt="OpenAD Portal"/>

3. Logout and email your group admin (if you have one),
or email us at  
[openad.toolkit@ibm.com](mailto:openad.toolkit@ibm.com). A system administrator
will add you to a group.

4. After you receive confirmation, login again. It should display your _group_
and your _role_ in that group, group admin or user. Congratulations! This is
confirmation you have an account on OpenAD, and you are logged in to OpenAD
portal.

_[Email us](mailto:openad.toolkit@ibm.com) again if you have any problems or
concerns about your account or access to the portal._

### 2. Generate Access Token

Once you are logged in to OpenAD portal, select the **Access Token** tab.

If it says, _You do not have a token yet,_ click **Generate Token**.
The token is a long sequence of random-seeming letters and numbers.

To copy the token, click anywhere on it. Then paste it wherever you need to
enter the token. _Guard this token like you would guard your username/password.
It grants the same access to the system._

### 3. Connect The Model

*IMPORATANT: Default inference url to our gateway is `https://open.accelerate.science/proxy`*

#### Example connecting to the `molformer` model:

Install OpenAD Toolkit, if not already installed, then run it.
```shell
pip install openad

openad
```

Add your token as a resuable authentication group.
```shell
>> model auth add group default with '<access_token>'
```

Add the inference model using your authentication group.
```shell
>> catalog model service from remote 'https://open.accelerate.science/proxy' as 'molformer' USING (auth_group=default Inference-Service=molformer)
```

### Lets break this command down
> for a more detailed information run the command `catalog ?`

#### `catalog model service from remote`
Connect to model from url

#### `'https://open.accelerate.science/proxy'`
Endpoint for model inference

#### `'molformer'`
Any name you want to give this service

#### `USING (auth_group=default ...)` 
The authentication group name for api access

#### `USING (... Inference-Service=molformer)` 
The model subscription name (check your dashboard for available models)

### Check Model Connection

The service should show as Connected
```shell
>>  model service status

Service    Status     Endpoint                               Host    Token Expires
---------  ---------  -------------------------------------  ------  -----------------
molformer  Connected  https://open.accelerate.science/proxy  remote  Wed Sep  11, 2030
```

Get more information about this model.
```shell
>>  molformer ?

Commands starting with "molformer"
- molformer get molecule property molformer_classification for [<list of SMILES>] | <SMILES>   USING (<parameter>=<value> <parameter>=<value>) (save_as '<filename.csv>')
- molformer get molecule property molformer_multitask_classification for [<list of SMILES>] | <SMILES>   USING (<parameter>=<value> <parameter>=<value>) (save_as '<filename.csv>')
- molformer get molecule property molformer_regression for [<list of SMILES>] | <SMILES>   USING (<parameter>=<value> <parameter>=<value>) (save_as '<filename.csv>')
```

### 4. Run Inference

Run the following command to get a classification result
```shell
>>  molformer get molecule property molformer_classification for 'OC12COC3=NCC1C23'
✔ Request Returned

subject           property                  result
----------------  ------------------------  --------
OC12COC3=NCC1C23  molformer_classification  [1]
```
