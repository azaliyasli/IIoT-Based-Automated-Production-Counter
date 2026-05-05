import cv2
from ultralytics import YOLO
from mqtt_publisher import MQTTPublisher

mqtt_client = MQTTPublisher("broker.hivemq.com", 1883, "factory/line1/bottle_count")

# Load Model
model = YOLO('yolov8n.pt')

# Prepare Video
video_path = "BottleProductionVideo.mp4"
cap = cv2.VideoCapture(video_path)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Prepare Counting
count_line_x = int((width / 2) + 500)

counted_ids = set()
total_bottles = 0

# Vision
while True:
    success, frame = cap.read()
    if not success:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        counted_ids.clear()
        continue

    # Track and Detect Objects (Bottles)
    results = model.track(frame, classes=[39], persist=True, tracker="bytetrack.yaml", verbose=False) # classes=[39] = "bottle"

    if results[0].boxes.id is not None:
        # Get coordinates and ids
        boxes = results[0].boxes.xyxy.cpu().numpy()
        track_ids = results[0].boxes.id.int().cpu().numpy()

        # Locate
        for box, track_id in zip(boxes, track_ids):
            x1, y1, x2, y2 = map(int, box)

            # Locating center of bottles
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # Visualize boxes and centers
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
            cv2.putText(frame, f"ID: {track_id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Counter
            offset = 15
            if (count_line_x - offset) < center_x < (count_line_x + offset):
                if track_id not in counted_ids:
                    counted_ids.add(track_id)
                    total_bottles += 1
                    mqtt_client.publish_count(total_bottles)

    cv2.line(frame, (count_line_x, 0), (count_line_x, height), (255, 0, 0), 2)

    # Print total number of produced bottles
    cv2.putText(frame, f"Total Bottles: {total_bottles}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

    # Open video
    cv2.imshow("Bottle Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

mqtt_client.stop()
cap.release()
cv2.destroyAllWindows()