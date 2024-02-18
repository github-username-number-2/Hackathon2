import os
import cv2
from ultralytics import YOLO
import time

# Path to save the output video
video_path_out = 'output_webcam.mp4'

# Initialize the video writer
out = None

# Initialize webcam
cap = cv2.VideoCapture(0)  # 0 for default webcam, change to other values if multiple webcams are connected

# Load the YOLO model
model_path = os.path.join('.', 'runs', 'detect', 'train', 'weights', 'last.pt')
model_path = "C:\\Users\\luekb\\Downloads\\birddetect\\birddetect\\best.pt"
model = YOLO(model_path)  # load a custom model

threshold = 0.75

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if out is None:
        H, W, _ = frame.shape
        out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), 30, (W, H))

    # Perform object detection
    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            '''cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)'''
            cv2.putText(frame, "OBSTACLE", (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    # Write frame to output video
    out.write(frame)

    # Display the frame
    cv2.imshow('YOLOv8 Object Detection', frame)

    # Break the loop if 'q' is pressed
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(.0001)

# Release the video capture and writer
cap.release()
if out is not None:
    out.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
