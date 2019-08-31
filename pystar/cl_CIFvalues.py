"""
container of CIFvalue
"""
__author__="ikibalin"
__version__="28/08/2019"

from .cl_CIFvalue import CIFvalue, str_to_comment

class CIFvalues(object):
    """
    container for objects CIFvalue
    """

    def __init__(self, values=[], comment=""):
        self.__cif_values = None
        self.__comment = None
        self.comment = comment
        self.values = values

    @property    
    def values(self):
        return self.__cif_values
    @values.setter
    def values(self, l_x):
        l_res = []
        try:
            if isinstance(l_x, str):
                l_x_in = [l_x]
            else:
                _ = [x for x in l_x]
                l_x_in = l_x
        except:
            l_x_in = [l_x]
        for x in l_x_in:
            if isinstance(x, CIFvalue):
                l_res.append(x)
            else:
                cif_value = CIFvalue()
                flag_out = cif_value.take_from_string(str(x))
                if flag_out:
                    l_res.append(cif_value)
        self.__cif_values = l_res
    @property    
    def comment(self):
        return self.__comment
    @comment.setter
    def comment(self, x):
        if isinstance(x, str):
            x_in = str_to_comment(x)
        else:
            x_in = str("\n".join([str_to_comment(hh) for hh in x]))
        self.__comment = x_in

    @property    
    def names(self):
        return [hh.name for hh in self.values]
    def __repr__(self):
        res = str(self)
        return res

    def __str__(self):
        if self.is_defined:
            ls_out = [self.comment]
            ls_out.extend([str(cif_value) for cif_value in self.values])
            return "\n".join(ls_out)
        return "The object 'CIFvalues' is not defined"

    @property
    def is_defined(self):
        cond = (self.values is not None)
        return cond

    def is_value(self, key_):
        str_1 = key_.strip().lower()
        if not(str_1.startswith("_")):
            str_1 = "_"+str_1
        l_name = [hh.name for hh in self.values]
        cond = (str_1 in l_name)
        return cond

    def is_prefix(self, key_):
        str_1 = key_.strip().lower()
        if not(str_1.startswith("_")):
            str_1 = "_"+str_1
        l_res = self.values_with_prefix(str_1)
        cond = (len(l_res) > 0)
        return cond


    def __getitem__(self, key_):
        res = None
        str_1 = key_.lower().strip()
        if not(str_1.startswith("_")):
            str_1 = "_"+str_1
        for cif_value in self.values:
            if cif_value.name == str_1:
                res = cif_value
                break
        l_res = self.values_with_prefix(str_1)
        if ((res is None) & (len(l_res) > 0)):
            res = l_res
        elif (res is None):
            self._show_message("Name '{:}' is not found".format(key_))
        return res

    def values_with_prefix(self, s_type: str):
        str_1 = s_type.lower().strip()
        if not(str_1.startswith("_")):
            str_1 = "_"+str_1
        l_res = []
        l_type = str_1.split("_")
        len_l_type = len(l_type)
        for cif_value in self.values:
            l_type_name = cif_value.name.split("_")
            if len_l_type <= len(l_type_name):
                flag = all([hh_1 == hh_2 for hh_1, hh_2 in zip(l_type, l_type_name[:len_l_type])])
                if flag:
                    l_res.append(cif_value)
        return l_res

    def take_from_string(self, string):
        if isinstance(string, str):
            l_string_in = string.split("\n")
        else:
            l_string_in = string
        l_value_string, l_comment = [], []
        s_val = []
        flag_in = False
        for i_line, line in enumerate(l_string_in):
            if line.strip().startswith(";"):
                s_val.append(line.strip())
                flag_in = not(flag_in)
            elif line.strip().startswith("#"):
                if flag_in:
                    s_val.append(line.strip())
                else:
                    l_comment.append(line.strip())
            elif line.strip().startswith("_"):
                if flag_in:
                    s_val.append(line.strip())
                else:
                    if s_val != []:
                        l_value_string.append("\n".join(s_val))
                    s_val = [line.strip()]
            elif flag_in:
                s_val.append(line.strip())
        if s_val != []:
            l_value_string.append("\n".join(s_val))
        self.comment = "\n".join(l_comment)
        self.values = l_value_string
        return True

    def _show_message(self, s_out: str):
        print("***  Error ***")
        print(s_out)

