from flask import Flask, request
from flask_smorest import abort

app = Flask(__name__)

# records = [{"name": "Marquee Moon", "tracks": [{"name": "See No Evil", "position": 1}]}]
records = [
    {
        "id": 1,
        "name": "Marquee Moon",
        "artist": "Television",
        "tracks": [
            {
                "name": "See No Evil",
                "position": 1,
            }
        ]
    }
]


@app.get("/records")
def get_records():
    return {"records": records}


@app.post("/record")
def create_record():
    request_data = request.get_json()
    new_record = {"name": request_data["name"], "tracks": []}
    records.append(new_record)
    return new_record, 201


@app.post("/record/<string:name>/track")
def create_item(name):
    request_data = request.get_json()
    for record in records:
        if record["name"] == name:
            new_item = {"name": request_data["name"], "position": request_data["position"]}
            record["tracks"].append(new_item)
            return new_item, 201
    return abort(404, messages="Track not found")


@app.get("/record/<string:name>")
def get_record(name):
    for record in records:
        if record["name"] == name:
            return record
    return abort(404, message="Record not found")


@app.get("/record/<string:name>/track")
def get_item_in_record(name):
    for record in records:
        if record["name"] == name:
            return {"tracks": record["tracks"]}
    # return {"message": "Record not found"}, 404
    return abort(404, message="Track not found")
