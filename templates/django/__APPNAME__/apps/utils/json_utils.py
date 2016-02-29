
import datetime
import json


class JSONEncoder(json.JSONEncoder):
    # this class is useful for serialization of objects into JSON
    # it helps to deal with complex types that standard JSON parser no not know about
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%Y %m %d %H:%M:%S")
        # elif isinstance(o, bson.ObjectId):
        #     return str(o)
        return json.JSONEncoder.default(self, o)
