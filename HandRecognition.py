from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator


# define
confidence_threshold = 0.5
Not_Supported_Type = 0


def load_model():
    try:
        json_file = open('network/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)
        model.load_weights("network/weights.hdf5")
        print("Model successfully loaded from disk.")

        # compile again
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model
    except:
        print("""Model not found. Please train the CNN by running the script 
                 cnn_train.py. Note that the training and test samples should be properly 
                 set up in the dataset directory.""")
        return None


def recognition(img, model):
    img = img.reshape((1,) + img.shape)

    test_datagen = ImageDataGenerator(rescale=1. / 255)
    m = test_datagen.flow(img, batch_size=1)
    y_pred = model.predict_generator(m, 1)
    possibility = y_pred[0].max()
    result = list(y_pred[0]).index(y_pred[0].max())
    if possibility > confidence_threshold:
        return possibility, result
    else:
        return 0, Not_Supported_Type
