"""
Model service demo used for tutorials and examples.

To launch:
    model service demo

Model repo:
    https://github.com/acceleratedscience/openad-service-demo
"""

import os
from typing import Any
from pydantic.v1 import Field
from openad_service_utils import (
    start_server,
    SimplePredictor,
    PredictorTypes,
    DomainSubmodule,
)


# Model imports
from rdkit import Chem


class DemoPredictor(SimplePredictor):
    """
    Return the number of atoms in a molecule.
    """

    # fmt:off
    domain: DomainSubmodule = DomainSubmodule("molecules")   # <-- edit here
    algorithm_name: str = "rdkit"                            # <-- edit here
    algorithm_application: str = "num_atoms"                 # <-- edit here
    algorithm_version: str = "v0"
    property_type: PredictorTypes = PredictorTypes.MOLECULE  # <-- edit here
    # fmt:on

    # User provided params for api / model inference
    batch_size: int = Field(description="Prediction batch size", default=128)
    workers: int = Field(description="Number of data loading workers", default=8)
    device: str = Field(description="Device to be used for inference", default="cpu")

    def setup(self):
        """Model setup. Loads the model and tokenizer, if any. Runs once.

        To wrap a model, copy and modify the standalone model setup and load
        code here. Remember to change variables to instance variables, so they
        can be used in the `predict` method.
        """
        self.model = None
        self.tokenizer = []
        self.model_path = os.path.join(self.get_model_location(), "model.ckpt")  # load model

    def predict(self, sample: Any):
        """
        Run predictions.
        """
        # -----------------------User Code goes in here------------------------
        smiles = sample
        mol = Chem.MolFromSmiles(smiles)  # pylint: disable=no-member
        num_atoms = mol.GetNumAtoms()
        result = num_atoms
        # ---------------------------------------------------------------------
        return result


# Register the class in global scope
DemoPredictor.register(no_model=True)

if __name__ == "__main__":
    # Start the server
    start_server(port=8034)
