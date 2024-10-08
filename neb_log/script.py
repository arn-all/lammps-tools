import numpy as np

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
