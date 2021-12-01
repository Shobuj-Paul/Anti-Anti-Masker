#!/usr/bin/env python3

import numpy as np
import cv2
import os

def mask_detection(frame):
    # Load a model imported from Tensorflow
    tensorflowNet = cv2.dnn.readNetFromTensorflow('../frozen_models/frozen_graph.pb', '../frozen_models/model.pbtxt')
    mean = np.array([1.0, 1.0, 1.0]) * 127.5
    scale = 1 / 127.5
    # Use the given image as input, which needs to be blob(s).
    tensorflowNet.setInput(cv2.dnn.blobFromImage(frame.astype(np.float32), scale, size=(224, 224), mean=mean, swapRB=True, crop=False))
    # Runs a forward pass to compute the net output
    networkOutput = tensorflowNet.forward()[0]
    return networkOutput[1], networkOutput[0]

def main():
    # Set correct directory path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    cap =  cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame (stream end?). Exiting ...")
            break
            
        networkOutput1, networkOutput2 = mask_detection(frame)
        non_mask, mask = "Non-Mask: " + str(networkOutput1), "Mask: " + str(networkOutput2)
        
        frame = cv2.putText(frame, non_mask, (0,450), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,255), thickness=2)
        frame = cv2.putText(frame, mask, (0,400), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,255), thickness=2)

        cv2.imshow("Mask Detection", frame)
        k = cv2.waitKey(1)
        if k == ord('s'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try : main()
    except: pass