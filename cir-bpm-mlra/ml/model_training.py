import pandas as pd
import numpy as np
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import os

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv("/content/processed_bp_snapshot.csv")

X = df[["SBP","DBP","HR"]].values
y_map = {"Normal":0,"Alert":1,"Warning":2,"Emergency":3}
y = df["bp_label"].map(y_map).values

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

y_train = to_categorical(y_train,4)
y_test  = to_categorical(y_test,4)

model = models.Sequential([
    layers.Dense(64,activation="relu",input_shape=(3,)),
    layers.Dense(32,activation="relu"),
    layers.Dense(4,activation="softmax")
])

model.compile(optimizer="adam",loss="categorical_crossentropy",metrics=["accuracy"])
model.fit(X_train,y_train,epochs=40,validation_data=(X_test,y_test))
model.save(os.path.join(BASE_DIR, "SPMR_Model.h5"))
print("Model saved")