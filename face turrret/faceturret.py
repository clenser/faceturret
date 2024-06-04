import cv2
import mediapipe as mp

# Configuration
write_video = True
debug = True
cam_source = 0   

x_min = 0
x_mid = 75
x_max = 150
# use angle between wrist and index finger to control x axis
palm_angle_min = -50
palm_angle_mid = 20

y_min = 0
y_mid = 90
y_max = 180
# use wrist y to control y axis
wrist_y_min = 0.3
wrist_y_max = 0.9

z_min = 10
z_mid = 90
z_max = 180
# use palm size to control z axis
plam_size_min = 0.1
plam_size_max = 0.3

claw_open_angle = 60
claw_close_angle = 0

prev_servo_angle = [x_mid, y_mid, z_mid, claw_open_angle]
fist_threshold = 7

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(cam_source)

# video writer
if write_video:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 60.0, (640, 480))

clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
map_range = lambda x, in_min, in_max, out_min, out_max: abs(
    (x - in_min) * (out_max - out_min) // (in_max - in_min)
)

with mp_hands.Hands(
    model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5
) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                WRIST = hand_landmarks.landmark[0]
                INDEX_FINGER_MCP = hand_landmarks.landmark[5]

                # calculate the distance between the wrist and the index finger
                palm_size = (
                    (WRIST.x - INDEX_FINGER_MCP.x) ** 2
                    + (WRIST.y - INDEX_FINGER_MCP.y) ** 2
                    + (WRIST.z - INDEX_FINGER_MCP.z) ** 2
                ) ** 0.5

                # Check if the hand is a fist
                distance_sum = 0
                for i in [7, 8, 11, 12, 15, 16, 19, 20]:
                    distance_sum += (
                        (WRIST.x - hand_landmarks.landmark[i].x) ** 2
                        + (WRIST.y - hand_landmarks.landmark[i].y) ** 2
                        + (WRIST.z - hand_landmarks.landmark[i].z) ** 2
                    ) ** 0.5
                if distance_sum / palm_size < fist_threshold:
                    claw_angle = claw_close_angle
                else:
                    claw_angle = claw_open_angle

                # calculate x angle
                distance = palm_size
                angle = (
                    WRIST.x - INDEX_FINGER_MCP.x
                ) / distance  # calculate the radian between the wrist and the index finger
                angle = int(
                    angle * 180 / 3.1415926
                )  # convert radian to degree
                angle = clamp(angle, palm_angle_min, palm_angle_mid)
                x_angle = map_range(
                    angle, palm_angle_min, palm_angle_mid, x_max, x_min
                )

                # calculate y angle
                wrist_y = clamp(WRIST.y, wrist_y_min, wrist_y_max)
                y_angle = map_range(wrist_y, wrist_y_min, wrist_y_max, y_max, y_min)

                # calculate z angle
                palm_size = clamp(palm_size, plam_size_min, plam_size_max)
                z_angle = map_range(
                    palm_size, plam_size_min, plam_size_max, z_max, z_min
                )

                print(x_angle, y_angle, z_angle, claw_angle)
                
                # Draw lines between hand landmarks
                connections = mp_hands.HAND_CONNECTIONS
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    connections,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style(),
                )

        # Flip the image horizontally for a selfie-view display.
        image = cv2.flip(image, 1)
        cv2.imshow("MediaPipe Hands", image)

        if write_video:
            out.write(image)
        if cv2.waitKey(5) & 0xFF == 27:
            if write_video:
                out.release()
            break

cap.release()
