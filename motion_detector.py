import cv2
import time

# Start camera
camera = cv2.VideoCapture(0)

# Load OpenCV's face detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

previous_x = None
previous_y = None

print("📷 Sneeze Measure - Motion Detector")
print("Move your head around.")
print("Press Q to quit.")

while True:

    success, frame = camera.read()

    if not success:
        print("❌ Could not read camera")
        break

    # Convert camera image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find faces
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    for (x, y, w, h) in faces:

        # Draw rectangle around face
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Find center of face
        center_x = x + w // 2
        center_y = y + h // 2

        # Calculate movement
        if previous_x is not None:

            movement = (
                abs(center_x - previous_x)
                + abs(center_y - previous_y)
            )

            cv2.putText(
                frame,
                f"Movement: {movement:.1f}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            # Detect sudden movement
            if movement > 15:

                cv2.putText(
                    frame,
                    "MOTION DETECTED!",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

        previous_x = center_x
        previous_y = center_y

    cv2.imshow("Sneeze Measure - Motion Detector", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()