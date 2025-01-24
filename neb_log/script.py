import numpy as np
import re, yaml

def extract_neb_profile(file: str) -> np.ndarray:
    """
    Reads a LAMMPS log file and extracts the NEB profile data.

    Args:
        file (str): The path to the LAMMPS log file.

    Returns:
        np.ndarray: A 3D NumPy array of shape (n_steps, n_replica, 2) containing the NEB profile data.
            - The first dimension represents the successive steps of the NEB relaxation, i.e. essentially corresponding to the line id in the log.lammps (ignoring non-numeric lines).
            - The second dimension represents the number of replicas in the NEB calculation.
            - The third dimension represents the reaction coordinate and energy (hence 2 columns) of each replica, at each step.
    """

    data = np.genfromtxt(file, skip_header=3, invalid_raise=False)
    data = data[np.isfinite(data).any(axis=1)]                        # cleanup NaNs row from "Climbing replica = n" or incomplete
  
    num_replicas = (data.shape[1] - 9) // 2
    profiles = data[:, 9:].reshape((data.shape[0], num_replicas, 2))  # Reshape as (n_steps, n_replica, 2) 
  
    return profiles

def parse_loglammps_yaml(file: str) -> list:
    """
    Parses thermo data from a LAMMPS log file formatted with YAML output.

    This function is specifically designed to handle log files generated when the
    `thermo_modify line yaml format none` keyword is used in LAMMPS.
    
    This Python code snippet was taken from LAMMPS documentation.

    Args:
        file (str): The path to the LAMMPS log file with YAML formatted thermo data.

    Returns:
        list: A list of dictionaries, where each dictionary represents a single
              thermo data block from the log file. The structure of the dictionaries
              depends on the specific LAMMPS settings used during the simulation.
    """

    
    try:
        from yaml import CSafeLoader as Loader
    except ImportError:
        from yaml import SafeLoader as Loader

    docs = ""
    with open(file, "r") as f:
        for line in f:
            m = re.search(r"^(keywords:.*$|data:$|---$|\.\.\.$|  - \[.*\]$)", line)
            if m: docs += m.group(0) + '\n'

    thermo = list(yaml.load_all(docs, Loader=Loader))
    return thermo

def get_final_prop(file, property='TotEng'):
    """Extracts the end value of the selected property from a LAMMPS log file, for each run in the logfile.

    Args:
        file (str): Path to the LAMMPS log file.

    Returns:
        float: Final total energy.
    """
    
    import lammps
    import lammps.formats
    lf = lammps.formats.LogFile(file)
    return [r[property][-1] for r in lf.runs]
