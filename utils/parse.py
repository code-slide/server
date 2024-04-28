import ast
import io
import sys

def get_script(script: str) -> tuple[str, str]:
    """
    Find the dynamic script in the input, which follows by identifier <Python>

    Params:
        script (str): input script
    
    Return:
        code (str): identified script from the input
        new_script (str): new script with code removal
    """
    not_quoting = True  # If parsing quotation, assuming '', "", and `` are the same

    start = 0           # Start index
    end = 0             # End index
    code = ''           # All code

    # Get Python code
    for i in range(len(script)):
        # Flip quoting bool if start/end quotating
        if script[i] == '\'' or script[i] == '\"' or script[i] == '`':
            not_quoting = not not_quoting

        # Set start index if start timing and not quotating
        elif script[i] == '<' and not_quoting:
            start = i + 1

        # Set end index if end timing and not quotating
        elif script[i] == '>' and not_quoting:
            end = i

        # <Python> code must continue till the end
        if script[start:end] == 'Python':
            code = script[end + 1:].strip()
            script = script[0:start-1].strip() if start > 1 else ""
            break

    return code, script

def embed_script(script: str) -> str:
    """
    Find, execute, and return printing strings from Python codes.

    Params:
        script (str): input Python script
    
    Return:
        output (str): string obtained from running identified Python code
    """
    py_script, output = get_script(script)
    print(py_script)

    # Redirect stdout to an in-memory buffer
    out_buffer = io.StringIO()
    sys.stdout = out_buffer

    # Execute code and retrieve printing values
    code = compile(py_script, '<string>', 'exec')
    exec(code)
    output += out_buffer.getvalue()

    # Restore stdout to default for print()
    sys.stdout = sys.__stdout__

    return output

def set_frame(frames: list[list], indexes: list[int], eofs: list[str], objects: list[str]):
    """
    Set displaying object to their desinated frames

    Params:
        frames (list[list]): all frames
        indexes (list[int]): targeted frames
        eofs (list[str]): objects that display to eof
        object (list[str]): object's id to display

    Return:
        frames (list[list]): all (modified) frames
    """
    new_max = len(frames)

    # Set frame
    for index in indexes:
        # Extend total frame if needed
        if index > new_max:
            # Add infinite objects
            frames += [eofs[:] for _ in range(index - new_max)]
            new_max = index

        # Add objects to destinated frames
        frames[index - 1].extend(objects)

    return frames

def parse_frames(script):
    """
    Parse input script to list of all frames with displaying object's id

    Params:
        script (str): input script
    
    Return:
        frames (list[list]): all frames
    """
    is_timing = False       # If parsing frame time (i.e <...>)   
    is_eof = False          # If parsing infinity (i.e. 'x-')
    is_next = False         # If parsing period (i.e. 'x-y')
    is_bracket = False      # If parsing bracket (i.e. {...})
    
    fr_index = ''           # From index
    to_index = ''           # To index

    curr_object = ['']      # Object's id list
    curr_index = 0          # Object's id index

    indexes = []            # All indexes
    eofs = []               # All object displayed to eof
    frames = [[]]           # All frames

    # Embed script
    script = embed_script(script).replace("\n", "").strip()

    for i in range(len(script)):
        # Set is_bracket = True if see '{'
        if script[i] == '{':
            is_bracket = True

        # Set is_bracket = True if see '}'
        elif script[i] == '}':
            is_bracket = False
        
        # Set frame and reset objects if start timing
        if is_bracket:
            curr_object[curr_index] += script[i]

        # Set is_next = True if see '-'
        elif script[i] == '-':
            is_next = True
        
        elif script[i] == '<':
            # Put to infinite list if eof
            if is_eof:
                eofs.extend(curr_object)

            frames = set_frame(frames, indexes, eofs, curr_object)

            # Reset
            curr_object = ['']
            curr_index = 0
            indexes = []
            is_timing = True
            is_eof = False
        
        # Add index to indexes and reset temp indexes if end timing or see ','
        elif script[i] == '>' or (script[i] == ',' and is_timing):
            # Put to eof if see '-' but have no to_index 
            if is_next and to_index == '':
                is_eof = True

            # Continue if indexes are not number (e.g. Python, Graph)
            start = int(fr_index)
            end = int(to_index) if to_index != '' else len(frames) if is_next else start
            indexes += range(start, end + 1)

            # Reset
            fr_index = ''
            to_index = ''
            if script[i] == '>':
                is_timing = False
                is_next = False

        elif script[i] == ',' and not (is_timing or is_bracket):
            curr_index += 1
            curr_object.append('')
        
        # Otherwise, append char to to_index/fr_index/curr_object
        elif script[i] != ' ':
            if is_timing:
                if is_next:
                    to_index += script[i]
                else:
                    fr_index += script[i]
            else:  
                curr_object[curr_index] += script[i]

        # Set frame if end of file but has some frames to add
        if i == len(script) - 1 and len(indexes) != 0:
            frames = set_frame(frames, indexes, eofs, curr_object)
			
    return frames

def main():
    script = sys.argv[1]
    frames = parse_frames(script)

    # Return frames to stdout 
    print(frames)       # <--- DON'T DELETE THIS LINE
    return frames

if __name__ == "__main__":
    main()