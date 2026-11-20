"""Write what CrysPy and pycifstar make of the CIF files of a folder.

    python cryspy_to_cif.py <folder> <out.json>

For every .rcif and .cif file of the folder: str() of pycifstar.to_global
and CrysPy's load_file(...).to_cif() (or the error). Two runs (with two
versions of pycifstar) are compared by compare_to_cif.py; CrysPy reads
its files by pycifstar, so its output must not change.
Run it with PYTHONHASHSEED=0: CrysPy writes some unknown categories in
the order of a set.
"""
import contextlib
import glob
import io
import json
import os
import sys
import warnings

import cryspy
import pycifstar


def main(folder, f_out):
    files = sorted(glob.glob(os.path.join(folder, "**", "*.rcif"), recursive=True) +
                   glob.glob(os.path.join(folder, "**", "*.cif"), recursive=True))
    res = {}
    warnings.simplefilter("ignore")
    for f_name in files:
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                text_star = str(pycifstar.to_global(f_name))
            except Exception as error:
                text_star = f"error {type(error).__name__}: {error}"
            try:
                text_cryspy = cryspy.load_file(f_name).to_cif()
            except Exception as error:
                text_cryspy = f"error {type(error).__name__}: {error}"
        res[os.path.relpath(f_name, folder)] = {
            "pycifstar": text_star, "cryspy": text_cryspy}
    with open(f_out, "w") as fid:
        json.dump(res, fid)
    print(f"{len(files)} files written to {f_out}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
