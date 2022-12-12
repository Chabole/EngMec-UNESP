# ---------------------------------------------------------------
# Script name : TensorFlow_mnist_my_image.py
# ---------------------------------------------------------------
# Train a CNN using Keras with the MNIST dataset and perform a
# prediction using a given image in a .png file.
# ---------------------------------------------------------------

# -------------------------------------------------------
# Modules to import
# -------------------------------------------------------

import tensorflow as tf
import matplotlib.pyplot as plt
import cv2

#from tensorflow import keras
#from tensorflow.keras import layers


# -------------------------------------------------------
# def main()
# -------------------------------------------------------

def main():

    # ---------------------------------------------------
    # Set-up
    # ---------------------------------------------------
    dataset = tf.keras.datasets.mnist
    model_dir = 'model_directory'
    no_of_epochs = 10

    # ---------------------------------------------------
    # Load the dataset
    # ---------------------------------------------------
    (x_train, y_train), (x_test, y_test) = dataset.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    print('>> Train: x=%s, y=%s' % (x_train.shape, y_train.shape))
    print('>> Test : x=%s, y=%s' % (x_test.shape, y_test.shape))

    # ---------------------------------------------------
    # Create the model
    # ---------------------------------------------------
    model = tf.keras.models.Sequential(
        [tf.keras.layers.Flatten(input_shape=(28, 28)),
         tf.keras.layers.Dense(units=512, activation='relu'),
         tf.keras.layers.Dropout(0.2),
         tf.keras.layers.Dense(10, activation='softmax')]
    )

    #model = keras.Sequential(
    #    [
    #        keras.Input(shape=(28, 28, 1)),
    #        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
    #        layers.MaxPooling2D(pool_size=(2, 2)),
    #        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
    #        layers.MaxPooling2D(pool_size=(2, 2)),
    #        layers.Flatten(),
    #        layers.Dropout(0.5),
    #        layers.Dense(10, activation="softmax"),
    #    ]
    #)

    # ---------------------------------------------------
    # Compile the model
    # ---------------------------------------------------
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # ---------------------------------------------------
    # Fit the model
    # ---------------------------------------------------
    history_callback = model.fit(
        x=x_train,
        y=y_train,
        epochs=no_of_epochs,
        validation_data=(x_test, y_test),
    )

    loss_history = history_callback.history['loss']
    accuracy_history = history_callback.history['accuracy']
    val_loss_history = history_callback.history['val_loss']
    val_accuracy_history = history_callback.history['val_accuracy']

    weights = model.get_weights()

    print(model.summary())
    print(weights)
    print('loss         = ', loss_history)
    print('accuracy     = ', accuracy_history)
    print('val_loss     = ', val_loss_history)
    print('val_accuracy = ', val_accuracy_history)

    # ---------------------------------------------------
    # Save the model
    # ---------------------------------------------------
    tf.keras.models.save_model(
        model,
        model_dir,
        overwrite=True,
        include_optimizer=True,
        save_format=None,
        signatures=None,
    )

    # ---------------------------------------------------
    # Evaluate the model
    # ---------------------------------------------------
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)

    print('Test Loss:     ', test_loss)
    print('Test Accuracy: ', test_acc)

    image_to_predict1 = cv2.imread('my_number_ex0_b.png')
    image_to_predict1_gray = cv2.cvtColor(image_to_predict1, cv2.COLOR_BGR2GRAY)
    gray_not = cv2.bitwise_not(image_to_predict1_gray)
    image_to_predict1_28x28 = cv2.resize(gray_not, (28, 28), interpolation=cv2.INTER_AREA) / 255.0

    print('-- Image to predict')
    print('Shape of image ', image_to_predict1_28x28.shape)

    predictions = model.predict(image_to_predict1_28x28.reshape(1, 28, 28))

    print(predictions)
    print('-- Predicted image')
    print('Most probable image ', tf.argmax(predictions[0]))

    # ---------------------------------------------------
    # Plot training results
    # ---------------------------------------------------
    loss_history = history_callback.history['loss']
    accuracy_history = history_callback.history['accuracy']
    val_loss_history = history_callback.history['val_loss']
    val_accuracy_history = history_callback.history['val_accuracy']

    epochs = tf.linspace(1, no_of_epochs, no_of_epochs)

    fig, axs = plt.subplots(1, 4, figsize=(10, 5))

    axs[0].plot(epochs, loss_history)
    axs[0].set_title('Training loss', fontsize=10)
    axs[0].set_xlabel('Epoch', fontsize=10)
    axs[0].set_ylabel('Loss', fontsize=10)
    axs[0].grid(True)
    axs[0].set_facecolor('palegreen')

    axs[1].plot(epochs, accuracy_history)
    axs[1].set_title('Training accuracy', fontsize=10)
    axs[1].set_xlabel('Epoch', fontsize=10)
    axs[1].set_ylabel('Accuracy', fontsize=10)
    axs[1].grid(True)
    axs[1].set_facecolor('palegreen')

    axs[2].plot(epochs, val_loss_history)
    axs[2].set_title('Validation loss', fontsize=10)
    axs[2].set_xlabel('Epoch', fontsize=10)
    axs[2].set_ylabel('Loss', fontsize=10)
    axs[2].grid(True)
    axs[2].set_facecolor('gainsboro')

    axs[3].plot(epochs, val_accuracy_history)
    axs[3].set_title('Validation accuracy', fontsize=10)
    axs[3].set_xlabel('Epoch', fontsize=10)
    axs[3].set_ylabel('Accuracy', fontsize=10)
    axs[3].grid(True)
    axs[3].set_facecolor('gainsboro')

    plt.suptitle('Model fitting statistics')
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)

    plt.show()


# -------------------------------------------------------
# Run only if source file is run as the main script
# -------------------------------------------------------

if __name__ == '__main__':
    main()

# ---------------------------------------------------------------
# End of file
# ---------------------------------------------------------------
