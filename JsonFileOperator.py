import json

class JsonFileOperator:
    'Perform operations on JSON file'

    def __init__(self, name, mode):
        self.name = name
        self.mode = mode
   
    def Write(self, data):
        with open(self.name, self.mode) as file:
            json.dump(data, file)
        
    def Read(self):
        data = None
        with open(self.name, self.mode) as file:
            data = json.load(file)
        
        return data
