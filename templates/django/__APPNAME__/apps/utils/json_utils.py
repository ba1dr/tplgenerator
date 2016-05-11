
import time
import datetime
import json

# Usage:  json.dumps(data, cls=JSONEncoder, indent=4, sort_keys=True, ensure_ascii=False)


class JSONEncoder(json.JSONEncoder):
    # this class is useful for serialization of objects into JSON
    # it helps to deal with complex types that standard JSON parser does not know about
    def default(self, o):
        if isinstance(o, datetime.datetime):
            # return (o + datetime.timedelta(seconds=time.timezone)).strftime("%Y %m %d %H:%M:%S+0000")
            return o.strftime("%Y %m %d %H:%M:%S")
        # elif isinstance(o, bson.ObjectId):
        #     return str(o)
        return json.JSONEncoder.default(self, o)
