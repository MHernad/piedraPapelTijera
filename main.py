import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
points = [0, 0]
jugar = True
papel = cv2.imread("imgs/papel.png")
piedra = cv2.imread("imgs/piedra.png")
tijera = cv2.imread("imgs/tijera.png")

tijera = cv2.resize(tijera, (320, 240))
papel = cv2.resize(papel, (320, 240))
piedra = cv2.resize(piedra, (320, 240))

cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Output", 640, 240)


def getHandMove(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if all([handLms.landmark[i].y < handLms.landmark[i + 3].y for i in range(9, 20, 4)]):
        return "rock"
    elif landmarks[13].y < landmarks[16].y and landmarks[17].y < landmarks[20].y:
        return "scissors"
    else:
        return "paper"


while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    if jugar:

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for _id, lm in enumerate(handLms.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    move = getHandMove(handLms)

                    result = papel

                    if move == "scissors":
                        result = piedra
                    elif move == "paper":
                        result = tijera
                    elif move == "rock":
                        result = papel

                    image = cv2.resize(image, (320, 240))

                    output_image = cv2.hconcat([image, result])

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(output_image, f"Player: {points[0]}", (10, 30), font, 1, (255, 255, 255), 2)
                    cv2.putText(output_image, f"AI: {points[1]}", (330, 30), font, 1, (255, 255, 255), 2)

                    cv2.imshow("Output", output_image)
                    key = cv2.waitKey(1)