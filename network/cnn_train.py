# -*- coding: utf-8 -*-
# this network is just a piece of shit, but yet, it works fine
# trying to use some more advanced and efficient networks
# networks will be changed once the newest edition of MobileFaceNet @tencent, ncnn be published
from keras.models import Sequential
from keras.layers import Convolution2D, BatchNormalization, Activation, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from network.depthwise_conv import DepthwiseConvolution2D
from set_gpu import get_session
import keras.backend.tensorflow_backend as KTF


KTF.set_session(get_session())

# init the model
model = Sequential()

model.add(Convolution2D(32, (3, 3), strides= (2 ,2), input_shape=(224, 224, 3), padding='same', use_bias=False))
model.add(BatchNormalization())
model.add(Activation('relu'))

model.add(DepthwiseConvolution2D(32, (3, 3), strides= (1, 1), padding= 'same', use_bias= False))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Convolution2D(64, (1, 1), strides= (1, 1), padding= 'same', use_bias= False))
model.add(BatchNormalization())
model.add(Activation('relu'))

model.add(DepthwiseConvolution2D(64, (3, 3), strides= (2, 2), padding= 'same', use_bias= False))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Convolution2D(128, (1, 1), strides= (1, 1), padding= 'same', use_bias= False))
model.add(BatchNormalization())
model.add(Activation('relu'))

model.add(DepthwiseConvolution2D(128, (3, 3), strides= (1, 1), padding= 'same', use_bias= False))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Convolution2D(128, (1, 1), strides= (1, 1), padding= 'same', use_bias= False))
model.add(BatchNormalization())
model.add(Activation('relu'))

model.add(DepthwiseConvolution2D(128, (3, 3), strides= (2, 2), padding= 'same', use_bias= False))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Convolution2D(256, (1, 1), strides= (1, 1), padding= 'same', use_bias= False))
model.add(BatchNormalization())
model.add(Activation('relu'))

model.add(DepthwiseConvolution2D(256, (3, 3), strides= (1, 1), padding= 'same', use_bias= False))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Convolution2D(256, (1, 1), strides= (1, 1), padding= 'same', use_bias= False))
model.add(BatchNormalization())
model.add(Activation('relu'))

model.add(DepthwiseConvolution2D(256, (3, 3), strides= (1, 1), padding= 'same', use_bias= False))
model.add(Flatten())
model.add(Dense(units = 4, activation = 'softmax'))

# compile
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


# Now generate training and test sets from folders
train_datagen = ImageDataGenerator(rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.,
                                   horizontal_flip=False)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory("Dataset/training_set",
                                                 target_size=(224,224),
                                                 color_mode='rgb',
                                                 batch_size=10,
                                                 class_mode='categorical')

test_set = test_datagen.flow_from_directory("Dataset/test_set",
                                            target_size=(224, 224),
                                            color_mode='rgb',
                                            batch_size=10,
                                            class_mode='categorical')

model.fit_generator(training_set,
                    steps_per_epoch=1956,
                    nb_epoch=10,
                    validation_data=test_set,
                    nb_val_samples=320)


# saving the weights
model.save_weights("weights.hdf5", overwrite=True)


# saving the model itself in json format:
model_json = model.to_json()
with open("model.json", "w") as model_file:
    model_file.write(model_json)
print("Model has been saved.")







