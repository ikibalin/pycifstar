"""
transform information from global block of cif file to class CIFglobal
"""
__author__="ikibalin"
__version__="29/08/2019"

from .cl_CIFvalue import str_to_comment
from .cl_CIFvalues import CIFvalues
from .cl_CIFvalue import CIFvalue
from .cl_CIFloop import CIFloop, find_name_comment_in_block
from .cl_CIFdata import CIFdata, delete_name_from_prefix


class CIFglobal(object):
    """
    container for objects CIFvalues, list of CIFloop and CIFdata
    """

    def __init__(self, name="", values=None, loops=[], datas=[], comment=""):
        self.__cif_global_name = None
        self.__cif_global_comment = None
        self.__cif_values = None
        self.__cif_loops = None
        self.__cif_datas = None
        self.name = name
        self.comment = comment
        self.values = values
        self.loops = loops
        self.datas = datas

    @property    
    def name(self):
        return self.__cif_data_name
    @name.setter
    def name(self, x):
        if x is not None:
            name = str(x).strip()
        else:
            name = ""
        self.__cif_global_name = name
    @property    
    def name(self):
        return self.__cif_global_name
    @name.setter
    def name(self, x):
        if x is not None:
            name = str(x).strip()
        else:
            name = ""
        self.__cif_global_name = name
    @property    
    def comment(self):
        return self.__cif_global_comment
    @comment.setter
    def comment(self, x):
        comment = str_to_comment(x)
        self.__cif_global_comment = comment
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
    def datas(self):
        return self.__cif_datas
    @datas.setter
    def datas(self, l_x):
        if isinstance(l_x, CIFdata):
            l_x_in = [l_x]
        elif isinstance(l_x, str):
            l_x_in = [l_x]
        l_cif_data = []
        for x in l_x:
            if isinstance(x, CIFdata):
                l_cif_data.append(x)
            elif isinstance(x, str):
                cif_data = CIFdata()
                flag_out = cif_data.take_from_string(x)
                if flag_out:
                    l_cif_data.append(cif_data)
                else:
                    self._show_message("Can not convert list of strings to object 'CIFdata'")
            else:
                self._show_message("Can not define the type of input data to convert it to object 'CIFdata'")
        self.__cif_datas = l_cif_data


    @property
    def is_values(self):
        return (self.values is not None)

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
        for cif_data in self.datas:
            ls_out.append("\n\n")
            ls_out.append(str(cif_data))
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
        if res is None:
            for cif_loop in self.loops:
                flag_1 = cif_loop.is_value(str_1)
                flag_2 = cif_loop.is_prefix(str_1)
                if flag_1:
                    res = cif_loop[str_1]
                    break
                elif flag_2:
                    res = cif_loop
                    break
        if res is None:
            for cif_data in self.datas:
                flag_1 = cif_data.is_value(str_1)
                flag_2 = cif_data.is_prefix(str_1)
                if (flag_1 | flag_2):
                    res = cif_data[str_1]
                    break
        if res is None:
            self._show_message("Item is not found")
        return res

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
        for cif_data in self.datas:
            flag_1 = cif_data.is_value(str_1)
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
        for cif_data in self.datas:
            flag_1 = cif_data.is_prefix(str_1)
            if flag_1:
                return flag_1
        return flag_1



    def take_from_string(self, string):
        if isinstance(string, str):
            l_string = string.split("\n")
        else:
            l_string = string

        name, comment, i_global = find_name_comment_in_block(l_string, "global_")
        self.name = name
        self.comment = comment

        flag_loop_read_name = False
        flag_loop_read_array = False
        flag_data_read = False
        l_string_values, l_string_loops = [], []
        l_string_loop = []
        i_data = -1
        for i_line, line in enumerate(l_string[(i_global+1):]):
            str_1 = line.strip()
            cond_1 = any([str_1.lower().startswith(key_word) for key_word in ["data_", "global_"]])
            cond_2 = (str_1 == "")
            cond_3 = str_1.lower().startswith("loop_")
            cond_4 = str_1.lower().startswith("_")
            cond_5 = str_1.lower().startswith("#")
            if cond_1:
                if str_1.lower().startswith("data_"):
                    i_data = i_line+i_global+1
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

        if (i_data != -1):
            l_string_datas, l_string_data = [], []
            for line in l_string[i_data:]:
                str_1 = line.strip()
                cond_1 = str_1.lower().startswith("global_")
                cond_2 = str_1.lower().startswith("data_") 
                if cond_1:
                    break
                elif cond_2:
                    if l_string_data != []:
                        l_string_datas.append("\n".join(l_string_data))
                    l_string_data = [str_1]
                else:
                    l_string_data.append(str_1)

            if l_string_data != []:
                l_string_datas.append("\n".join(l_string_data))
            if l_string_datas != []:
                self.datas = l_string_datas

        return True
