import json

data = None 

def load_data():
    """
    Loads information from Configure.json
    """
    global data

    with open('Configure.json') as f:
        data = json.load(f)

load_data()