import json


class ParamsEncoder(json.JSONEncoder):
    def default(self, o) -> str:
        dictionary = dict(o.__dict__)
        for key in dictionary.keys():
            dictionary[key] = str(dictionary[key])
        return json.dumps(dictionary)
