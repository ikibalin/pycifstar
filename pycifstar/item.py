"""
transform information from one variable of .cif file to Item
"""
__author__="ikibalin"
__version__="2019/09/12"

import re

# A value of a CIF line: a quoted string (its quote closes only before a
# blank or the end of the line, so "O'Brien" and 'A #1' stay one value), a
# comment from a '#' that starts a value to the end of the line, or a run
# of non-blank characters ('a#b' is a value, not a value and a comment).
CIF_TOKEN = re.compile(
    r"""'(?:[^']|'(?=\S))*'(?=\s|$)|"(?:[^"]|"(?=\S))*"(?=\s|$)|#.*|\S+""")
# a value written without quotes
CIF_SIMPLE_VALUE = re.compile(r"""[^\s_#$'"\[\];][^\s]*""")
CIF_RESERVED = ("data_", "loop_", "global_", "save_", "stop_")



class Item(object):
    """
    class to store one line from .star, .cif
    """

    def __init__(self, name=None, value=None, comment=""):
        self.__name = None
        self.__value = None
        self.__comment = None
        self.name = name
        self.value = value
        self.comment = comment

    @property    
    def name(self):
        return self.__name
    @name.setter
    def name(self, x):
        if x is not None:
            cif_name = str(x).strip().lower()
            if not(cif_name.startswith("_")):
                cif_name = "_"+cif_name
        else:
            cif_name = None
        self.__name = cif_name

    @property    
    def tag(self):
        return self.name
    @tag.setter
    def tag(self, x):
        self.name = x


    @property    
    def value(self):
        return self.__value
    @value.setter
    def value(self, x):
        if x is not None:
            self.__value = str(x).strip().strip("\"").strip("'")
        else:
            self.__value = None
    @property    
    def comment(self):
        return self.__comment
    @comment.setter
    def comment(self, x):
        comment = str_to_comment(x)
        self.__comment = comment
    def __float__(self):
        return float(self.value)


    def __repr__(self):
        res = str(self)
        return res

    def __str__(self):
        if self.is_defined:
            if self.is_comment:
                comment = self.comment
            else:
                comment= ""
            if self.is_value_lines:
                ls_out = ["{:} {:}".format(self.name, comment)]
                ls_out.append("\n;\n")
                ls_out.append(self.value)
                ls_out.append("\n;")
            else:
                ls_out = ["{:} {:}".format(self.name, print_string(self.value))]
                ls_out.append(" {:}".format(comment))
            return "".join(ls_out)
        return "Item is not defined"

    @property
    def is_defined(self):
        cond = ((self.name is not None) & (self.value is not None))
        return cond
    @property
    def is_value_lines(self):
        cond = len(self.value.split("\n")) > 1
        return cond
    @property
    def is_comment(self):
        cond = (self.comment is not None)
        return cond


    def take_from_string(self, string):
        is_strings = len(string.strip().split("\n")) > 1
        if is_strings:
            first_string = string.strip().split("\n")[0]
        else:
            first_string = string

        l_value, comment, ind_1 = split_values_comment(first_string)
        self.comment = comment
        str_1 = first_string[:ind_1].strip()

        if len(l_value) == 0:
            self._show_message("Undefined format for string\n")
            return False

        self.name = l_value[0]
        if not(is_strings):
            if len(l_value) == 1:
                self.value = "."
            elif len(l_value) == 2:
                self.value = l_value[1]
            else:  # several words without quotes: one value, as before
                self.value = str_1[len(l_value[0]):].strip().strip("\"").strip("'")
            return True
        else:
            l_string = string.strip().split("\n")
            str_1 = l_string[1].strip()
            if str_1.startswith(";"):
                l_help = [i_line+2 for i_line, line in enumerate(l_string[2:]) if line.strip().startswith(";")]
                if len(l_help) > 0:
                    value = str_1.lstrip(";")+"\n"+"\n".join(l_string[2:l_help[0]])
                else:
                    value = str_1.lstrip(";")+"\n"+"\n".join(l_string[2:])
                self.value = value
                return True
            else:
                self._show_message("Can not find ';' for multistring variable")
                return False
        return True

    def _show_message(self, s_out: str):
        print("***  Error ***")
        print(s_out)

    def to_file(self, f_name):
        with open(f_name, "w") as fid:
            fid.write(str(self))


def split_values_comment(line: str):
    """Values and comment of a line of a CIF file.

    Returns the values (without their quotes), the comment (from '#', ''
    when there is none) and the index where the comment starts (the length
    of the line when there is none). A '#' inside a quoted value or inside
    a word is a part of the value.
    """
    l_value = []
    for match in CIF_TOKEN.finditer(line):
        token = match.group(0)
        first = token[0]
        if first == "#":
            return l_value, token, match.start()
        if first in "'\"":
            if len(token) > 1 and token[-1] == first:
                token = token[1:-1]
            else:  # a quote that is not closed: dropped as before
                token = token.strip("'\"")
        l_value.append(token)
    return l_value, "", len(line)


def print_string(str_1):
    str_2 = str_1.strip("\"").strip("'")
    if (CIF_SIMPLE_VALUE.fullmatch(str_2) is not None and
            not str_2.lower().startswith(CIF_RESERVED)):
        return str_2
    if str_2.find("\n") != -1:
        return "\n;\n{:}\n;".format(str_2)
    # a quote closes the value only before a blank: choose the one that
    # does not appear so in the text
    if re.search(r"'(\s|$)", str_2) is None:
        return "'{:}'".format(str_2)
    if re.search(r'"(\s|$)', str_2) is None:
        return '"{:}"'.format(str_2)
    return "\n;\n{:}\n;".format(str_2)


def str_to_comment(x):
    if x is not None:
        ind = str(x).find("#")
        if ind == -1:
            comment = str(x)
        else:
            comment = str(x).strip()
    else:
        comment = ""
    if (comment != "")&(not(comment.startswith("#"))):
        comment = "#"+comment
    return comment
