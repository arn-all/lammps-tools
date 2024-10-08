## LAMMPS Log Parsing Utilities

This directory provides utility functions for parsing data from LAMMPS log files:

* `extract_neb_profile(file)`: Extracts NEB profile data from LAMMPS log files.
* `parse_loglammps_yaml(file)`: Parses thermo data from LAMMPS log files formatted with YAML output.

**Example:**

```python
import numpy as np

neb_profile = extract_neb_profile("neb.lammps")
number_of_steps = neb_profile.shape[0]

thermo_data = parse_loglammps_yaml("lammps_thermo.log")
first_data_block = thermo_data[0]
step = first_data_block["Step"]
```
