import argparse 
import glob 
from pathlib import Path 
import ase.io 
import numpy as np 
from tqdm import tqdm 
from animation import animate_progress 
 
def create_pos(in_file, out_file): 
    system = ase.io.read(in_file, format="lammps-data", style="atomic") 
    values = np.hstack([system.arrays["id"].reshape(-1, 1), system.positions]) 
    np.savetxt(out_file, 
               values, 
               fmt=['%d', '%.18e', '%.18e', '%.18e'], 
               comments='', 
               header=str(values.shape[0])) 
 
@animate_progress 
def convert_single_file(input_file, output_file, force): 
    input_path = Path(input_file) 
    output_path = Path(output_file) 
    if not force:
        if output_path.exists():
            raise FileExistsError("Use the --force option to override.")
    create_pos(input_path, output_path) 
    print(f'\nSuccessfully created {output_path}') 
 
def convert_multiple_files(glob_pattern, suffix, append_suffix, force): 
    input_files = glob.glob(glob_pattern) 
 
    for input_file in tqdm(input_files, desc='Converting Files', unit='file'): 
        input_path = Path(input_file) 
 
        if append_suffix:
            output_path = Path( str(input_path) + f'.{suffix}') 
        else: 
            if suffix[0] != ".":
                suffix = "." + suffix
            output_path = input_path.with_suffix(suffix) 
 
        # Check if the output file already exists or is the same as the input file 
        if not force:
            if output_path.exists() or output_path == input_path: 
                print(f'Skipping {input_path} to prevent overwriting input or existing output file.') 
                continue 
 
        create_pos(input_path, output_path) 
 
    print(f'Successfully converted {len(input_files)} files') 
 
if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Convert LAMMPS data files to POS format.') 
    parser.add_argument('input', help='Input file for single conversion or glob pattern for multiple files') 
    parser.add_argument('output', nargs='?', help='Output file for single conversion') 
    parser.add_argument('--suffix', '-s', default='pos', help='Suffix for output files in case of multiple file conversion') 
    parser.add_argument('--append-suffix', '-a', action='store_true', help='Append the suffix instead of replacing it') 
    parser.add_argument('--force', '-f', action='store_true', help='Allow overriding existing files. Default is to skip those cases.') 
 
    args = parser.parse_args() 
 
    if not "*" in args.input: 
        convert_single_file(args.input, args.output, force) 
    else:
        convert_multiple_files(args.input, args.suffix, args.append_suffix, args.force) 
