from fastapi import FastAPI
from configReader import configReader
from PrettyJSONResponse import PrettyJSONResponse

app = FastAPI()
parser = configReader()

@app.get("/", response_class=PrettyJSONResponse)
def read_root():
    return parser.parseConfig()
