import json

def remove_comments(jsonc):
    ''' Comments are the only differentiating factor between jsonc and json, so create a list representing the jsonc file and remove all 
    lines starting with the // denoting a comment'''
    lines = jsonc.split('\n')
    json_lines = [line for line in lines if not line.strip().startswith('//')]
    return '\n'.join(json_lines)

def jsonc_to_json_func(jsonc_file, json_file):
    '''Writes contents of jsonc file into a readable and iterable json file.
    Input: jsonc file to be read, empty file to add the contents of the jsonc to
    Result: json file populated with the correct data'''
    with open(jsonc_file, 'r') as f:
        jsonc_content = f.read()

    json_content = remove_comments(jsonc_content)

    # Parsing the JSON
    parsed_json = json.loads(json_content)

    # Write the parsed JSON to a new file
    with open(json_file, 'w') as f:
        json.dump(parsed_json, f, indent=4)  # Optionally, you can specify an indentation level