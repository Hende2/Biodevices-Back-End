import json
from test_inserting_w_acc import insert_data
from from_file import jsonc_to_json_func, remove_comments, unpackage

print(jsonc_to_json_func('readings_data.jsonc')) # Converts the jsonc file to a python dictionary containing the same data under teh same keys
insert_data(jsonc_to_json_func('readings_data.jsonc'))


