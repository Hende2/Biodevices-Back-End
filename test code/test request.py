import requests
def get_data_from_mongodb():
    """
    fetch data from mongodb sever.
        
    """
    r = requests.get('http://127.0.0.1:8000/getreading')
    print(r.json())
    data_as_tuples = [tuple(item) for item in r.json()]
    print("requesting data")
    print(data_as_tuples)
    return data_as_tuples
get_data_from_mongodb()