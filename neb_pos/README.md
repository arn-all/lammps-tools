# lmp2pos tool for NEB

Tool to convert lammps-data files (those written with the `write_data` command) to a format readable by the neb command (`neb each ... ` or `neb final ...`).


## Features

- Support for multiple files is provided in the form of glob expressions. 

- Preserves the id of atoms found in the lammps-data file.

## General Usage


To convert **one file**:

```bash
python script.py neb_step_1.lmp neb_step_1.pos
```

To convert **multiple files**, saving them to the same location, with their suffix replaced by ".pos". *Note: The quotes around the glob expression are compulsory.*

```bash
python script.py "neb_step_*.lmp"
```

## Special cases

For files ending by an id instead of a suffix, you can choose to append the suffix (provided with --suffix or .pos by default). 

For instance, 

```bash
python script.py "neb_step.*" --suffix dat --append-suffix 
```
Will save files as "neb_step.*.dat".

## Safety 

For safety, the script cannot override existing files by default. If needed, use the `--force/-f` option:

```bash
python3 script.py "test/neb_knot_file_out.*" --force -s dat
```


## Help


```
usage: script.py [-h] [--suffix SUFFIX] [--append-suffix] [--force] input [output]           
                                                                                             
Convert LAMMPS data files to POS format.                                                     
                                                                                             
positional arguments:                                                                        
  input                 Input file for single conversion or glob pattern for multiple files  
  output                Output file for single conversion                                    
                                                                                             
options:                                                                                     
  -h, --help            show this help message and exit                                      
  --suffix SUFFIX, -s SUFFIX                                                                 
                        Suffix for output files in case of multiple file conversion          
  --append-suffix, -a   Append the suffix instead of replacing it                            
  --force, -f           Allow overriding existing files. Default is to skip those cases.     

```
