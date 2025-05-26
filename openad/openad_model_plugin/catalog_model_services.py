import glob
import json
import os
import shlex
import shutil
import sys
import time
from functools import lru_cache
from subprocess import run
from typing import Dict, Tuple
import pandas as pd

import pyparsing as py
from openad.core.help import help_dict_create
from openad.helpers.output import output_error, output_success, output_table, output_text, output_warning
from openad.helpers.general import get_case_insensitive_key
from openad.helpers.spinner import spinner
from openad.helpers.paths import parse_path, fs_success
from openad.openad_model_plugin.auth_services import (
    load_lookup_table,
    remove_auth_group,
    remove_service_group,
    update_lookup_table,
    get_service_api_key,
    hide_api_keys,
)
from openad.openad_model_plugin.config import DISPATCHER_SERVICE_PATH, SERVICE_MODEL_PATH, SERVICES_PATH
from openad.openad_model_plugin.services import ModelService, UserProvidedConfig
from openad.openad_model_plugin.utils import bcolors, get_logger
from openad.openad_model_plugin.demo.launch_demo import launch_model_service_demo
from pandas import DataFrame
from tabulate import tabulate
from tomlkit import parse

logger = get_logger(__name__, color=bcolors.OKCYAN + bcolors.UNDERLINE)


# this is the global object that should be used across openad and testing
logger.debug("initializing global Model Service.")
Dispatcher = ModelService(location=DISPATCHER_SERVICE_PATH, update_status=True, skip_sky_validation=True)
### example of how to use the dispatcher ###
# with Dispatcher() as service:
#     print(service.list())

# Repeated clauses
CLAUSE_QUOTES_SERVICE = (
    "Single quotes are optional in case <cmd>service_name</cmd> contains a space or special character."
)
CLAUSE_QUOTES_AUTHGROUP = (
    "Single quotes are optional in case <cmd>auth_group</cmd> contains a space or special character."
)
CLAUSE_QUOTES_SERVICE_AUTHGROUP = "Single quotes are optional for both <cmd><service_name></cmd> and <cmd><auth_group></cmd> in case they contain a space or special character."
CLAUSE_GPU = "If you don't want your service to use GPU you can append the <cmd>no_gpu</cmd> clause."
ATTENTION_PROXY_URL = """<on_yellow> ATTENTION </on_yellow>
<yellow>The proxy URL used in the examples may be different for you:
- open.accelerate.science/proxy --> for most users
- <soft>xxxx</soft>.accelerate.science/proxy --> custom subdomain if your company runs its own instance</yellow>"""


def get_namespaces():
    list_of_namespaces = [
        os.path.basename(f.path) for f in os.scandir(SERVICE_MODEL_PATH) if f.is_dir()
    ]  # os.walk(SERVICE_MODEL_PATH)
    logger.debug(f"finding namespaces | {list_of_namespaces=}")
    return list_of_namespaces


@lru_cache(maxsize=16)
def get_local_service_defs(reference: str) -> list:
    """pulls the list of available service definitions. caches first result"""
    logger.debug(f"searching defs in {reference}")
    service_list = []
    service_files = glob.glob(reference + "/*.json", recursive=True)
    for file in service_files:
        with open(file, "r") as file_handle:
            try:
                jdoc = json.load(file_handle)
                service_list.append(jdoc)
            except Exception as e:
                output_error("invalid service json definition  " + file)
                output_error(e)
    return service_list


def load_service_cache() -> Dict[str, dict] | None:
    """load latest cache"""
    # TODO: implement load at beginning. need to make custom cache
    try:
        with open(os.path.join(DISPATCHER_SERVICE_PATH, "cached_service_defs.json"), "w+") as f_cached:
            logger.debug("loading service defs cache")
            return json.load(f_cached)
    except Exception as e:
        # catch all. if it fails should not stop us from proceeding
        logger.error(f"could not load service defs cache: {str(e)}")
        return None


def save_service_cache(service_definitions):
    """save latest cache"""
    try:
        with open(os.path.join(DISPATCHER_SERVICE_PATH, "cached_service_defs.json"), "w+") as f_cached:
            logger.debug("saving cache to file")
            json.dump(service_definitions, f_cached)
    except Exception as e:
        # catch all. if it fails should not stop us from proceeding
        logger.error(f"could not save service defs cache to file: {str(e)}")
        pass


def get_cataloged_service_defs() -> Dict[str, dict]:
    """Returns a dictionary of cataloged services definitions"""
    logger.debug("checking available service definitions")
    service_definitions = dict()
    # get local namespace service definitions
    # list_of_namespaces = [os.path.basename(f.path) for f in os.scandir(SERVICE_MODEL_PATH) if f.is_dir()]
    # list_of_namespaces = []
    # # iterate over local service definitions
    # for namespace in list_of_namespaces:
    #     service_list = []
    #     services_path = SERVICE_MODEL_PATH + namespace + SERVICES_PATH
    #     if os.path.exists(services_path):
    #         service_list = get_local_service_defs(services_path)
    #     else:
    #         services_path = SERVICE_MODEL_PATH + namespace + "/**" + SERVICES_PATH
    #         services_path = glob.glob(services_path, recursive=True)
    #         if len(services_path) > 0:
    #             services_path = services_path[0]
    #             service_list = get_local_service_defs(services_path)
    #     if service_list:
    #         logger.debug(f"adding local defs for | {namespace=}")
    #         service_definitions[namespace] = service_list
    # iterate over remote service definitions
    with Dispatcher() as service:
        dispatcher_services = service.list()
        # iterate over keys not used before
        for name in set(dispatcher_services):  # - set(list_of_namespaces):
            spinner.start(f"Loading definitions for {name}")
            remote_definitions = service.get_remote_service_definitions(name)
            if remote_definitions:
                logger.debug(f"adding remote service defs for | {name=}")
                service_definitions[name] = remote_definitions
            else:
                logger.warning(f"remote service defs not found, sevice not available | {name=}")
                service_definitions[name] = remote_definitions

    spinner.stop()
    return service_definitions


def get_catalog_namespaces(cmd_pointer, parser) -> Dict:
    """Get a local model catalog"""
    ns = get_namespaces()
    return output_table(DataFrame(ns), headers=["Cataloged Services"], is_data=False)


def model_service_status(cmd_pointer, parser):
    """get all services status"""
    logger.debug("listing model status")
    # get list of directory names for the catalog models
    models = {
        "Service": [],
        "Status": [],
        "Endpoint": [],
        "Host": [],
        "Auth Group": [],
        "Auth Key": [],
        "API Expires": [],
    }
    with Dispatcher(update_status=True) as service:
        # get all the services then order by name and if url exists
        all_services: list = service.list()
        # !important load services with update
        if all_services:  # proceed if any service available
            try:
                spinner.start("Checking services status")

                # No longer needed because requests have their own timeout
                # Leaving here in case there's unintended consequences.
                # # TODO: verify how much time or have a more robust method
                # time.sleep(2)  # wait for service threads to ping endpoint

                for name in all_services:
                    res = service.get_short_status(name)

                    # Add auth information
                    config = service.get_config_as_dict(name)
                    data = params = config.get("data", {}).get("data", "{}")
                    data = json.loads(data)
                    params = data.get("params", {})
                    _, auth_group = get_case_insensitive_key(params, "auth_group")
                    _, auth_key = get_case_insensitive_key(params, "authorization")
                    if auth_group:
                        models["Auth Group"].append(auth_group)
                        models["Auth Key"].append("-")
                    elif auth_key:
                        auth_key_trunc = auth_key[:6] + "..." + auth_key[-6:] if len(auth_key) > 15 else auth_key
                        models["Auth Group"].append("-")
                        models["Auth Key"].append(auth_key_trunc)
                    else:
                        models["Auth Group"].append("-")
                        models["Auth Key"].append("-")

                    # set the status of the service
                    if res.get("message"):
                        # an overwite if something occured
                        status = res.get("message")
                    elif res.get("up"):
                        status = "Ready"
                    elif res.get("url") and not res.get("is_remote"):
                        status = "Pending"
                    elif res.get("is_remote") and res.get("url"):
                        status = "Unreachable"
                    else:
                        status = "DOWN"
                    if res.get("is_remote"):
                        models["Host"].append("remote")
                        proxy_info: dict = res.get("jwt_info")
                        models["API Expires"].append(proxy_info.get("exp_formatted", "No Info"))
                    else:
                        models["Host"].append("local")
                        models["API Expires"].append("")
                    models["Service"].append(name)
                    models["Status"].append(status)
                    models["Endpoint"].append(res.get("url"))
            except Exception as e:
                # model service not cataloged or doesnt exist
                output_warning(f"Error getting status: {str(e)}")
            finally:
                spinner.stop()
    df = DataFrame(models)
    df = df.sort_values(by=["Status", "Service"], ascending=[False, True])
    return output_table(df, is_data=False)


def model_service_config(cmd_pointer, parser):
    """prints service resources"""
    logger.debug("listing service config")
    service_name = parser.as_dict()["service_name"]
    # load service status details
    with Dispatcher() as service:
        res = service.get_config_as_dict(service_name)
        config = {**res["template"]["service"], **res["template"]["resources"]}
        table_data = [[key, value] for key, value in config.items()]
    # add authentication group details
    auth_lookup_table = load_lookup_table()
    table_data.insert(0, ["authentication group", auth_lookup_table["service_table"].get(service_name, "None")])
    return DataFrame(table_data, columns=["Resource", "value"])


def retrieve_model(from_path: str, to_path: str) -> Tuple[bool, str]:
    logger.debug("retrieving service model")
    spinner.start("Retrieving model")
    # uses ssh or https
    if (from_path.startswith("git@") or from_path.startswith("https://")) and from_path.endswith(".git"):
        # test if git is available
        try:
            cmd = shlex.split("git --version")
            run(cmd, capture_output=True, text=True, check=True)
        except Exception:
            spinner.fail("git not installed or unreachable")
            spinner.stop()
            return False, "git not installed or unreachable"
        # attempt to download model using git ssh
        try:
            cmd = shlex.split(f"git clone {from_path} {to_path}")
            clone = run(cmd, capture_output=True, text=True)  # not running check=true
            assert clone.returncode == 0, clone.stderr
            spinner.info(f"successfully retrieved model {from_path}")
            spinner.stop()
            return True, ""
        except Exception as e:
            spinner.fail(f"error: {str(e)}")
            spinner.stop()
            return False, str(e)
    # uses local path
    elif os.path.exists(from_path):
        # attempt to copy model
        try:
            cmd = shlex.split(f"cp -r {from_path} {to_path}")
            cp = run(cmd, capture_output=True, text=True)
            assert cp.returncode == 0, cp.stderr
            spinner.info(f"successfully retrieved model {from_path}")
            spinner.stop()
            return True, ""
        except Exception as e:
            spinner.fail(f"failed to fetch path {from_path} >> {str(e)}")
            spinner.stop()
            return False, str(e)
    else:
        spinner.fail(f"invalid path {from_path}")
        spinner.stop()
        return False, f"invalid path {from_path}"


def load_service_config(local_service_path: str) -> UserProvidedConfig:
    """loads service params from openad.cfg file"""
    logger.debug(f"get local service configuration | {local_service_path=}")
    cfg_map = {
        "port": int,
        "replicas": int,
        "cloud": str,
        "disk_size": int,
        "cpu": str,
        "memory": str,
        "accelerators": str,
        "setup": str,
        "run": str,
    }
    if os.path.exists(os.path.join(local_service_path, "openad.cfg")):
        try:
            # open the document
            with open(os.path.join(local_service_path, "openad.cfg")) as f:
                parser = parse(f.read())
            conf = {}
            # check if [defaults] key exists if not ignore. allows for new fields in the future
            if "defaults" in parser.keys():
                parser = parser.get("defaults")
            # cast the values into a new dict
            for key, value in parser.items():
                key = key.lower()
                if value and key in cfg_map.keys():
                    conf[key] = cfg_map[key](value)  # cast the type to value
            # check if conf has any values
            if conf:
                # create a UserProvidedConfig with conf data
                spinner.info("found non defaults in openad.cfg")
                spinner.stop()
                table_data = [[key, value] for key, value in conf.items()]
                print(tabulate(table_data, headers=["Resource", "value"], tablefmt="pretty"))
                return UserProvidedConfig(**conf, workdir=local_service_path, data=json.dumps({}))
            else:
                spinner.warn("error with (openad.cfg). Could not load user config. Loading defaults.")
        except Exception as e:
            output_error(str(e))
            spinner.warn("error with (openad.cfg). Could not load user config. Loading defaults.")
            spinner.stop()
    # use default config
    return UserProvidedConfig(workdir=local_service_path, data=json.dumps({}))


def add_remote_service_from_endpoint(cmd_pointer, parser) -> bool:
    service_name = parser.as_dict()["service_name"]
    endpoint = parser.as_dict()["path"]
    logger.debug(f"add as remote service | {service_name=} {endpoint=}")
    with Dispatcher() as service:
        if service_name in service.list():
            return False
        # load remote endpoint to config custom field
        if "params" in parser:
            params = {k: v for k, v in parser.as_dict().get("params")}
            logger.debug(f"user added params: {params}")
        else:
            params = {}
        config = json.dumps(
            {
                "remote_service": True,
                "remote_endpoint": endpoint,
                "remote_status": False,
                "params": params,  # header values for request
            }
        )
        service.add_service(service_name, UserProvidedConfig(data=config))
    return True


def catalog_add_model_service(cmd_pointer, parser) -> bool:
    """Add model service repo to catalog"""

    service_name = parser.as_dict()["service_name"]
    service_path = os.path.expanduser(parser.as_dict()["path"])
    logger.debug(f"catalog model service | {service_name=} {service_path=}")
    params = {}
    if "params" in parser.as_dict():
        for i in parser.as_dict()["params"]:
            key_lower = i[0].lower()
            params[key_lower] = i[1]

    # Detect path source
    path = parser.as_dict().get("path")
    is_openbridge = path.endswith(".accelerate.science/proxy")
    auth_group = None

    # OpenBridge only
    if is_openbridge:
        # Error - Missing auth method
        if "auth_group" not in params.keys() and "authorization" not in [key.lower() for key in params.keys()]:
            return output_error(
                "The <yellow>auth_group</yellow> or <yellow>authorization</yellow> key is required to connect to the OpenAD proxy server",
                "For more info, run <cmd>catalog model ?</cmd>",
            )

        # Error - Missing inference service
        if "inference-service" not in [key.lower() for key in params.keys()]:
            return output_error(
                "The <yellow>inference-service</yellow> key is required to connect to the OpenAD proxy server",
                "For more info, run <cmd>catalog model ?</cmd>",
            )

    # Error - Conflicting auth methods
    if "auth_group" in params.keys() and "authorization" in params.keys():
        return output_error(
            "The <yellow>auth_group</yellow> and <yellow>authorization</yellow> keys can't be mixed in the same statement",
            "For more info, run <cmd>catalog model ?</cmd>",
        )

    # Parse auth group
    if "auth_group" in params.keys():
        auth_group = params["auth_group"]
        lookup_table = load_lookup_table()
        if auth_group not in lookup_table["auth_table"]:
            return output_error(
                [
                    f"Auth group '{auth_group}' does not exist",
                    "To see available auth groups, run <cmd>model auth list</cmd>",
                ],
            )

    # Remote
    if "remote" in parser:
        success = add_remote_service_from_endpoint(cmd_pointer, parser)
        if auth_group is not None:
            update_lookup_table(auth_group=auth_group, service=service_name)
        if success:
            output_success(
                f"Service <yellow>{service_name}</yellow> added to catalog from <yellow>{service_path}</yellow>",
                return_val=False,
            )
        else:
            output_error(f"A service named <yellow>{service_name}</yellow> already exists", return_val=False)

        return success

    # Local
    else:
        # Check if service exists
        with Dispatcher() as service:
            if service_name in service.list():
                return output_error(f"A service named <yellow>{service_name}</yellow> already exists")

        # Download model
        local_service_path = os.path.join(SERVICE_MODEL_PATH, service_name)
        is_local_service_path, _ = retrieve_model(service_path, local_service_path)
        if is_local_service_path is False:
            output_error(
                [f"Service <yellow>{service_name}</yellow> failed to be added", "Check path or url for typos"],
                return_val=False,
            )
            return False

        # Get any available configs from service
        config = load_service_config(local_service_path)

        # Add service
        with Dispatcher() as service:
            service.add_service(service_name, config)
            output_success(f"Service <yellow>{service_name}</yellow> added to catalog", return_val=False)

        return True


def uncatalog_model_service(cmd_pointer, parser) -> bool:
    """This function removes a catalog from the ~/.openad_model_service directory"""
    service_name = parser.as_dict()["service_name"]
    logger.debug(f"uncatalog model service | {service_name=}")
    with Dispatcher() as service:
        # check if service exists
        if service_name not in service.list():
            output_error(f"No service named <yellow>{service_name}</yellow> found in catalog", return_val=False)
            return False
        # stop running service
        start_service_shutdown(service_name)
        # remove local files for service
        if os.path.exists(os.path.join(SERVICE_MODEL_PATH, service_name)):
            shutil.rmtree(os.path.join(SERVICE_MODEL_PATH, service_name))
        # remove service from cache
    with Dispatcher() as service:  # initialize fresh load
        try:
            service.remove_service(service_name)
        except Exception as e:
            if "No such file or directory" in str(e):
                output_warning(["Trying to remove non-existing service", "Config has been deleted"], return_val=False)
                # TODO: make more robust error handling
                path = os.path.join(os.path.expanduser("~/.servicing"), f"{service_name}_service.yaml")
                open(path).close()  # create file
                service.remove_service(service_name)
            else:
                output_error([f"Failed to remove <yellow>{service_name}</yellow> service", str(e)], return_val=False)
                return False
    # remove service from authentication lookup table
    if get_service_api_key(service_name):
        remove_service_group(service_name)

    output_success(f"Service <yellow>{service_name}</yellow> removed from catalog", return_val=False)
    return True


def service_up(cmd_pointer, parser) -> bool:
    """This function synchronously starts a service"""
    gpu_disable = "no_gpu" in parser.as_dict()  # boolean flag to disable gpu
    service_name = parser.as_dict()["service_name"]
    logger.debug(f"start service | {service_name=} {gpu_disable=}")
    # spinner.start("Starting service")
    output_success("Deploying Service. Please wait...", return_val=False)
    try:
        with Dispatcher() as service:
            service.up(service_name, skip_prompt=True, gpu_disable=gpu_disable)

            # spinner.succeed(f"service ({service_name}) started")
            output_success(f"Service {service_name} is Starting.. may take some time.")
            return True
    except Exception as e:
        output_error("Service was unable to be started:\n" + str(e), return_val=False)
        return False


def local_service_up(cmd_pointer, parser) -> None:
    service_name = parser.as_dict()["service_name"]
    logger.debug(f"start service locally | {service_name=}")
    output_error(f" {service_name} Not yet implemented")


def start_service_shutdown(service_name):
    logger.debug(f"prepare service shutdown | {service_name=}")
    with Dispatcher() as service:
        if service.status(service_name).get("url") or bool(service.status(service_name).get("up")):
            # shut down service
            service.down(service_name, skip_prompt=True)
            # reinitialize service
            config = service.get_user_provided_config(service_name)
            service.remove_service(service_name)
            service.add_service(service_name, config)
            spinner.warn(f"service {service_name} is terminating.. may take some time.")
            spinner.stop()
            return True
        else:
            # output_error(
            #    f"service {service_name} was not able to terminate, please check error sky pilot to determine status and force shutdown",
            #    return_val=False,
            # )
            return False


def service_down(cmd_pointer, parser) -> None:
    """This function synchronously shuts down a service"""
    is_success = False
    try:
        service_name = parser.as_dict()["service_name"]
        logger.debug(f"attempt to stop service | {service_name=}")
        spinner.start(f"terminating {service_name} service")
        if not start_service_shutdown(service_name):
            spinner.info(f"service {service_name} is not up")
            # output_warning(f"service {service_name} is not up")
            is_success = True
    except Exception as e:
        output_error(str(e))
    finally:
        spinner.stop()
    return is_success


def get_service_endpoint(service_name) -> str | None:
    """gets the service endpoint for a given service, if endpoint is not available it returns None"""
    if service_name is None:
        # may in future return a default local service
        return None
    with Dispatcher() as service:
        endpoint = service.get_url(service_name)
    logger.debug(f"get service endpoint | {service_name=} {endpoint=}")
    return endpoint


def get_service_requester(service_name) -> str | None:
    """gets the service request params for a given service, if endpoint is not available it returns None"""
    if service_name is None:
        # may in future return a default local service
        return None
    with Dispatcher() as service:
        status = service.get_short_status(service_name)
        spinner.stop()  # Spinner may be started from within get_short_status -> maybe_refresh_auth
        endpoint = service.get_url(service_name)
        return {"func": service.service_request, "status": status, "endpoint": endpoint}


# @@
def add_service_auth_group(cmd_pointer, parser):
    """Create an authentication group"""
    auth_group = parser.as_dict()["auth_group"]
    api_key = parser.as_dict()["api_key"]
    logger.debug(f"adding auth group | {auth_group=} {api_key=}")
    lookup_table = load_lookup_table()
    if auth_group in lookup_table["auth_table"]:
        return output_error(f"authentication group '{auth_group}' already exists")
    updated_lookup_table = update_lookup_table(auth_group=auth_group, api_key=api_key)
    output_success(f"successfully added authentication group '{auth_group}'")
    hide_api_keys(updated_lookup_table)
    return DataFrame(updated_lookup_table["auth_table"].items(), columns=["auth group", "api key"])


def remove_service_auth_group(cmd_pointer, parser):
    """remove an authentication group"""
    auth_group = parser.as_dict()["auth_group"]
    logger.debug(f"removing auth group | {auth_group=}")
    lookup_table = load_lookup_table()
    if auth_group not in lookup_table["auth_table"]:
        return output_error(f"authentication group '{auth_group}' does not exists")
    updated_lookup_table = remove_auth_group(auth_group)
    output_success(f"removed authentication group '{auth_group}'")
    hide_api_keys(updated_lookup_table)
    return DataFrame(updated_lookup_table["auth_table"].items(), columns=["auth group", "api key"])


def attach_service_auth_group(cmd_pointer, parser):
    """add a model service to an authentication group"""
    service_name = parser.as_dict()["service_name"]
    auth_group = parser.as_dict()["auth_group"]
    logger.debug(f"attaching auth group to service | {service_name=} {auth_group=}")
    lookup_table = load_lookup_table()
    # connect mapping to service from auth group
    with Dispatcher() as dispatch:
        models = dispatch.list()
        if service_name not in models:
            return output_error(f"service '{service_name}' does not exist")
        if auth_group not in lookup_table["auth_table"]:
            return output_error(f"auth group '{auth_group}' does not exist")
    # add auth to service
    updated_lookup_table = update_lookup_table(auth_group=auth_group, service=service_name)
    hide_api_keys(updated_lookup_table)
    return DataFrame(updated_lookup_table["service_table"].items(), columns=["service", "auth group"])


def detach_service_auth_group(cmd_pointer, parser):
    """remove a model service from an authentication group"""
    service_name = parser.as_dict()["service_name"]
    logger.debug(f"detaching auth group from service | {service_name=}")
    lookup_table = load_lookup_table()
    if service_name not in lookup_table["service_table"]:
        return output_error(f"service '{service_name}' does not have an authentication group")
    updated_lookup_table = remove_service_group(service_name)
    hide_api_keys(updated_lookup_table)
    return DataFrame(updated_lookup_table["service_table"].items(), columns=["service", "auth group"])


def list_auth_services(cmd_pointer, parser):
    """list authentication groups and services that use it"""
    # Extracting the data from the dictionary
    lookup_table = load_lookup_table(hide_api=True)
    services = []
    auth_groups = []
    apis = []
    # Extract services and their corresponding auth groups
    for service, auth_group in lookup_table["service_table"].items():
        services.append(service)
        auth_groups.append(auth_group)
        apis.append(lookup_table["auth_table"].get(auth_group))
    # Add auth groups from auth_table that are not in service_table
    for auth_group, api in lookup_table["auth_table"].items():
        if auth_group not in auth_groups:
            services.append(None)
            auth_groups.append(auth_group)
            apis.append(api)
    # Creating the DataFrame
    df = DataFrame({"auth group": auth_groups, "service": services, "api key": apis})
    return output_table(df, is_data=False)


def get_model_service_result(cmd_pointer, parser):
    # with Dispatcher as servicer:
    #    service_status = servicer.get_short_status(parser.to_dict()["service_name"].lower())
    try:
        # response = Dispatcher.service_request(
        #     name=service_name, method="POST", timeout=None, verify=not service_status.get("is_remote"), _json=a_request
        # )
        a_request = {"url": parser.as_dict()["request_id"], "service_type": "get_result"}
        response = Dispatcher.service_request(
            name=parser.as_dict()["service_name"].lower(), method="POST", timeout=None, verify=False, _json=a_request
        )
        # response = requests.post(Endpoint + "/service", json=a_request, headers=headers, verify=False)
    except Exception as e:
        output_error(str(e))
        return output_error("Error: \n Server not reachable at ")

    try:
        response_result = response.json()
        try:
            if isinstance(response_result, str):
                response_result = json.loads(response_result)
            if isinstance(response_result, dict):
                if "warning" in response_result:
                    return output_warning(response_result["warning"]["reason"])
                elif "error" in response_result:
                    run_error = "Request Error:\n"

                    for key, value in response_result["error"].items():
                        value = str(value).replace("<", "`<")
                        value = str(value).replace(">", ">`")
                        run_error = run_error + f"- <cmd>{key}</cmd> : {value}\n  "
                    return output_error(run_error)
                if "detail" in response_result:
                    return output_warning(response_result["detail"])

            result = pd.DataFrame(response_result)

            # TODO / Dead code: there is no "save_as" or "result_file" in the parser
            if "save_as" in parser:
                filename = str(parser["results_file"])
                file_path = parse_path(cmd_pointer, filename, force_ext="csv")
                result.to_csv(file_path, index=False)
                fs_success(cmd_pointer, filename, file_path, "Result")

        except Exception as e:
            print(e)
            result = response_result

        if isinstance(result, dict):
            if "error" in result:
                run_error = "Request Error:\n"
                for key, value in result["error"].items():
                    run_error = run_error + f"- <cmd>{key}</cmd> : {value}\n  "
                return output_text(run_error)

    except Exception as e:
        run_error = "HTTP Request Error:\n"

        return output_error(run_error + "\n" + str(e))

    return result


def model_service_demo(cmd_pointer, parser):
    """
    Spin up the model service demo in a subprocess.
    """
    restart = "restart" in parser.as_dict()
    debug = "debug" in parser.as_dict()

    return launch_model_service_demo(restart=restart, debug=debug)


def service_catalog_grammar(statements: list, help: list):
    """This function creates the required grammar for managing cataloging services and model up or down"""
    logger.debug("catalog model service grammer")
    catalog = py.CaselessKeyword("catalog")
    uncatalog = py.CaselessKeyword("uncatalog")
    model = py.CaselessKeyword("model")
    up = py.CaselessKeyword("up")
    local = py.CaselessKeyword("local")
    down = py.CaselessKeyword("down")
    service = py.CaselessKeyword("service")
    status = py.CaselessKeyword("status")
    refresh = py.CaselessKeyword("refresh")
    fr_om = py.CaselessKeyword("from")
    _list = py.CaselessKeyword("list")
    quoted_string = py.QuotedString("'", escQuote="\\")

    auth_group = quoted_string | py.Word(py.alphanums + "_")
    service_name = quoted_string | py.Word(py.alphanums + "_")

    a_s = py.CaselessKeyword("as")
    describe = py.CaselessKeyword("describe")
    remote = py.CaselessKeyword("remote")
    auth = py.CaselessKeyword("auth")
    group = py.CaselessKeyword("group")
    _with = py.CaselessKeyword("with")
    add = py.CaselessKeyword("add")
    create = py.CaselessKeyword("create")
    remove = py.CaselessKeyword("remove")
    to = py.CaselessKeyword("to")

    # catalog service
    using_keyword = py.CaselessKeyword("USING").suppress()
    quoted_identifier = py.QuotedString("'", escChar="\\", unquoteResults=True)
    parameter = py.Word(py.alphas, py.alphanums + "-_") | quoted_identifier
    value = py.Word(py.alphanums + "-_") | quoted_identifier
    param_value_pair = py.Group(parameter + py.Suppress("=") + value)
    using_clause = py.Optional(
        using_keyword + py.Suppress("(") + py.Optional(py.OneOrMore(param_value_pair))("params") + py.Suppress(")")
    )

    # ---
    # Model auth list
    statements.append(py.Forward(model + auth + _list)("list_auth_services"))
    help.append(
        help_dict_create(
            name="model auth list",
            category="Model",
            command="model auth list",
            description="List authentication groups that have been created.",
        )
    )

    # ---
    # Model auth create group
    # Consistent command - to be swapped:
    # statements.append(
    #     py.Forward(model + auth + create + group + auth_group("auth_group") + _with + quoted_string("api_key"))(
    #         "add_service_auth_group"
    #     )
    # )
    # Inconsistent comand:
    statements.append(
        py.Forward(model + auth + add + group + auth_group("auth_group") + _with + quoted_string("api_key"))(
            "add_service_auth_group"
        )
    )
    help.append(
        help_dict_create(
            name="model auth create group",
            category="Model",
            # command="model auth create group <auth_group> with '<auth_token>'", # Consistent - to be swapped
            command="model auth add group <auth_group> with '<auth_token>'",  # Inconsistent
            description=f"""Create a new authentication group for model services to use.

Single quotes are required for your <cmd><auth_token></cmd> but optional for <cmd><auth_group></cmd> in case it contains a space or special character.

Authorization is required to connect to IBM-hosted models (IBM partners only). Using an auth group allows you to authorize multiple models at once, and is the recommended authorization method.

<h1>Example</h1>

{ATTENTION_PROXY_URL}

1. Copy your authentication token from the OpenAD portal:
   - <link>open.accelerate.science</link> for most users
   - <link><soft>xxxx</soft>.accelerate.science</link> custom subdomain if your company runs its own instance
2. Create an auth group, e.g. 'default':
   <cmd>model auth add group default with '<auth_token>'</cmd>
3. Catalog your services with the auth_group provided:
   <cmd>model service catalog from remote 'https://open.accelerate.science/proxy' as gen using (inference-service=generation auth_group=default)</cmd>

You can also add a cataloged model to a group after you've created it:
<cmd>model auth add service gen to group default</cmd>
""",
        )
    )

    # ---
    # Model auth remove group
    statements.append(py.Forward(model + auth + remove + group + auth_group("auth_group"))("remove_service_auth_group"))
    help.append(
        help_dict_create(
            name="model auth remove group",
            category="Model",
            command="model auth remove group <auth_group>",
            description=f"""Remove an authentication group.

{CLAUSE_QUOTES_AUTHGROUP}

Examples:
<cmd>model auth remove group default</cmd>
<cmd>model auth remove group 'my group'</cmd>
""",
        )
    )

    # ---
    # Model auth add service to group
    statements.append(
        py.Forward(model + auth + add + service + service_name("service_name") + to + group + auth_group("auth_group"))(
            "attach_service_auth_group"
        )
    )
    help.append(
        help_dict_create(
            name="model auth add service",
            category="Model",
            command="model auth add service <service_name> to group <auth_group>",
            description=f"""Ad a model service to an authentication group.

{CLAUSE_QUOTES_SERVICE_AUTHGROUP}

Examples:
- <cmd>model auth add service molf to group default</cmd>
- <cmd>model auth add service 'my molf' to group 'my group'</cmd>
""",
        )
    )

    # ---
    # Model auth remove
    statements.append(
        py.Forward(model + auth + remove + service + service_name("service_name"))("detach_service_auth_group")
    )
    help.append(
        help_dict_create(
            name="model auth remove service",
            category="Model",
            command="model auth remove service <service_name>",
            description=f"""Detach a model service from an authentication group.

{CLAUSE_QUOTES_SERVICE}

Examples:
- <cmd>model auth remove service molf</cmd>
- <cmd>model auth remove service 'my molf'</cmd>""",
        )
    )

    # ---
    # Model catalog status
    # Consistent command - to be swapped:
    # statements.append(py.Forward(model + catalog + status)("model_service_status"))
    # Inconsistent command:
    statements.append(py.Forward(model + service + status)("model_service_status"))
    help.append(
        help_dict_create(
            name="model service status",
            category="Model",
            # command="model catalog status", # Consistent - to be swapped
            command="model service status",  # Inconsistent
            description="Get the status of your currently cataloged services.",
        )
    )

    # ---
    # Refresh model service status
    statements.append(py.Forward(model + service + refresh)("model_service_refresh"))
    help.append(
        help_dict_create(
            name="model service refresh",
            category="Model",
            command="model service refresh",
            description="Refresh the grammar definitions. Use this when the grammar for a service is missing.",
        )
    )

    # ---
    # Model service describe
    statements.append(py.Forward(model + service + describe + (service_name)("service_name"))("model_service_config"))
    help.append(
        help_dict_create(
            name="model service describe",
            category="Model",
            command="model service describe <service_name>",
            description=f"""Get a service's configuration details.

{CLAUSE_QUOTES_SERVICE}

Examples:
- <cmd>model service describe gen</cmd>
- <cmd>model service describe 'my gen'</cmd>
""",
        )
    )

    # ---
    # Model catalog list
    statements.append(py.Forward(model + catalog + _list)("get_catalog_namespaces"))
    help.append(
        help_dict_create(
            name="model catalog list",
            category="Model",
            command="model catalog list",
            description="List your currently cataloged services.",
        )
    )

    # ---
    # Model service uncatalog
    # Consistent command - to be swapped:
    # statements.append(py.Forward(model + service + uncatalog + service_name("service_name"))("uncatalog_model_service"))
    # Iconsistent command:
    statements.append(py.Forward(uncatalog + model + service + service_name("service_name"))("uncatalog_model_service"))
    help.append(
        help_dict_create(
            name="model service uncatalog",
            category="Model",
            # command="model service uncatalog <service_name>", # Consistent - to be swapped
            command="uncatalog model service <service_name>",  # Inconsistent
            description=f"""Uncatalog a model service.

{CLAUSE_QUOTES_SERVICE}

Examples:
- <cmd>uncatalog model service 'gen'</cmd>
- <cmd>uncatalog model service 'my gen'</cmd>
""",
        )
    )

    # ---
    # Model service catalog
    # Consistent command - to be swapped:
    # statements.append(
    #     py.Forward(
    #         model
    #         + service
    #         + catalog
    #         + fr_om
    #         + py.Optional(remote("remote"))
    #         + quoted_string("path")
    #         + a_s
    #         + (quoted_string | py.Word(py.alphanums + "_"))("service_name")
    #         + using_clause
    #     )("catalog_add_model_service")
    # )
    # Inconsistent command:
    statements.append(
        py.Forward(
            catalog
            + model
            + service
            + fr_om
            + py.Optional(remote("remote"))
            + quoted_string("path")
            + a_s
            + (quoted_string | py.Word(py.alphanums + "_"))("service_name")
            + using_clause
        )("catalog_add_model_service")
    )
    help.append(
        help_dict_create(
            name="catalog model service",
            category="Model",
            # command="model service catalog from [ remote ] '<path>|<github>|<service_url>' as <service_name> USING (<parameter>=<value> <parameter>=<value>)", # Consistent - to be swapped
            command="catalog model service from [ remote ] '<path>|<github>|<service_url>' as <service_name> USING (<parameter>=<value> <parameter>=<value>)",  # Inconsistent
            description=f"""Catalog a model service from a local path, from GitHub or from an hosted service URL.

Use the <cmd>remote</cmd> clause when cataloging from a hosted service URL.

            
<h1>Parameters</h1>

<cmd><path>|<github>|<service_url></cmd>
    The location of the model service, to be provided in single quotes.
    This can be a local path, a GitHub SSH URI, or a URL for an existing remote service:
    <cmd><soft>...</soft>from '/path/to/service'</cmd>
    <cmd><soft>...</soft>from 'git@github.com:acceleratedscience/openad-service-gen.git'</cmd>
    <cmd><soft>...</soft>from remote '0.0.0.0:8080'</cmd> <soft>// Note: 'remote' is required for cataloging a remote service</soft>

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


<h1>Examples</h1>

{ATTENTION_PROXY_URL}

- Catalog a model using SkyPilot deployment
<cmd>catalog model service from 'git@github.com:acceleratedscience/openad-service-gen.git' as gen</cmd>

- Catalog a model using a authentication group
<cmd>catalog model service from remote 'https://open.accelerate.science/proxy' as molf USING (inference-service=molformer auth_group=default)</cmd>

- Catalog a model using an authorization token
<cmd>openad catalog model service from remote 'https://open.accelerate.science/proxy' as gen USING (inference-service=generation authorization='<auth_token>')</cmd>

- Catalog a remote service that was shared with you:
<cmd>catalog model service from remote 'http://54.235.3.243:3001' as gen</cmd>""",
        )
    )

    # ---
    # Model service up
    statements.append(
        py.Forward(
            model + service + up + service_name("service_name") + py.Optional(py.CaselessKeyword("NO_GPU")("no_gpu"))
        )("service_up")
    )
    help.append(
        help_dict_create(
            name="Model up",
            category="Model",
            command="model service up <service_name> [ no_gpu ]",
            description=f"""Launch a model service, after it was cataloged using <cmd>model service catalog</cmd>.

{CLAUSE_QUOTES_SERVICE}

{CLAUSE_GPU}

Examples:
- <cmd>model service up gen</cmd>
- <cmd>model service up 'my gen'</cmd>
- <cmd>model service up gen no_gpu</cmd>""",
        )
    )

    # ---
    # Model service local up
    statements.append(
        py.Forward(
            model
            + service
            + local
            + up
            + service_name("service_name")
            + py.Optional(py.CaselessKeyword("NO_GPU")("no_gpu"))
        )("local_service_up")
    )
    help.append(
        help_dict_create(
            name="Model local up",
            category="Model",
            command="model service local up <service_name> [ no_gpu ]",
            description=f"""Launch a model service locally.

{CLAUSE_QUOTES_SERVICE}

{CLAUSE_GPU}

Example:
- <cmd> model service local up gen</cmd>
- <cmd> model service local up 'my gen'</cmd>
- <cmd> model service local up gen no_gpu</cmd>
""",
        )
    )

    # ---
    # Model service down
    statements.append(py.Forward(model + service + down + service_name("service_name"))("service_down"))
    help.append(
        help_dict_create(
            name="model down",
            category="Model",
            command="model service down <service_name>",
            description=f"""Deactivate a model service.

{CLAUSE_QUOTES_SERVICE}

Examples:
- <cmd>model service down gen</cmd>
- <cmd>model service down 'my gen'</cmd>
""",
        )
    )

    # ---
    # Model service get result
    # Consistent command - to be swapped:
    # statements.append(
    #     py.Forward(
    #         model
    #         + service
    #         + py.CaselessKeyword("get")
    #         + py.CaselessKeyword("result")
    #         + service_name("service_name")
    #         + quoted_string("request_id")
    #     )("get_model_service_result")
    # )
    # Inconsistent command:
    statements.append(
        py.Forward(
            py.CaselessKeyword("get")
            + model
            + service
            + service_name("service_name")
            + py.CaselessKeyword("result")
            + quoted_string("request_id")
        )("get_model_service_result")
    )
    help.append(
        help_dict_create(
            name="model service result",
            category="Model",
            # command="model service get result <service_name> '<result_id>'", # Consistent - to be swapped
            command="get model service <service_name> result '<result_id>'",  # Inconsistent
            description=f"""Retrieve a result from a model service.

This is for async inference, which will return a <cmd><result_id></cmd> instead of a result.
            
{CLAUSE_QUOTES_SERVICE}

Examples:
- <cmd>get model service gen result 'xyz'</cmd>
- <cmd>get model service 'my gen' result 'xyz'</cmd>
""",
        )
    )

    # ---
    # Model service demo
    statements.append(
        py.Forward(
            model
            + service
            + py.CaselessKeyword("demo")
            + py.Optional(py.CaselessKeyword("restart")("restart") | py.CaselessKeyword("debug")("debug"))
        )("model_service_demo")
    )
    help.append(
        help_dict_create(
            name="model service demo",
            category="Model",
            command="model service demo",
            description="""Launch a demo service to learn about the OpenAD model service.

Before you can run the demo service, you'll need to install the service tools:
<cmd>pip install git+https://github.com/acceleratedscience/openad_service_utils.git@0.3.1</cmd>

Further instructions are provided once the service is launched.
It will shut down automatically when OpenAD is terminated.

Optional clauses:
<cmd>restart</cmd>
    Reboot the service
<cmd>debug</cmd>
    Display the logs from the subprocess

Examples:
- <cmd>model service demo</cmd>
- <cmd>model service demo restart</cmd>
- <cmd>model service demo debug</cmd>
""",
        )
    )
