import os
import shutil
import pytest
from pandas import DataFrame
from openad.openad_model_plugin.catalog_model_services import retrieve_model, Dispatcher
from tests.helpers import random_name


@pytest.mark.parametrize(
    "from_path",
    [
        "git@github.com:acceleratedscience/openad-service-prop.git",
        "git@github.com:acceleratedscience/openad-service-gen.git",
        "https://github.com/acceleratedscience/openad-service-prop.git",
    ],
)
def test_retrieve_model(from_path):
    """test model download to direcotry using ssh and cp"""
    # setup
    local_to_path = "/tmp/" + random_name()
    # test
    is_success, err = retrieve_model(from_path, local_to_path)
    # cleanup first in case test fails
    if os.path.exists(os.path.join(local_to_path)):
        shutil.rmtree(os.path.join(local_to_path))
    # validate
    assert is_success, str(err)
