import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model("SPMR_Model.h5")

labels = ["Normal","Alert","Warning","Emergency"]

def predict_bp(sbp,dbp,hr):

    X = np.array([[sbp,dbp,hr]])

    pred = model.predict(X)

    index = np.argmax(pred)

    return labels[index]