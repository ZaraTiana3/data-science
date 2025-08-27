import cv2
from imutils.video import VideoStream
import imutils
import mtcnn
from mtcnn import MTCNN
from mtcnn.utils.images import load_image

import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from  tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np

from collections import deque

buffer = deque(maxlen=10)

# Create a detector instance
detector = MTCNN(device="CPU:0")
detections_result = []

def process_image(frame):
    #image = load_img(path_image, target_size=(224,224))
    image = img_to_array(frame)
    frame = cv2.resize(frame, (224, 224))
    frame = preprocess_input(frame)
    return frame

model = tf.keras.models.load_model('D:\ongoing\python_project\Face_mask_detector\mask_detector.h5')

vs = VideoStream(src=0).start()

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    #detect face
    result = detector.detect_faces(frame)
    print("Image detected: ", result)
    
    if len(result)!=0: 
        print("Detect mask")   
        bounding_box = result[0]['box']
        face = frame[bounding_box[1]: bounding_box[1]+bounding_box[3],bounding_box[0]: bounding_box[0]+ bounding_box[2]] 
        img_processed = process_image(face)
        #predict the presence of mask
        predict = model.predict(np.expand_dims(img_processed, axis=0))

        print("Le resultat de detect_mask  est: ",predict, "d'où on a: ", np.argmax(predict))
        list_mask = [0,1]
        result_mask = list_mask[np.argmax(predict)] #with mask, without_mask

        #Append  the result_mask value in buffer
        buffer.append(result_mask)
        #Get the maximum value
    else:
        buffer.append(-1)
        
    max_value = max(list(buffer))
    if max_value == 0: #with mask
        print("With mask")
        cv2.putText(frame, "WITH MASK", (bounding_box[0], bounding_box[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0,255,0), 2)
        cv2.rectangle(frame,
                    (bounding_box[0], bounding_box[1]),
                    (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),(0,255,0),2)
        
    elif max_value == 1: #without mask
        print("Without mask")
        cv2.putText(frame, "WITHOUT MASK", (bounding_box[0], bounding_box[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0,0, 255), 2)
        cv2.rectangle(frame,
                    (bounding_box[0], bounding_box[1]),
                    (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),(0,0,255), 2)
        
    cv2.imshow("Image", frame)
    cv2.waitKey(1)



