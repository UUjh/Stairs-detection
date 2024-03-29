import numpy as np
import cv2
import glob

#Load YOLO
net = net = cv2.dnn.readNet("yolov3_training_2000.weights","yolov3_testing.cfg")

# Name custom object
classes = ["stair"]

layer_names = net.getLayerNames()
output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes),3))

#save image path
img_path = 'C:/Users/lenovo/Desktop/edge_tmp/tmp.jpg'

# read image path
img_path2 = (r'C:/Users/lenovo/Desktop/edge_tmp/tmp.jpg')


cap = cv2.VideoCapture(0)

while(True):
    _, frame = cap.read()
    
    heigth, width, channels = frame.shape
    frame = cv2.GaussianBlur(frame, (5, 5), 0.3)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # get edge
    edge = cv2.Canny(frame, 25, 75)
    
    # edge가 NoneType으로 나옴.
    
    # save
    img = cv2.imread(img_path2)
    
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    heigth2, width2, channels2 = img.shape

    blob = cv2. dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    class_ids = []
    confidences = []
    boxes = []
    
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                # Object detected
                print(class_id)
    
                center_x = int(detection[0] * width2)
                center_y = int(detection[1] * heigth2)
                w = int(detection[2] * width2)
                h = int(detection[3] * heigth2)
                
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                
                boxes.append([x,y,w,h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]

            cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            cv2.putText(img, label, (x,y + 30), font, 3 ,color, 3)


    Gx = cv2.Sobel(np.float32(frame), cv2.CV_32F, 1, 0, 3)
    Gy = cv2.Sobel(np.float32(frame), cv2.CV_32F, 0, 1, 3)

    sobel = cv2.magnitude(Gx, Gy)
    sobel = np.clip(sobel, 0, 255).astype(np.uint8)

# save sobel images
    cv2.imwrite(img_path, sobel)
    cv2.imshow("image", img)
    cv2.imshow("sobel", sobel)


    if cv2.waitKey(20) == ord('q'): 
        break
