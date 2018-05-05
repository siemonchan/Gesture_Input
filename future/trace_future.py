import cv2
import numpy as np


class TRACE:

    __BLUR_KERNEL_SIZE = 15
    __OPEN_KERNEL_SIZE = 15
    __CLOSE_KERNEL_SIZE = 15
    __RED = (0, 0, 255)
    __GREEN = (0, 255, 0)
    __BLUE = (255, 0, 0)
    __WHITE = (255, 255, 255)
    __Distance_to_Disconnect = 100

    def __init__(self):
        self.trace = []

    def __op_open(self, img, kernel_size):
        if kernel_size % 2 == 0:
            raise ValueError("kernel_size must be an odd number")

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        binary = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        # cv2.imshow("open", binary)
        return binary

    def __op_close(self, img, kernel_size):
        if kernel_size % 2 == 0:
            raise ValueError("kernel_size must be an odd number")

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        binary = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        # cv2.imshow("close", binary)
        return binary

    def __op_blur(self, img, kernel_size):
        if kernel_size % 2 == 0:
            raise ValueError("kernel_size must be an odd number")

        binary = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
        return binary

    def append(self, data):
        self.trace.append(data)

    def clear(self):
        self.trace.clear()

    def draw_trace(self, frame):
        if len(self.trace) < 4:
            pass
        else:
            for i in range(0, len(self.trace) - 2, 2):
                start_point = (self.trace[i], self.trace[i + 1])
                end_point = (self.trace[i + 2], self.trace[i + 3])

                # judge if the distance between two point is too far (larger than threshold)
                if ((start_point[0] - end_point[0]) * (start_point[0] - end_point[0]) +
                    (start_point[1] - end_point[1]) * (start_point[1] - end_point[1])) < self.__Distance_to_Disconnect:
                    cv2.line(frame, start_point, end_point, self.__RED, 10)
        return frame

    def get_trace(self, height, width):
        canvas = np.zeros((height, width, 3), np.uint8)
        canvas.fill(255)

        for i in range(0, len(self.trace) - 2, 2):
            start_point = (self.trace[i], self.trace[i + 1])
            end_point = (self.trace[i + 2], self.trace[i + 3])

            # judge if the distance between two point is too far (larger than threshold)
            if ((start_point[0] - end_point[0]) * (start_point[0] - end_point[0]) +
                (start_point[1] - end_point[1]) * (start_point[1] - end_point[1])) < self.__Distance_to_Disconnect:
                cv2.line(canvas, start_point, end_point, self.__RED, 10)

        pic = self.__op_blur(canvas, self.__BLUR_KERNEL_SIZE)
        pic = self.__op_close(pic, self.__OPEN_KERNEL_SIZE)
        pic = self.__op_open(pic, self.__CLOSE_KERNEL_SIZE)

        return pic