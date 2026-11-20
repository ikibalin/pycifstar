"""Loops, block search, writing and reading back."""
import glob
import os
import re

import pytest

import pycifstar
from pycifstar.item import CIF_RESERVED, CIF_SIMPLE_VALUE, print_string
from pycifstar.loop import find_name_comment_in_block

DIR_TEST = os.path.dirname(__file__)
DIR_EXAMPLES = os.path.join(DIR_TEST, os.pardir, "examples")
FILES = sorted(glob.glob(os.path.join(DIR_TEST, "*.cif")) +
               glob.glob(os.path.join(DIR_EXAMPLES, "*.rcif")))


def read_data(text):
    data = pycifstar.Data()
    data.take_from_string(text)
    return data


def print_string_reference(str_1):
    """print_string as it was before its fast path."""
    str_2 = str_1.strip("\"").strip("'")
    if (CIF_SIMPLE_VALUE.fullmatch(str_2) is not None and
            not str_2.lower().startswith(CIF_RESERVED)):
        return str_2
    if str_2.find("\n") != -1:
        return "\n;\n{:}\n;".format(str_2)
    if re.search(r"'(\s|$)", str_2) is None:
        return "'{:}'".format(str_2)
    if re.search(r'"(\s|$)', str_2) is None:
        return '"{:}"'.format(str_2)
    return "\n;\n{:}\n;".format(str_2)


@pytest.mark.parametrize("value", [
    "1.0", "-0.25(3)", ".", "?", "abc", "a\"b", "a'b", "ab'", "ab\"", "'ab'",
    "\"ab\"", "Data_x", "DATA_x", "loop", "Loop_", "global_1", "save_a",
    "STOP_", "dataset", "_tag", "#1", "$a", "[1]", ";x", "a b", " a", "a ",
    "x' y", "it' s \"x\" y", "two\nlines", "", "''", "Fe3+", "O'Brien"])
def test_print_string_same_as_reference(value):
    assert print_string(value) == print_string_reference(value)


def test_several_rows_in_one_line():
    data = read_data("data_a\nloop_\n_s_x\n_s_y\n1 2 3 4\n5 6 7 8\n")
    loop = data.loops[0]
    assert loop["_s_x"] == ["1", "3", "5", "7"]
    assert loop["_s_y"] == ["2", "4", "6", "8"]


def test_row_over_several_lines_and_short_last_row():
    data = read_data("data_a\nloop_\n_s_x\n_s_y\n_s_z\n1\n2 3 # c1\n4 5 6\n7\n")
    loop = data.loops[0]
    assert loop.values == [["1", "2", "3"], ["4", "5", "6"], ["7", ".", "."]]
    assert loop.values_comment[0] == "# c1"


def test_loop_values_quoted_and_plain():
    data = read_data("data_a\nloop_\n_s_l\n_s_t\nA 'x y'\nB \"'z'\"\nC w\n")
    assert data.loops[0]["_s_t"] == ["x y", "z", "w"]
    data = read_data("data_a\nloop_\n_s_l\n_s_t\nA 1\nB 2 # two\n")
    assert data.loops[0].values == [["A", "1"], ["B", "2"]]
    assert data.loops[0].values_comment == ["", "# two"]


def test_loop_ends_at_tag_block_or_empty_line():
    text = ("data_a\nloop_\n_s_x\n1\n2\n\n_t_y 5\nloop_\n_u_v\n7\nDATA_b\n"
            "_w_z 8\n")
    global_ = pycifstar.Global()
    global_.take_from_string(text)
    data_a, data_b = global_.datas
    assert [loop["_s_x"] for loop in data_a.loops[:1]] == [["1", "2"]]
    assert data_a["_t_y"].value == "5"
    assert data_a.loops[1]["_u_v"] == ["7"]
    assert data_b.name == "b" and data_b["_w_z"].value == "8"


def test_find_name_comment_in_block():
    lines = ["# head", "  Data_Fe3O4  # the phase", "loop_"]
    assert find_name_comment_in_block(lines, "data") == \
        ("Fe3O4", "  # the phase", 1)
    assert find_name_comment_in_block(lines, "global_") == ("", "", -1)


def test_written_loop():
    loop = pycifstar.Loop(names=("_a_x", "_a_y"),
                          values=[["1", "a b"], ["2", "data_c"]])
    assert str(loop) == "loop_ \n_a_x  \n_a_y  \n1 'a b' \n2 'data_c' "


@pytest.mark.parametrize("f_name", FILES, ids=os.path.basename)
def test_file_is_read_back_the_same(f_name):
    global_ = pycifstar.to_global(f_name)
    text = str(global_)
    global_2 = pycifstar.Global()
    global_2.take_from_string(text)
    assert str(global_2) == text
    assert [data.name for data in global_2.datas] == \
        [data.name for data in global_.datas]
    for data, data_2 in zip(global_.datas, global_2.datas):
        assert [loop.values for loop in data.loops] == \
            [loop.values for loop in data_2.loops]
        if data.items is not None:
            assert [(item.name, item.value) for item in data.items] == \
                [(item.name, item.value) for item in data_2.items]
