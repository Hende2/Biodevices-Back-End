import json
from test_inserting_w_acc import insert_data
from from_file import jsonc_to_json_func, remove_comments

print(jsonc_to_json_func('readings_data.jsonc'))
insert_data(jsonc_to_json_func('readings_data.jsonc'))


