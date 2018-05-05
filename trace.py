import numpy as np
import cv2


BLUR_KERNEL_SIZE = 15
OPEN_KERNEL_SIZE = 15
CLOSE_KERNEL_SIZE = 15
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)
Distance_to_Disconnect = 100


def blur(img, kernel_size):
    if kernel_size % 2 == 0:
        raise Exception("kernel_size must be an odd number")
    blur = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    return blur


def open(img, kernel_size):
    if kernel_size % 2 == 0:
        raise Exception("kernel_size must be an odd number")
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    binary = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    cv2.imshow("open", binary)
    return binary


def close(img, kernel_size):
    if kernel_size % 2 == 0:
        raise Exception("kernel_size must be an odd number")
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    binary = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("close", binary)
    return binary


def draw_trace(trace, frame):
    if len(trace) < 4:
        pass
    else:
        for i in range(0, len(trace), 2):
            start_point = (trace[i], trace[i + 1])
            end_point = (trace[i + 2], trace[i + 3])
            # judge if the distance between two point is too far (larger than threshold
            if ((start_point[0] - end_point[0])*(start_point[0] - end_point[0]) +
                (start_point[1] - end_point[1])*(start_point[1] - end_point[1])) < Distance_to_Disconnect:
                cv2.line(frame, start_point, end_point, RED, 10)
    return frame


def get_trace(height, width, trace):
    canvas = np.zeros((height, width, 3), np.uint8)
    canvas.fill(255)

    for i in range(0, len(trace), 2):
        start_point = (trace[i], trace[i + 1])
        end_point = (trace[i + 2], trace[i + 3])
        # judge if the distance between two point is too far (larger than threshold
        if ((start_point[0] - end_point[0]) * (start_point[0] - end_point[0]) +
            (start_point[1] - end_point[1]) * (start_point[1] - end_point[1])) < Distance_to_Disconnect:
            cv2.line(canvas, start_point, end_point, RED, 10)

    pic = blur(canvas, BLUR_KERNEL_SIZE)
    pic = close(pic, OPEN_KERNEL_SIZE)
    pic = open(pic, CLOSE_KERNEL_SIZE)

    return pic

