# Beginners Guide to using OpenAD model inference API


## What does this service do?

OpenAD model inference API enables you to run model inference as a service (MIaaS). Public models are available to anyone by connecting to OpenAD model service with an api key. Private models can also be hosted by the service so you can run inference without installing Python packages locally, downloading model checkpoints, and other technical details.

In short, OpenAD model service gives you these benefits:
- Eliminate the need to run inference locally.
- Easily deploy ML models as a service.
- Integrate an ML model so you can use it directly in the OpenAD Toolkit CLI and notebooks.
- Don't worry about infrastructure; just focus on making and using models.

# Getting Started

### 1. Create Account
To run infere an Account using IBMidt need to create an account [here](https://open.accelerate.science/)

OpenAD,nce on OpenAD model service, you first need to create an account... Fo
For that you need an IBMid.


1. 
enlink for laterodel invferencf crea.. F
If you have any issues or inquiries please reach out to us via [phil.downey1@ibm.com](mailto:phil.downey1@ibm.com)

questionsemailatt openad.toolkit@ibm.com openad.toolkit@ibm.com### 2. Generate access token
Upon account creation you will have access to the default publicly available groups. Now you need to get your access token to use the service. Once generated copy and proceed.

![alt text](/assets/proxy/access_token.png)

### 3. Connect the Inference Model to OpenAD Toolkit

#### Example connecting to the `molformer` model:

Install OpenAD Toolkit
```shell
pip install openad
```

Start up OpenAD Toolkit.
```shell
openad
```

Add your token as a resuable authentication group.
```shell
>> model auth add group default with '<access_token>'
```

Add the inference model using your authentication group.
```shell
>> catalog model service from remote 'https://open.accelerate.science' as 'molformer' USING (auth_group=default Inference-Service=molformer)
```

### Lets break this command down
> for a more detailed information run the command `catalog ?`

#### `catalog model service from remote`
Connect to model from url

#### `'https://open.accelerate.science'`
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

Service    Status     Endpoint                          Host    Token Expires
---------  ---------  --------------------------------  ------  ----------------
molformer  Connected  https://open.accelerate.science   remote  Wed Sep  11, 2030
```

Get more information about this model.
```shell
>>  molformer ?

Commands starting with "molformer"
- molformer get molecule property molformer_classification for [<list of SMILES>] | <SMILES>   USING (<parameter>=<value> <parameter>=<value>) (save_as '<filename.csv>')
- molformer get molecule property molformer_multitask_classification for [<list of SMILES>] | <SMILES>   USING (<parameter>=<value> <parameter>=<value>) (save_as '<filename.csv>')
- molformer get molecule property molformer_regression for [<list of SMILES>] | <SMILES>   USING (<parameter>=<value> <parameter>=<value>) (save_as '<filename.csv>')
```

### Run Inference on Model

Run the following command to get a classification result
```shell
>>  molformer get molecule property molformer_classification for 'OC12COC3=NCC1C23'
✔ Request Returned

subject           property                  result
----------------  ------------------------  --------
OC12COC3=NCC1C23  molformer_classification  [1]
```
