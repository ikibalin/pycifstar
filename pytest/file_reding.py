import pycifstar

def test_answer():
    f_name = "./example_1.cif"
    global_ = pycifstar.read_star_file(f_name)
    global_ = pycifstar.read_file(f_name)
    item = global_["_cell_length_a"]
    assert item.name == "_cell_length_a"
    assert item.value == "8.56212()"
    assert item.comment == "# object Cell - Fitable"
    
    item = global_["Fe3O4_cell_length_a"]
    assert item.name == "_cell_length_a"
    assert item.value == "8.56212()"
    assert item.comment == "# object Cell - Fitable"

    items = global_["_cell_length"]
    assert len(items) == 3
    assert items.names == ("_cell_length_a", "_cell_length_b", "_cell_length_c")

    loop = global_["_atom_site"]
    assert loop.names == ("_atom_site_adp_type", "_atom_site_b_iso_or_equiv", 
        "_atom_site_fract_x", "_atom_site_fract_y", "_atom_site_fract_z", 
        "_atom_site_label", "_atom_site_occupancy", "_atom_site_type_symbol")
    
    data = global_["Fe3O4"]
    assert data.name == "Fe3O4"

    item = pycifstar.Item(name="_jh", value="sf", comment="jhklj")
    loop = pycifstar.Loop(names=("_jh_2", "_jh_zzz"), values=(("1", "2"), ("11", "22"), ("111", "222")))

    data_block = pycifstar.Data()
    data_block.add_item(item)
    data_block.add_loop(loop)

    global_["_cell_length_a"].value = 8.3
    global_["_cell_length_a"].comment = "comment line"
    print(global_)
    




