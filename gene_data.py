import os
import cv2
import time

# define
TRAIN_DATA_SIZE = 300
TEST_DATA_SIZE = 50
ESC = 27


def train_data(frame, key, i):

    if key == '1':
        input_data_type = 'input'
    elif key == '2':
        input_data_type = 'delete'
    elif key == '3':
        input_data_type = 'stop'
    elif key == '4':
        input_data_type = 'send_to_OCR'

    print("your are taking the set of " + input_data_type + " " + str(i))

    if not os.path.exists("Dataset/training_set/"+input_data_type):
        os.mkdir("Dataset/training_set/"+input_data_type)

    cv2.putText(frame, "now taking the data of"+input_data_type+"gesture" + str(i), (20, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                255)
    cv2.imshow("recording", frame)
    cv2.waitKey(50)
    cv2.imwrite("Dataset/training_set/" + input_data_type + '/' + str(i) + ".jpg", frame[200:424, 300:524])

    k = cv2.waitKey(2) & 0xFF
    if k == ESC:
        exit()

    k = cv2.waitKey(2)
    if k == '0':
        print("pause now, press any key to continue")
        while True:
            cv2.waitKey()
            break


def test_data(frame, key, i):
    if key == '1':
        input_data_type = 'input'
    elif key == '2':
        input_data_type = 'delete'
    elif key == '3':
        input_data_type = 'stop'
    elif key == '4':
        input_data_type = 'send_to_OCR'

    print("your are taking the set of " + input_data_type + " " + str(i))

    if not os.path.exists("Dataset/test_set/" + input_data_type):
        os.mkdir("Dataset/test_set/" + input_data_type)

    cv2.putText(frame, "now taking the data of"+input_data_type+"gesture" + str(i), (20, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                255)
    cv2.imshow("recording", frame)
    cv2.waitKey(50)
    cv2.imwrite("Dataset/test_set/" + input_data_type + '/' + str(i) + ".jpg", frame[200:424, 300:524])

    k = cv2.waitKey(2) & 0xFF
    if k == ESC:
        exit()

    k = cv2.waitKey(2)
    if k == '0':
        print("pause now, press any key to continue")
        while True:
            cv2.waitKey()
            break


if not os.path.exists("Dataset"):
    os.mkdir("Dataset")
if not os.path.exists("Dataset/training_set"):
    os.mkdir("Dataset/training_set")
if not os.path.exists("Dataset/test_set"):
    os.mkdir("Dataset/test_set")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

while True:
    print("""
            this code will guide you to build your own dataset, the size of training and test data set can be
        modified by yourself, defaults are 300 and 50, press any button to stat:

        press:
            1 to take training set
            2 to take test set
            0 to exit
        """)
    Key = input()
    if Key == '1':
        print("now taking train data set")
        while True:
            print("""
                        you are taking train data set now
                        press:
                            1 to take input gesture
                            2 to take delete gesture
                            3 to take stop gesture
                            4 to take send_to_OCR gesture
                            0 to exit
                """)
            key = input()
            if key == '0':
                break


            time_start = time.time()
            second = 5
            while True:
                time_now = time.time()
                print(time_now-time_start)
                if (time_now-time_start) >= 1:
                    second = second - 1
                    time_start = time_now
                ret, frame = cap.read()
                cv2.rectangle(frame, (300, 200), (524, 424), (0, 255, 0), 1)
                cv2.putText(frame, "recording will stat in "+str(second)+" seconds, put your hands in the rectangle",
                            (20, 20),
                            cv2.FONT_HERSHEY_PLAIN, 1,
                            255)
                cv2.imshow("recording", frame)
                cv2.waitKey(10)
                if second == 0:
                    break

            # take data
            for i in range(1, TRAIN_DATA_SIZE):
                ret, frame = cap.read()
                cv2.rectangle(frame, (300, 200), (524, 424), (0, 255, 0), 1)
                train_data(frame, key, i)

    elif Key == '2':
        print("now taking test data set")
        while True:
            print("""
                        you are taking train data set now
                        press:
                            1 to take input gesture
                            2 to take delete gesture
                            3 to take stop gesture
                            4 to take send_to_OCR gesture
                            0 to exit
                """)
            key = input()
            if key == '0':
                break

            # count down
            time_start = time.time()
            second = 5
            while True:
                time_now = time.time()
                print(time_now - time_start)
                if (time_now - time_start) >= 1:
                    second = second - 1
                    time_start = time_now
                ret, frame = cap.read()
                cv2.rectangle(frame, (300, 200), (524, 424), (0, 255, 0), 1)
                cv2.putText(frame,
                            "recording will stat in " + str(second) + " seconds, put your hands in the rectangle",
                            (20, 20),
                            cv2.FONT_HERSHEY_PLAIN, 1,
                            255)
                cv2.imshow("recording", frame)
                cv2.waitKey(10)
                if second == 0:
                    break

            # take data
            for i in range(1, TEST_DATA_SIZE):
                ret, frame = cap.read()
                cv2.rectangle(frame, (300, 200), (524, 424), (0, 255, 0), 1)
                test_data(frame, key, i)

    elif Key == '0':
        cap.release()
        cv2.destroyAllWindows()
        exit(0)

    else:
        print('wrong input')
        continue

