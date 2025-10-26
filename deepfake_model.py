from transformers import AutoImageProcessor, ViTForImageClassification
import cv2
import torch
from PIL import Image
import numpy as np

# MODÈLE PUBLIC 92% ACCURACY + BOOST INTELLIGENT
model_name = "prithivMLmods/Deep-Fake-Detector-v2-Model"
processor = AutoImageProcessor.from_pretrained(model_name)
model = ViTForImageClassification.from_pretrained(model_name)

# Détecteur de visage
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def extract_score(video_path):
    cap = cv2.VideoCapture(video_path)
    scores = []
    frame_count = 0

    while cap.isOpened() and frame_count < 60:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        # Détection visage
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            face = frame[y:y+h, x:x+w]
        else:
            face = frame  # fallback

        # Préparation image
        rgb_face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_face).resize((224, 224))
        
        inputs = processor(images=pil_image, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            fake_prob = probs[0][0].item()  # 0 = Deepfake
        scores.append(fake_prob)
    
    cap.release()
    
    if not scores:
        return 0.5

    raw_score = np.mean(scores)

    # BOOST AGRESSIF
    if raw_score > 0.5:
        raw_score = min(0.99, raw_score * 1.5)
    elif raw_score > 0.3:
        raw_score = min(0.95, raw_score * 1.3)

    return raw_score