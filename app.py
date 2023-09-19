from flask import Flask

app = Flask(__name__)

records = [
    {
        "name": "Marquee Moon",
        "artist": "Television",
        "tracks": [
            {
                "name": "See No Evil",
            }
        ],
    }
]

@app.get("/record")
def get_records():
    return {"records": records}
