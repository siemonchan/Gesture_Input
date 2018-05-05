import tensorflow as tf
import cv2
import time
from HandDetection import detection
from HandRecognition import load_model
from HandRecognition import recognition
from future.character import Stroke
from future.character import Character

# define
Not_Supported_Type = 0
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)
INPUT = 1  # one figure up: to input character
STOP = 2  # put up the whole hand: to stop the whole program
SEND_TO_OCR = 3  # thumps up: to send the trace you`ve finished to the OCR to recognize
DELETE = 4  # fist: to delete a character
SIGSTOP = 3  # signal stop
SIGOCR = 3  # signal send to OCR
SIGDELTE = 3  # signal delete
ESC = 27  # ESC

config = tf.ConfigProto()
config.gpu_options.allow_growth = True

# load model for cnn
model = load_model()

# Open Camera object
cap = cv2.VideoCapture(0)

# Decrease frame size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

text = []
character = Character(800, 600)
stroke = Stroke()
cnt_x = []
cnt_y = []
signal_stop = 0
signal_delete = 0
signal_OCR = 0
FPS = 0
STATE_NOW = None

while True:
    start_time = time.time()
    # do hand detection
    ret, frame = cap.read()
    frame, X, Y, W, H, cnt_x, cnt_y = detection(frame)

    if X == 0 & Y == 0 & W == 0 & H == 0:  # no hand detected, do nothing
        continue
    else:
        # resize the img
        img = frame[Y:Y+H, X:X+W]
        img_proc = cv2.resize(img, (200, 200))

        # do hand recognition
        possibility, result = recognition(img_proc, model)

        if result == Not_Supported_Type:

            signal_delete = max(0, signal_delete - 1)
            signal_stop = max(0, signal_stop - 1)
            signal_OCR = max(0, signal_OCR - 1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            frame = cv2.putText(frame, "FPS:" + str(FPS) + ' STOP  Input Context:' + text, (20, 20), font,
                                1.2, GREEN)
            if STATE_NOW == INPUT:
                if stroke not in vars():
                    character.character_append(stroke)  # 判断为该笔画已经输入完
                    del stroke

            STATE_NOW = Not_Supported_Type

        elif result == INPUT:
            signal_delete = max(0, signal_delete - 1)
            signal_stop = max(0, signal_stop - 1)
            signal_OCR = max(0, signal_OCR - 1)

            if stroke not in vars():
                stroke = Stroke()

            Loc_X = cnt_x[list(cnt_y).index(max(cnt_y))]
            Loc_Y = max(cnt_y)
            stroke.stroke_append(Loc_X)
            stroke.stroke_append(Loc_Y)
            character.draw_character()
            font = cv2.FONT_HERSHEY_SIMPLEX
            frame = cv2.putText(frame, "FPS:" + str(FPS) + ' INPUT  Input Context:' + text, (20, 20), font,
                                1.2, GREEN)

            STATE_NOW = INPUT

        elif result == STOP:
            signal_delete = max(0, signal_delete - 1)
            signal_OCR = max(0, signal_OCR - 1)
            signal_stop = signal_stop + 1

            font = cv2.FONT_HERSHEY_SIMPLEX
            frame = cv2.putText(frame, "FPS:" + str(FPS) + ' STOP  Input Context:' + text, (20, 20), font,
                                1.2, GREEN)

            if signal_stop == SIGSTOP:
                STATE_NOW = STOP
                signal_stop = 0
                print('program ending now!')
                font = cv2.FONT_HERSHEY_SIMPLEX
                frame = cv2.putText(frame, 'program ending now!', (20, 20), font, 1.2, GREEN)
                text.clear()
                stroke.stroke_clear()
                character.character_clear()
                cv2.waitKey(500)
                exit(0)

        elif result == DELETE:
            signal_stop = max(0, signal_stop - 1)
            signal_OCR = max(0, signal_OCR - 1)
            signal_delete = signal_delete + 1

            if signal_delete == SIGDELTE:
                STATE_NOW = DELETE
                signal_delete = 0
                text = text[:-1]

            font = cv2.FONT_HERSHEY_SIMPLEX
            frame = cv2.putText(frame, "FPS:" + str(FPS) + ' DELETE  Input Context:' + text, (20, 20), font,
                                1.2, GREEN)

        elif result == SEND_TO_OCR:
            signal_stop = max(0, signal_stop - 1)
            signal_delete = max(0, signal_delete - 1)
            signal_OCR = signal_OCR + 1

            if signal_OCR == SIGOCR:
                signal_OCR = 0
                if STATE_NOW == INPUT:
                    character.character_append(stroke)
                text.append(character.recognize_character())
                character.character_clear()
                stroke.stroke_clear()

                STATE_NOW = SEND_TO_OCR

            font = cv2.FONT_HERSHEY_SIMPLEX
            frame = cv2.putText(frame, "FPS:" + str(FPS) + ' SEND TO OCR  Input Context:' + text, (20, 20), font,
                                1.2, GREEN, 2)

    # get FPS
    time_per_frame = time.time() - start_time
    FPS = 1000 / time_per_frame

    # show image
    cv2.imshow('Gesture_Input_Demo', frame)

    # close the output video by pressing 'ESC'
    k = cv2.waitKey(2) & 0xFF
    if k == ESC:
        break

cap.release()
cv2.destroyAllWindows()
