# -*- coding: utf-8 -*-
"""M515Y1092_ERIN_NLP1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ms0Uwz2TH3SQZOAorMWO-9JLHozCbY_S

Nama : Erin Nur Fatimah

Alamat : RT 003 Sindet, Wukirsari, Imogiri, Bantul, Yogyakarta

TTL: Bantul, 25 Januari 2002

Perguruan Tinggi: Universitas Teknologi Digital Indonesia

Jurusan : D3-Rekayasa Perangkat Lunak Aplikasi

Nomor WhatsApp : 083149731170

Email : 203110024@students.akakom.ac.id

data set dari link https://www.kaggle.com/datasets/atulanandjha/imdb-50k-movie-reviews-test-your-bert
"""

from google.colab import drive

drive.mount('/content/drive')

import pandas as pd

data = pd.read_csv('/content/drive/MyDrive/data set/data set proyek 2/train.csv')

data = pd.read_csv('/content/drive/MyDrive/data set/data set proyek 2/test.csv')

data.head()

category = pd.get_dummies(data.sentiment)
data_baru = pd.concat([data, category], axis=1)
data_baru = data_baru.drop(columns='sentiment')
data_baru

from sklearn.model_selection import train_test_split

text = data_baru['text'].values
label = data_baru[['pos','neg']].values
text_train , text_test, label_train, label_test = train_test_split(text, label, test_size=0.2)

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

tokenizer = Tokenizer(num_words=280617, oov_token='-')
tokenizer.fit_on_texts(text_train)
tokenizer.fit_on_texts(text_test)

seq_train = tokenizer.texts_to_sequences(text_train)
seq_test = tokenizer.texts_to_sequences(text_test)

pad_train = pad_sequences(seq_train,
                          maxlen=300,
                          padding='post',
                          truncating='post')

pad_test = pad_sequences(seq_test,
                         maxlen=300,
                         padding='post',
                         truncating='post')

from tensorflow.keras import layers
from tensorflow.keras import Sequential

model = Sequential([layers.Embedding(280617, 64, input_length=300),
                    layers.LSTM(64, dropout=0.1),
                    layers.Dense(128, activation='relu'),
                    layers.Dense(64, activation='relu'),
                    layers.Dense(2, activation='sigmoid')])
model.summary()

import tensorflow as tf

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

num_epochs = 10
history = model.fit(pad_train, label_train, epochs=num_epochs, 
                    validation_data=(pad_test, label_test), verbose=2)