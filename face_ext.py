import cv2
import numpy as np
import os
from facedetector import FaceDetector
from PIL import Image
# Load the face cascade model.
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Open the video file.
video = cv2.VideoCapture('vid1.mp4')

# Create a folder to store the extracted faces.
if not os.path.exists('faces'):
    os.mkdir('faces')

# Iterate through the frames of the video.
images= []
padding = 1.0
while True:

    # Read the frame.
    ret, frame = video.read()
    if ret and isinstance(frame, np.ndarray):
          image = {
            "file": frame,
            "sourcePath": video,
            "sourceType": "video",
          }
          images.append(image)
    else:
        break
video.release()
cv2.destroyAllWindows()
for (i, image) in enumerate(images):
    print("[INFO] processing image {}/{}".format(i + 1, len(images)))
    faces = FaceDetector.detect(image["file"])

    array = cv2.cvtColor(image['file'], cv2.COLOR_BGR2RGB)
    img = Image.fromarray(array)

    j = 1
    for face in faces:
      
      bbox = face['bounding_box']
      pivotX, pivotY = face['pivot']
      
      if bbox['width'] < 10 or bbox['height'] < 10:
        continue
      
      left = pivotX - bbox['width'] / 1.0 * padding
      top = pivotY - bbox['height'] / 1.0 * padding
      right = pivotX + bbox['width'] / 1.0 * padding
      bottom = pivotY + bbox['height'] / 1.0 * padding
      cropped = img.crop((left, top, right, bottom))
      cv2.imwrite(os.path.join('faces', 'face_{}.jpg'.format(len(os.listdir('faces')))), np.asarray(cropped))
   