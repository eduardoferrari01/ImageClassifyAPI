import io
from fastapi import FastAPI, File
from PIL import Image

from api.core.cnn.cnn_model import CnnModel

app = FastAPI()

cnn = CnnModel()


@app.get("/cnn/class/names")
def get_class_names():
    return cnn.get_classes()


@app.post("/cnn/classify/")
async def classify(file: bytes = File(...)):
    image = Image.open(io.BytesIO(file))
    return cnn.classify(image)
