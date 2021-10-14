import requests
import cv2

url = "localhost:4242/api/predict"
file_path = "images/test_image.jpg"

query = {'image': (file_path, open(file_path, 'rb'), "image/jpeg")}



response = requests.post(
    'http://localhost:4242/api/predict', files=query)

prediction = response.json()

print("Your model has predicted that waldo is at the xy location ({}, {})".format(
    prediction["x"], prediction["y"]))


image = cv2.imread(file_path)
image = cv2.circle(
    image, (prediction["x"], prediction["y"]), 5, (0, 255, 0), -1)

cv2.imwrite("result.png", image)
