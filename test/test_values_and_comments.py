"""Values, quotes and comments of CIF lines (CIF 1.1 syntax, section 2.2.7:
a quote closes a value only before a blank, '#' starts a comment only at
the start of a value)."""
import pycifstar
from pycifstar.item import print_string, split_values_comment
from pycifstar.loop import smart_split


def read_data(text):
    data = pycifstar.Data()
    data.take_from_string(text)
    return data


def test_hash_inside_quotes_is_a_value():
    data = read_data("data_a\n_x_title \"A B #1 C\"\n_x_name 'D #2' # comment\n_x_y 1\n")
    assert data["_x_title"].value == "A B #1 C"
    assert data["_x_name"].value == "D #2"
    assert data["_x_name"].comment == "# comment"
    assert data["_x_y"].value == "1"


def test_hash_inside_word_and_comment_of_loop():
    data = read_data("data_a\nloop_\n_s_label\n_s_text\nA1 'x #1'  # first\nB2 c#d\n")
    loop = data.loops[0]
    assert loop["_s_text"] == ["x #1", "c#d"]
    assert loop.values_comment[0] == "# first"


def test_split_with_tabs_and_apostrophe():
    assert smart_split("Fe1\tFe\t0.5  0.25") == ["Fe1", "Fe", "0.5", "0.25"]
    assert smart_split("1 O'Brien 'it''s' 'a b'") == ["1", "O'Brien", "it''s", "a b"]
    assert split_values_comment("a 'b c' # rest 'x'") == (["a", "b c"], "# rest 'x'", 8)
    assert smart_split("C C 0.0033 'International Tables Vol C'") == \
        ["C", "C", "0.0033", "International Tables Vol C"]


def test_written_values_are_read_back():
    for value in ("1.25(3)", "a b", "A B #1 C", "#13744", "_tag_like", "loop_x",
                  "O'Brien", "it' s \"x\" y", "[1,2]", "two\nlines"):
        text = print_string(value)
        if text.startswith("\n;"):  # a text field: not read in loops yet
            assert "\n" in value or ("' " in value and '" ' in value)
            if "\n" in value:
                continue
        else:
            data = read_data(f"data_a\nloop_\n_s_v\n_s_w\n{text:} end\n")
            assert data.loops[0]["_s_v"] == [value], (value, text)
        data = read_data(f"data_a\n_s_v {text:}\n_s_w 1\n")
        assert data["_s_v"].value == value, (value, text)


def test_tag_itself_is_found_before_prefix():
    items = read_data("data_a\n_cell 1\n_cell_length_a 2\n").items
    assert items["_cell"].value == "1"
    assert len(items["_cell_length"]) == 1
