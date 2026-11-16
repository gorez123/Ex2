import os
import cv2

cascade_path = os.path.join(os.path.dirname(cv2.__file__), "data", "haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(cascade_path)

img = cv2.imread("class_photo.jpeg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(20, 20))

print(f"Detected students: {len(faces)}")

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
cv2.imwrite("haar_result.jpg", img)