import ase, ase.io, ase.geometry
import numpy as np

# for progressbar. Can be removed.
from tqdm import tqdm 


def mix_AB_along_axis(system_A, system_B, axis, L_A, centre_A, L_buffer=0, use_buffer=True):
    # axis = x, y or z. Combinaitions of axis not supported
    # L_A = size of the A region along axis. Constraint: L_A+2*L_buffer < L_axis
    """Mixes two atomic configurations (A and B) along a specified axis.
    This function mixes two atomic configurations (A and B) along a specified axis (x, y, or z). 
    It creates a new system with region A having positions from system_A and region B having positions taken from system_B. 
    Optionally, a buffer region can be introduced between A and B for a smoother transition.
    
    This procedure allows the creation of a kink-pair that is accurate enough to serve as an initial guess for NEB.

    Args:
        system_A: An ASE Atoms object representing system A.
        system_B: An ASE Atoms object representing system B.
        axis: The axis for mixing ("x", "y", or "z").
        L_A: Size of region A along the specified axis.
        centre_A: Centre of region A along the specified axis.
        L_buffer: Size of the buffer region between A and B along axis (default to 0, i.e. no buffer).
        use_buffer: Flag to indicate using the buffer region (default: True).

    Returns:
        An ASE Atoms object representing the mixed system.
    """


    allowed_axis_values = ["x", "y", "z"]
    axis_n = allowed_axis_values.index(axis)
    cell_length = system_A.cell.cellpar()[axis_n]


    if cell_length-2*L_buffer-L_A < 0:
        if cell_length-L_A <= 0:
            L_A = cell_length
            L_buffer = 0
            use_buffer = False
            print("Cell is smaller than L_A. Setting L_A = cell_length and disabling buffer.")
        else:
            L_buffer = max(0, cell_length-L_A)/2
            print("Cell is too small, reducing buffer to (cell_length-L_A)/2")

    # assert cell_length-2*L_buffer-L_A >= 0, f"L_A + 2*L_buffer = {L_A + 2*L_buffer:.3f}, exceeding cell dimension along axis {axis} = {cell_length:.3f}"
    assert np.allclose(system_A.get_cell(), system_B.get_cell()), "Cells should be identical"

    mixed_system = system_B.copy()

    def disp(sys_a, sys_b):
        # displacement with minimum image convention
        return ase.geometry.find_mic(sys_a.positions-sys_b.positions, cell=sys_a.get_cell(), pbc=True)[0]
    
    d_AB = disp(system_A, system_B)

    # atoms of zone A
    mask_A = np.abs(mixed_system.positions - centre_A)[:, axis_n] <= L_A/2
    mixed_system.positions[mask_A] += d_AB[mask_A]

    if use_buffer:
        # atoms of buffer
        mask_buffer = (np.abs(mixed_system.positions[:, axis_n] - centre_A)> L_A/2) & \
                    (L_A/2 + L_buffer >= np.abs(mixed_system.positions[:, axis_n] - centre_A))
        
        pos_of_buf_atoms = mixed_system.positions[mask_buffer][:, axis_n]

        mixed_system.positions[mask_buffer] += d_AB[mask_buffer] * (1- ((np.abs(pos_of_buf_atoms -centre_A) -L_A/2) /(L_buffer)))[:, np.newaxis]
    
    return mixed_system


def load_file(file_):
    """Loads a LAMMPS data file using ASE, sorts atoms by id and wrap pbc.
    """
    sys_ = ase.io.read(file_, style="atomic")

    # sort
    sys_ = sys_[np.argsort(sys_.arrays["id"])]

    # wrap to pbc just in case
    sys_.wrap()

    return sys_

def save_pos(out_file, system):
    """Saves the atomic positions of a system to a text file for lammps neb command.
    """
    values = np.hstack([system.arrays["id"].reshape(-1, 1), system.positions]) 
    np.savetxt(out_file, 
               values, 
               fmt=['%d', '%.18e', '%.18e', '%.18e'], 
               comments='', 
               header=str(values.shape[0])) 

def create_path(initial, final, n_steps):
    """Creates a series of LAMMPS data files representing intermediate configurations between two initial configurations.
    """
    cell_dimensions = initial.cell.cellpar()[:3]

    x = np.linspace(0, 1, n_steps)

    for i in tqdm(range(n_steps)):
        

        buf = False if i == 0 else True
        try:
            mixed_cell = mix_AB_along_axis(initial, final, 
                                axis="x", 
                                L_A=x[i]*cell_dimensions[0], 
                                centre_A=cell_dimensions[0]/2,
                                L_buffer=cell_dimensions[0]/6,
                                use_buffer=buf)
        except AssertionError:
            # try without buffer in case it doesn't fit
            mixed_cell = mix_AB_along_axis(initial, final, 
                                axis="x", 
                                L_A=x[i]*cell_dimensions[0], 
                                centre_A=cell_dimensions[0]/2,
                                L_buffer=cell_dimensions[0]/8,
                                use_buffer=False)
        ase.io.write(f"kink_pair_{i}.lammps-data", mixed_cell)
        save_pos(f"kink_pair_{i}.pos", mixed_cell)


def main():
    """This script creates a series of LAMMPS data files representing a path between two atomic configurations (i.e. dislocations in different Peierls valleys). 
    """
    sys_0 = load_file("dislo_0.lammps-data")
    sys_1 = load_file("dislo_1.lammps-data")

    if sys_0.get_global_number_of_atoms() == 2400:
        # Replicate along axis x if needed
        sys_0 *= [40, 1, 1]
        sys_1 *= [40, 1, 1]

        ase.io.write("dislo_0_40b.lammps-data", sys_0)

    create_path(sys_0, sys_1, 12)

if __name__ == "__main__":
    main()
