from .cl_CIFvalue import CIFvalue
from .cl_CIFvalues import CIFvalues
from .cl_CIFloop import CIFloop
from .cl_CIFdata import CIFdata
from .cl_CIFglobal import CIFglobal


def to_global(f_name):
    fid = open(f_name, "r")
    string = fid.read()
    fid.close()
    cif_global = CIFglobal()
    flag = cif_global.take_from_string(string)
    if not flag:
        print("Error at file reading")
    return cif_global

def to_data(f_name):
    fid = open(f_name, "r")
    string = fid.read()
    fid.close()
    cif_data = CIFdata()
    flag = cif_data.take_from_string(string)
    if not flag:
        print("Error at file reading")
    return cif_data

def to_loop(f_name):
    fid = open(f_name, "r")
    string = fid.read()
    fid.close()
    cif_loop = CIFloop()
    flag = cif_loop.take_from_string(string)
    if not flag:
        print("Error at file reading")
    return cif_loop

def to_values(f_name):
    fid = open(f_name, "r")
    string = fid.read()
    fid.close()
    cif_values = CIFvalues()
    flag = cif_values.take_from_string(string)
    if not flag:
        print("Error at file reading")
    return cif_values
