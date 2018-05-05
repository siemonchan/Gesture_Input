import cv2
import numpy as np
import pytesseract as pyt


class Stroke:

    __RED = (0, 0, 255)
    __GREEN = (0, 255, 0)
    __BLUE = (255, 0, 0)
    __WHITE = (255, 255, 255)

    def __init__(self):
        self.stroke = []

    def stroke_append(self, point):
        self.stroke.append(point[0])
        self.stroke.append(point[1])

    def stroke_clear(self):
        self.stroke.clear()

    def draw_stroke(self, canvas):
        if len(self.stroke) < 4:
            raise ValueError("too little input")
        else:
            for i in range(0, len(self.stroke) - 2, 2):
                start_point = (self.stroke[i], self.stroke[i + 1])
                end_point = (self.stroke[i + 2], self.stroke[i + 3])

                cv2.line(canvas, start_point, end_point, self.__RED, 10)


class Character:

    __BLUR_KERNEL_SIZE = 15
    __OPEN_KERNEL_SIZE = 15
    __CLOSE_KERNEL_SIZE = 15

    def __init__(self, height, width):
        self.character = []
        self.height = height
        self.width = width

    def __image_process(self, canvas):
        binary = cv2.GaussianBlur(canvas, (self.__BLUR_KERNEL_SIZE, self.__BLUR_KERNEL_SIZE), 0)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.__CLOSE_KERNEL_SIZE, self.__CLOSE_KERNEL_SIZE))
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.__OPEN_KERNEL_SIZE, self.__OPEN_KERNEL_SIZE))
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        return binary

    def character_append(self, stroke):
        self.character.append(stroke)

    def character_clear(self):
        self.character.clear()

    def character_remove_end(self):
        self.character = self.character[:-1]

    def draw_character(self):
        canvas = np.zeros((self.height, self.width, 3), np.uint8)
        canvas.fill(255)

        for i in range(0, len(self.character)):
            Stroke.draw_stroke(self.character[i], canvas)

        return canvas

    def recognize_character(self):
        canvas = np.zeros((self.height, self.width, 3), np.uint8)
        canvas.fill(255)

        for i in range(0, len(self.character)):
            Stroke.draw_stroke(self.character[i], canvas)

        canvas = self.__image_process(canvas)
        text = pyt.image_to_string(canvas)

        return text


stroke_1 = Stroke()
stroke_1.stroke_append((1, 1))
stroke_1.stroke_append((88, 74))
stroke_1.stroke_append((378, 203))
stroke_2 = Stroke()
stroke_2.stroke_append((350, 40))
stroke_2.stroke_append((200, 139))
stroke_2.stroke_append((30, 409))
character_1 = Character(500, 500)
character_1.character_append(stroke_1)
character_1.character_append(stroke_2)
canvas = character_1.draw_character()
cv2.imshow("canvas", canvas)
cv2.waitKey(500)
print(character_1.recognize_character())
