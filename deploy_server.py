from flask import Flask, render_template, request, redirect
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
# from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import tempfile
import os

# loss_fn = tf.keras.losses.BinaryCrossentropy(from_logits=True)
# optimizer = tf.keras.optimizers.Adam()
# metrics = tf.keras.metrics.BinaryAccuracy()
# print('keras : ', keras.__version__)
app = Flask(__name__)
dic = {0 : 'Cat', 
       1 : 'Dog'}

model = load_model('model.h5')

def predict_label(image):
    # i = load_img(img_path, target_size = (122,122))
    # image = image.resize((224,224))
    i = img_to_array(image)/255.0
    i = i.reshape(1,224,224,3)
    p = model.predict(i)
    p = (p >= 0).astype(int)
    return dic[p[0][0]]


@app.route("/", methods = ['GET', 'POST'])
def index():
    return render_template('index.html', answer = None)

@app.route("/upload", methods = ['POST'])
def upload():
    img = request.files['image']

    # to not save the user input
    _, temp_file_path = tempfile.mkstemp() # when I dont want to save image but no display after upload also
    
    # to save the user input img
    # temp_file_path = 'static/' + img.filename

    img.save(temp_file_path)
    print(temp_file_path)

    # load the image from the file
    image = load_img(temp_file_path, target_size=(224, 224))
    #predict the label
    rst = predict_label(image)
    # pass the image path to the template
    img_path = os.path.basename(temp_file_path)

    #delete the user image
    # os.remove(temp_file_path)

    return render_template('index.html', answer = f"It's a {rst}.")#, img_path = img_path)

@app.route("/info", methods = ['GET', 'POST'])
def info():
    return render_template('info.html')

app.run(debug = True, port = 5003)