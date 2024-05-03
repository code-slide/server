#
# api.codeslide.net
# 
# @license
# Forked from mydraft.cc by Sebastian Stehle
# Copyright (c) Do Duc Quan. All rights reserved.
# 

import pytest
from parse import get_script, embed_script, set_frame, parse_frames

def test_get_script():
    """
    Test get_script function
    """
    # Passed, with Python code
    script = "<Python>print('Hello, World!')\nprint('Hi')"
    expected_code = "print('Hello, World!')\nprint('Hi')"
    expected_script = ""
    actual_code, actual_script = get_script(script)
    
    assert actual_code == expected_code
    assert actual_script == expected_script

    # Passed, with Python code and other script
    script = "<1> Object1 \n <Python>print('Hello, World!')"
    expected_code = "print('Hello, World!')"
    expected_script = "<1> Object1"
    actual_code, actual_script = get_script(script)
    
    assert actual_code == expected_code
    assert actual_script == expected_script

    # Passed, with Python code and assignment
    script = "<1> Object1 = {'TEXT': '<Hello, World!>'} \n <Python>print('Hello, World!')"
    expected_code = "print('Hello, World!')"
    expected_script = "<1> Object1 = {'TEXT': '<Hello, World!>'}"
    actual_code, actual_script = get_script(script)
    
    assert actual_code == expected_code
    assert actual_script == expected_script

    # Passed, with no Python code
    script = "<1> Object1"
    expected_code = ""
    expected_script = "<1> Object1"
    actual_code, actual_script = get_script(script)
    
    assert actual_code == expected_code
    assert actual_script == expected_script

def test_embed_script():
    """
    Test embed_script function
    """
    # Passed, with Python code
    script = "<Python> print('<1,2> Object1')"
    expected_output = "<1,2> Object1\n"
    actual_output = embed_script(script)
    
    assert actual_output == expected_output

    # Passed, with Python code and assignment
    script = "<Python> a = 1 \nprint(f'<1> Object{a}')"
    expected_output = "<1> Object1\n"
    actual_output = embed_script(script)
    
    assert actual_output == expected_output

    # Passed, with no code
    script = ""
    expected_output = ""
    actual_output = embed_script(script)
    
    assert actual_output == expected_output

    # Passed, with no Python tag
    script = "print('<1> Object1')"
    expected_output = "print('<1> Object1')"
    actual_output = embed_script(script)
    
    assert actual_output == expected_output

    # Failed, with incomplete Python code
    script = "<Python> print('Hello, World!'"
    with pytest.raises(SyntaxError):
        embed_script(script)

    # Failed, with incorrect spacing in Python code
    script = "<Python> print('Hello, World!')\n    print('Hi')"
    with pytest.raises(SyntaxError):
        embed_script(script)

    # Failed, with non-included library import
    script = "<Python> import pandas as pd \nprint(pd.DataFrame([1, 2, 3]))"
    with pytest.raises(ModuleNotFoundError):
        embed_script(script)

def test_set_frame():
    """
    Test set_frame function
    """
    # Passed, with no objects
    frames = [[]]
    indexes = [1, 2]
    eofs = []
    objects = []
    expected_frames = [[], []]
    actual_frames = set_frame(frames, indexes, eofs, objects)
    
    assert actual_frames == expected_frames

    # Passed, with objects
    frames = [[]]
    indexes = [1, 2]
    eofs = []
    objects = ["Object1", "Object2"]
    expected_frames = [["Object1", "Object2"], ["Object1", "Object2"]]
    actual_frames = set_frame(frames, indexes, eofs, objects)
    
    assert actual_frames == expected_frames

    # Passed, with infinite objects
    frames = [[], ["Object1"]]
    indexes = [3]
    eofs = ["Object1"]
    objects = ["Object2"]
    expected_frames = [[], ["Object1"], ["Object1", "Object2"]]
    actual_frames = set_frame(frames, indexes, eofs, objects)
    
    assert actual_frames == expected_frames

def test_parse_frames():
    """
    Test parse_frames function
    """
    # Passed, with no syntax
    script = "<Python>print('<1> Object1')"
    expected_frames = [["Object1"]]
    actual_frames = parse_frames(script)
    
    assert actual_frames == expected_frames

    # Passed, with multiple items 
    script = "<Python>print('<1> Object1, Object2')"
    expected_frames = [["Object1", "Object2"]]
    actual_frames = parse_frames(script)
    
    assert actual_frames == expected_frames

    # Passed, with from-to syntax
    script = "<1-3> Object1 \n <Python>print('<2-4> Object2')"
    expected_frames = [["Object1"], ["Object1", "Object2"], ["Object1", "Object2"], ["Object2"]]
    actual_frames = parse_frames(script)
    
    assert actual_frames == expected_frames

    # Passed, with multi syntax
    script = "<1,3,5> Object1 \n <Python>print('<2,4,6> Object2')"
    expected_frames = [["Object1"], ["Object2"], ["Object1"], ["Object2"], ["Object1"], ["Object2"]]
    actual_frames = parse_frames(script)
    
    assert actual_frames == expected_frames

    # Passed, with single infinity syntax (1)
    script = "<3-> Object1 \n <Python>print('<4> Object2')"
    expected_frames = [[], [], ["Object1"], ["Object1", "Object2"]]
    actual_frames = parse_frames(script)
    
    assert actual_frames == expected_frames

    # Passed, with single infinity syntax (2)
    script = "<4> Object2 \n <Python>print('<3-> Object1')"
    expected_frames = [[], [], ["Object1"], ["Object2", "Object1"]]
    actual_frames = parse_frames(script)
    
    assert actual_frames == expected_frames

    # Passed, with multiple infinity syntax (1)
    script = "<3-> Object1 \n <Python>print('<4-> Object2')"
    expected_frames = [[], [], ["Object1"], ["Object1", "Object2"]]
    actual_frames = parse_frames(script)
    
    assert actual_frames == expected_frames

    # Passed, with multiple infinity syntax (2)
    script = "<4-> Object2 \n <Python>print('<3-> Object1')"
    expected_frames = [[], [], ["Object1"], ["Object2", "Object1"]]
    actual_frames = parse_frames(script)
    
    assert actual_frames == expected_frames

    # Passed, with assignment (1)
    script = "<1> Object2 \n <Python>print('<2> Object1 = {\"TEXT\": \"Hello, world!\"}')"
    expected_frames = [["Object2"], ["Object1={\"TEXT\": \"Hello, world!\"}"]]
    actual_frames = parse_frames(script)
    
    assert actual_frames == expected_frames

    # Passed, with assignment (2)
    script = "<2> Object1 = {\"TEXT\": \"Hello, world!\"} \n <Python>print('<1> Object2')"
    expected_frames = [["Object2"], ["Object1={\"TEXT\": \"Hello, world!\"}"]]
    actual_frames = parse_frames(script)
    
    assert actual_frames == expected_frames

    # Passed, with overriding (1)
    script = "<1> Object1 \n <Python>print('<1> Object1 = {\"TEXT\": \"Hello, world!\"}')"
    expected_frames = [["Object1", "Object1={\"TEXT\": \"Hello, world!\"}"]]
    actual_frames = parse_frames(script)
    
    assert actual_frames == expected_frames

    # Passed, with overriding (2)
    script = "<1> Object1 = {\"TEXT\": \"Hello, world!\"} \n <Python>print('<1> Object1')"
    expected_frames = [["Object1={\"TEXT\": \"Hello, world!\"}", "Object1"]]
    actual_frames = parse_frames(script)
    
    assert actual_frames == expected_frames

    # Passed, with multi syntax including from-to (1)
    script = "<1,3-4> Object1 \n <Python>print('<2,5-6> Object2')"
    expected_frames = [["Object1"], ["Object2"], ["Object1"], ["Object1"], ["Object2"], ["Object2"]]
    actual_frames = parse_frames(script)
    
    assert actual_frames == expected_frames

    # Passed, with multi syntax including from-to (2)
    script = "<3-4,1> Object1 \n <Python>print('<5-6,2> Object2')"
    expected_frames = [["Object1"], ["Object2"], ["Object1"], ["Object1"], ["Object2"], ["Object2"]]
    actual_frames = parse_frames(script)
    
    assert actual_frames == expected_frames

    # Passed, with multi syntax including infinite (1)
    script = "<1,3-> Object1 \n <Python>print('<2,4-> Object2')"
    expected_frames = [["Object1"], ["Object2"], ["Object1"], ["Object1", "Object2"]]
    actual_frames = parse_frames(script)

    assert actual_frames == expected_frames

    # Passed, with multi syntax including infinite (2)
    script = "<3-,1> Object1 \n <Python>print('<4-,2> Object2')"
    expected_frames = [["Object1"], ["Object2"], ["Object1"], ["Object1", "Object2"]]
    actual_frames = parse_frames(script)

    # Passed, with multi syntax including both infinite & from-to (1)
    script = "<1-2,3-> Object1 \n <Python>print('<2-3,4-> Object2')"
    expected_frames = [["Object1"], ["Object1", "Object2"], ["Object1", "Object2"], ["Object1", "Object2"]]
    actual_frames = parse_frames(script)

    assert actual_frames == expected_frames

    # Passed, with multi syntax including both infinite & from-to (2)
    script = "<3-,1-2> Object1 \n <Python>print('<4-,2-3> Object2')"
    expected_frames = [["Object1"], ["Object1", "Object2"], ["Object1", "Object2"], ["Object1", "Object2"]]
    actual_frames = parse_frames(script)

    assert actual_frames == expected_frames

    # Failed, with syntax after python tag
    script = "<1-> Object1 \n <Python>print('<2> Object2') \n <2> Object2"
    with pytest.raises(Exception):
        parse_frames(script)

    # Failed, with unknown variable
    script = "<1-> Object1 \n <Python>print(<2> Object2)"
    with pytest.raises(Exception):
        parse_frames(script)