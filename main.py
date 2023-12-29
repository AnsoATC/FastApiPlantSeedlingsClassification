from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import cv2

app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:3000",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Load your trained model
MODEL = tf.keras.models.load_model('saved_models/best_model_3.keras')  # Update with your model path

# Define class names as per your model
CLASS_NAMES = ['Black-grass', 'Charlock', 'Cleavers', 'Common Chickweed',
               'Common wheat', 'Fat Hen', 'Loose Silky-bent', 'Maize',
               'Scentless Mayweed', 'Shepherds Purse',
               'Small-flowered Cranesbill', 'Sugar beet']

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

def preprocess_image(image: Image.Image) -> np.ndarray:
    # Convert PIL Image to NumPy array
    img = np.array(image)

    # Resize, convert to HSV, apply mask, etc., as per your model's training
    img = cv2.resize(img, (128, 128))
    blurr = cv2.GaussianBlur(img, (5, 5), 0)
    hsv = cv2.cvtColor(blurr, cv2.COLOR_BGR2HSV)
    # ... continue with your specific preprocessing

    # Normalize the image
    img = img.astype('float32') / 255.0

    return img

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    image = Image.open(BytesIO(await file.read()))
    processed_image = preprocess_image(image)
    img_batch = np.expand_dims(processed_image, 0)

    predictions = MODEL.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    return {
        'class': predicted_class,
        'confidence': float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
