"""
transform information from data block of cif file to class CIFdata
"""
__author__="ikibalin"
__version__="28/08/2019"

from .cl_CIFvalue import str_to_comment
from .cl_CIFvalues import CIFvalues
from .cl_CIFvalue import CIFvalue
from .cl_CIFloop import CIFloop, find_name_comment_in_block


class CIFdata(object):
    """
    container for objects CIFvalues and list of CIFloop
    """

    def __init__(self, name="", values=None, loops=[], comment=""):
        self.__cif_data_name = None
        self.__cif_data_comment = None
        self.__cif_values = None
        self.__cif_loops = None
        self.name = name
        self.comment = comment
        self.values = values
        self.loops = loops

    @property    
    def name(self):
        return self.__cif_data_name
    @name.setter
    def name(self, x):
        if x is not None:
            name = str(x).strip()
        else:
            name = ""
        self.__cif_data_name = name
    @property    
    def comment(self):
        return self.__cif_data_comment
    @comment.setter
    def comment(self, x):
        comment = str_to_comment(x)
        self.__cif_data_comment = comment
    @property    
    def comments(self):
        return self.values.comment

    @property    
    def values(self):
        return self.__cif_values
    @values.setter
    def values(self, x):
        if isinstance(x, CIFvalues):
            res = x
        elif isinstance(x, str):
            cif_values = CIFvalues()
            flag = cif_values.take_from_string(x)
            if flag:
                res = cif_values
            else:
                self._show_message("Can not convert string to object 'CIFvalues'")
                res = None
        elif x is None:
            res = None
        else:
            try:
                flag_1 = isinstance(x[0], CIFvalue)
                flag_2 = isinstance(x[0], str)
            except:
                flag_1, flag_2 = False, False
            cif_values = CIFvalues()
            if flag_1:
                cif_values.values = x
                res = cif_values
            elif flag_2:
                try:
                    cif_values.values = "\n".join(x)
                    res = cif_values
                except:
                    self._show_message("Can not convert list of strings to object 'CIFvalues'")
                    res = None
            else:
                self._show_message("Can not define the type of input data to convert it to object 'CIFvalues'")
                res = None
        self.__cif_values = res

    @property    
    def loops(self):
        return self.__cif_loops
    @loops.setter
    def loops(self, l_x):
        if isinstance(l_x, CIFloop):
            l_x_in = [l_x]
        elif isinstance(l_x, str):
            l_x_in = [l_x]
        l_cif_loop = []
        for x in l_x:
            if isinstance(x, CIFloop):
                l_cif_loop.append(x)
            elif isinstance(x, str):
                cif_loop = CIFloop()
                flag_out = cif_loop.take_from_string(x)
                if flag_out:
                    l_cif_loop.append(cif_loop)
                else:
                    self._show_message("Can not convert list of strings to object 'CIFloop'")
            else:
                self._show_message("Can not define the type of input data to convert it to object 'CIFloop'")
        self.__cif_loops = l_cif_loop

    @property
    def is_values(self):
        return (self.values is not None)

    
    def is_value(self, key_):
        str_1 = delete_name_from_prefix(key_, self.name)

        flag_1 = False
        if self.is_values:
            flag_1 = self.values.is_value(str_1)
        if flag_1:
            return flag_1
        for cif_loop in self.loops:
            flag_1 = cif_loop.is_value(str_1)
            if flag_1:
                return flag_1
        return flag_1

    def is_prefix(self, key_):
        str_1 = delete_name_from_prefix(key_, self.name)

        flag_1 = False
        if self.is_values:
            flag_1 = self.values.is_prefix(str_1)
        if flag_1:
            return flag_1
        for cif_loop in self.loops:
            flag_1 = cif_loop.is_prefix(str_1)
            if flag_1:
                return flag_1
        return flag_1


    def __repr__(self):
        res = str(self)
        return res

    def __str__(self):
        ls_out = ["data_{:} {:}\n".format(self.name, self.comment)]
        ls_out.append("\n")
        if self.is_values:
            ls_out.append(str(self.values))
        for cif_loop in self.loops:
            ls_out.append("\n\n")
            ls_out.append(str(cif_loop))
        return "".join(ls_out)

    def _show_message(self, s_out: str):
        print("***  Error ***")
        print(s_out)

    def __getitem__(self, key_):
        str_1 = delete_name_from_prefix(key_, self.name)

        flag_1 = self.values.is_value(str_1)
        flag_2 = self.values.is_prefix(str_1)
        res = None
        if flag_1:
            res = self.values[str_1]
        elif flag_2:
            res = self.values.values_with_prefix(str_1)
        else:
            for cif_loop in self.loops:
                flag_1 = cif_loop.is_value(str_1)
                flag_2 = (cif_loop.prefix == str_1)
                if flag_1:
                    res = cif_loop[str_1]
                    break
                elif flag_2:
                    res = cif_loop
                    break
        if res is None:
            self._show_message("Item is not found")
        return res

    def take_from_string(self, string):
        if isinstance(string, str):
            l_string = string.split("\n")
        else:
            l_string = string

        name, comment, i_data = find_name_comment_in_block(l_string, "data_")
        self.name = name
        self.comment = comment

        flag_loop_read_name = False
        flag_loop_read_array = False
        l_string_values, l_string_loops = [], []
        l_string_loop = []
        for line in l_string[(i_data+1):]:
            str_1 = line.strip()
            cond_1 = any([str_1.lower().startswith(key_word) for key_word in ["data_", "global_"]])
            cond_2 = (str_1 == "")
            cond_3 = str_1.lower().startswith("loop_")
            cond_4 = str_1.lower().startswith("_")
            cond_5 = str_1.lower().startswith("#")
            if cond_1:
                break
            elif cond_2:
                pass
            elif cond_3:
                if l_string_loop != []:
                    l_string_loops.append("\n".join(l_string_loop))
                    l_string_loop = []
                flag_loop_read_name = True
                flag_loop_read_array = False
            elif (cond_4 | cond_5):
                if flag_loop_read_name:
                    l_string_loop.append(str_1)
                else:
                    flag_loop_read_name = False
                    flag_loop_read_array = False
                    l_string_values.append(str_1)
            else:
                if (flag_loop_read_name | flag_loop_read_array):
                    flag_loop_read_name = False
                    flag_loop_read_array = True
                    l_string_loop.append(str_1)
                else:
                    l_string_values.append(str_1)
        self.values = "\n".join(l_string_values)
        if l_string_loop != []:
            l_string_loops.append("\n".join(l_string_loop))
        if l_string_loops != []:
            self.loops = l_string_loops
        return True

def delete_name_from_prefix(key_: str, s_name: str):
    str_1 = key_.strip().lower()
    if str_1.startswith(s_name.lower()):
        str_1 = str_1[len(s_name):]
    elif str_1.startswith("_"+s_name.lower()):
        str_1 = str_1[(1+len(s_name)):]
    if not(str_1.startswith("_")):
        str_1 = "_"+str_1
    return str_1