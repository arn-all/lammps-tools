## LAMMPS Log Parsing Utilities

This directory provides utility functions for parsing data from LAMMPS log files:

* `extract_neb_profile(file)`: Extracts NEB profile data from LAMMPS log files.
* `parse_loglammps_yaml(file)`: Parses thermo data from LAMMPS log files formatted with YAML output. This function is specifically designed to handle log files generated when the
    `thermo_modify line yaml format none` keyword is used in LAMMPS.
* `get_final_prop(file, property)`: Extract the final value of some property from a logfile. A list is returned as the logfile may contain several runs. Useful to follow the evolution of a property along a (relaxed) NEB barrier.


**Example:**

```python
import numpy as np

neb_profile = extract_neb_profile("neb.lammps")
number_of_steps = neb_profile.shape[0]

thermo_data = parse_loglammps_yaml("lammps_thermo.log")
first_data_block = thermo_data[0]
step = first_data_block["Step"]
```
