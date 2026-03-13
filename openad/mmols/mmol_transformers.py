import copy
import gemmi
from openad.helpers.data_formats import OPENAD_MMOL_DICT
from openad.mmols.mmol_functions import parse_cif_block


def mmol2cif(mmol_dict, path=None):
    """
    Convert a macromolecule dictionary to CIF format.
    Used to store a macromolecule as a CIF file.
    """

    # Error handling
    if not mmol_dict:
        print("mmol2cif() - No mmol_dict provided")
        return None

    cif_data = None
    
    # Load the PDB data
    if mmol_dict["data3DFormat"] == "cif":
        cif_data = mmol_dict["data3D"]
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(cif_data)
    elif mmol_dict["data3DFormat"] == "pdb":
        cif_data = pdb2cif(mmol_dict["data3D"], dest_path=path)  # Will write to disk if path is set

    # Return the PDB data as a string
    return cif_data


def mmol2pdb(mmol_dict, path=None):
    """
    Convert a macromolecule dictionary to PDB format.
    Used to store a macromolecule as a PDB file.
    """

    # Error handling
    if not mmol_dict:
        print("mmol2pdb() - No mmol_dict provided")
        return None

    pdb_data = None
    
    # Load the PDB data
    if mmol_dict["data3DFormat"] == "pdb":
        pdb_data = mmol_dict["data3D"]
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(pdb_data)

    elif mmol_dict["data3DFormat"] == "cif":
        pdb_data = cif2pdb(mmol_dict["data3D"], dest_path=path)  # Will write to disk if path is set

    # Return the PDB data as a string
    return pdb_data


def pdb2cif(pdb_data=None, pdb_path=None, dest_path=None):
    """
    Convert PDB path/data to CIF format.
    
    Note: Converting PDB to CIF format may not preserve all data
    in a way that stays compatible with the Miew viewer.
    """

    # Parse the PDB string
    if pdb_data:
        structure = gemmi.read_pdb_string(pdb_data)

    # Load the PDB file
    elif pdb_path:
        structure = gemmi.read_structure(pdb_path)

    # Error handling
    else:
        print("pdb2cif() - No pdb_path or pdb_data provided")
        return None

    # See https://gemmi.readthedocs.io/en/latest/mol.html#entity
    structure.setup_entities()
    structure.assign_label_seq_id()

    # Write the CIF to disk
    if dest_path:
        structure.make_mmcif_document().write_file(dest_path)

    # Return the CIF data as a string
    else:
        return structure.make_mmcif_block()


def cif2pdb(cif_data=None, cif_path=None, dest_path=None):
    """
    Convert CIF path to PDB format.
    """

    # Parse the CIF string
    if cif_data:
        cif_doc = gemmi.cif.read_string(cif_data)
        cif_block = cif_doc.sole_block()
        structure = gemmi.make_structure_from_block(cif_block)

    # Load the CIF file
    elif cif_path:
        structure = gemmi.read_structure(cif_path)

    # Error handling
    else:
        print("cif2pdb() - No cif_data or cif_path provided")
        return None

    # Write the PDB to disk
    if dest_path:
        structure.write_pdb(dest_path)

    # Return the PDB data as a string
    else:
        return structure.make_pdb_string()


def cif2mmol(cif_data=None, cif_path=None):
    """
    Convert CIF data or file to a Moll object.

    Used for:
    - Opening a CIF file in the GUI (cif_path).
    - Opening downloaded CIF data in the GUI (cif_data).
    """

    # Parse the CIF string
    if cif_data:
        cif_doc = gemmi.cif.read_string(cif_data)

    # Load the CIF file
    elif cif_path:
        cif_doc = gemmi.cif.read_file(cif_path)
        # Read the CIF file content
        with open(cif_path, "r", encoding="utf-8") as f:
            cif_data = f.read()

    # Error handling
    else:
        print("cif2moll() - No cif_data or cif_path provided")
        return None

    # Parse the CIF data
    cif_block = cif_doc.sole_block()
    data = parse_cif_block(cif_block)

    # Create the moll object
    mmol_dict = copy.deepcopy(OPENAD_MMOL_DICT)
    mmol_dict["molType"] = "mmol"
    mmol_dict["data"] = data
    mmol_dict["data3D"] = cif_data
    mmol_dict["data3DFormat"] = "cif"

    # Return the moll object
    return mmol_dict


def pdb2mmol(pdb_data=None, pdb_path=None):
    """
    Convert PDB data or file to a Moll object.

    Used for:
    - Opening a PDB file in the GUI (pdb_path).
    - Opening downloaded PDB data in the GUI (pdb_data) **

    ** Not used because we use the CIF format when downloading
    """

    # Parse the PDB string
    if pdb_data:
        struct = gemmi.read_pdb_string(pdb_data)

    # Load the PDB file
    elif pdb_path:
        struct = gemmi.read_pdb(pdb_path)
        # Read the PDB file content
        with open(pdb_path, "r", encoding="utf-8") as f:
            pdb_data = f.read()

    # Error handling
    else:
        print("pdb2moll() - No pdb_data or pdb_path provided")
        return None

    # Parse the PDB data as CIF
    cif_doc = struct.make_mmcif_document()
    cif_block = cif_doc.sole_block()
    data = parse_cif_block(cif_block)

    # Create the moll object
    mmol_dict = copy.deepcopy(OPENAD_MMOL_DICT)
    mmol_dict["molType"] = "mmoll"
    mmol_dict["data"] = data
    mmol_dict["data3D"] = pdb_data
    mmol_dict["data3DFormat"] = "pdb"

    # Return the moll object
    return mmol_dict


