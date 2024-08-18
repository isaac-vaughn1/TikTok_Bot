import json

data = None 

def load_data():
    """
    Loads information from Configure.json
    """
    global data

    try:
        with open('Configure.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Configure.json not found")
    except Exception as e:
        print(f"There was an error loading Configure.json: {e}")

load_data()