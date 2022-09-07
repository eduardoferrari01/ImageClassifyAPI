import io
from fastapi import FastAPI, File
from PIL import Image

from api.core.cnn.cnn_model import CnnModel

app = FastAPI()

cnn = CnnModel()


@app.get("/cnn/class/names")
def get_class_names():
    return cnn.get_class_names()


@app.post("/cnn/classify")
async def classify(file: bytes = File(...)):
    image = Image.open(io.BytesIO(file))
    return cnn.classify(image)


@app.get("/cnn/exists/label/{label}")
def recognized_label(label):
    return label in cnn.get_class_names()
