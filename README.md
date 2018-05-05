# HAND INPUT 2

## Basic Info

​	This is code of my garduat design to build a hand input programm using deep learning networks and OCR. A fully functional version of this should be able to capture your hand and tracing it. Draw strokes of character in air with your finger and program can recognize it and print on the screen.

​	To use this code you`ll need:

​		**python3**

​		**tensorflow**

​		**keras**

​		**tesseract**

​		**opencv3**

​	All above is easy to apply to your computer no matter which operating system you are using now. You may need some other environment libraries but I think they are all based on python so you can install them easily. It will performance better if you have a graphic card. I used GTX1060 to train and test my networks and it`s a little bit slow, but nothing intolerable.

## Structure

​	Of coure, main code is in `main.py`

​	`HandDetection.py`and `HandRecognition.py` are two main part to detect you hand and recognize it. They are based on CNN, AlexNet for details.

​	`cnn_train.py`is used to generate your own database. Trained model will be saved in `.hdf5` and `.json` files.

## also

​	There will be some modification and adjustment in the future, but I doubt that i will spend much time on it. More than happy to have PR.