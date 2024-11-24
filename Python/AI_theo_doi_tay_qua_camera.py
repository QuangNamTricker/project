import cv2
import mediapipe as mp
import time

# Khởi tạo webcam
cap = cv2.VideoCapture(0)

# Khởi tạo MediaPipe Hands
mphands = mp.solutions.hands
hands = mphands.Hands(False)
mpDraw = mp.solutions.drawing_utils

# Biến thời gian để tính FPS
pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    if not success:
        break

    # Chuyển đổi BGR sang RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Xử lý nếu phát hiện bàn tay
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:  # Lặp qua từng bàn tay
            for id, lm in enumerate(handLms.landmark):
                # Lấy tọa độ (x, y)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)

                # Vẽ vòng tròn tại điểm mốc số 0 (gốc của bàn tay)
                if id == 0:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

            # Vẽ các kết nối giữa các điểm mốc
            mpDraw.draw_landmarks(img, handLms, mphands.HAND_CONNECTIONS)

    # Tính FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Hiển thị FPS trên ảnh
    cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # Hiển thị hình ảnh
    cv2.imshow("Từ Quang Nam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
