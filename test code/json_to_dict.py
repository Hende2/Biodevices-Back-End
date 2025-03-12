from jsonc_to_json import jsonc_to_json_func 
#Also automatically imports json

# jsonc_to_json_func('readings_data.jsonc','test_output.json') #This converts into json file

with open('test_output.json') as file:
    data = json.load(file)
print(data)

