import json

class identifiers:
    def __init__(self, id, datetime, hasSynced, isSafe, location, uid):
        self.id = id
        self.datetime = datetime
        self.hasSynced = hasSynced
        self.isSafe = isSafe
        self.location = location
        self.uid = uid

    def __repr__(self):
        return f"Identifiers({self.id}, {self.datetime}, {self.hasSynced}, {self.isSafe}, {self.location}, {self.uid})"

class measurements:
    def __init__(self, id, chloride, ph, temperature, turbidity, timeIntervals):
        self.id = id
        self.chloride = chloride
        self.ph = ph
        self.temperature = temperature
        self.turbidity = turbidity
        self.timeIntervals = timeIntervals

    def __repr__(self):
        return f"Measurements({self.id}, {self.chloride}, {self.ph}, {self.temperature}, {self.turbidity}, {self.timeIntervals})"

def remove_comments(jsonc):
    ''' Comments are the only differentiating factor between jsonc and json, so create a list representing the jsonc file and remove all 
    lines starting with the // denoting a comment'''
    lines = jsonc.split('\n')
    json_lines = [line for line in lines if not line.strip().startswith('//')]
    return '\n'.join(json_lines)

def jsonc_to_json_func(jsonc_file):
    '''Writes contents of jsonc file into a readable and iterable json file.
    Input: jsonc file to be read, empty file to add the contents of the jsonc to
    Result: json file populated with the correct data'''
    with open(jsonc_file, 'r') as f:
        jsonc_content = f.read()

    json_content = remove_comments(jsonc_content)
    parsed_json = json.loads(json_content)
    return parsed_json
    
def unpackage(dict):
    '''Converts the dictionary obtained from the json file into two python objects that satisfy relational requirements'''
    identifier_obj = identifiers(dict['id'], dict['datetime'], dict['hasSynced'], dict['isSafe'], dict['location'], dict['uid'])
    data_obj = measurements(dict['id'], dict['measurements'][0]['values'], dict['measurements'][1]['values'], dict['measurements'][2]['values'], dict['measurements'][3]['values'], dict['measurements'][1]['values'])
    print(identifier_obj)
    print(data_obj)
    return identifier_obj, data_obj

print(jsonc_to_json_func('readings_data.jsonc'))
unpackage(jsonc_to_json_func('readings_data.jsonc'))