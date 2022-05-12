import tensorflow as tf
import csv
from keras.models import Sequential
from keras.layers import Dense
from MatchExample import MatchExample

"""
Juan Francisco Patino

Professional soccer game result neural network

features: #TODO

labels: home win, draw, away win, no bet

//label as "no bet" if obvious upset

"""

# control

matchExamples = []  # array of match example objects
label_names = []

features = 0  # determined after reading in CSV
number_of_examples = 0  # determined after reading in CSV
max_second_dim = 0
input_shape = (number_of_examples, 1)


def fromCSV():
    global number_of_examples
    global features
    global matchExamples
    global max_second_dim

    with open('MatchExamples - Soccer.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        x = 0
        for row in reader:
            if x < 2:  # ignore first two rows
                if x == 1:
                    y = 0
                    for col in row:
                        if y < 5:
                            y = y + 1
                            continue
                        label_names.append(col)
                x = x + 1
                continue
            else:
                features = row.__len__() - 5
                number_of_examples = number_of_examples + 1
                this_match_attributes = []
                y = 0
                for col in row:
                    if y < 5:
                        y = y + 1
                        continue
                    else:

                        val = int(col).__abs__()
                        this_match_attributes.append(val)
                        if val > max_second_dim:
                            max_second_dim = val

                if row[0] == '1':
                    label = 0
                elif row[1] == '1':
                    label = 1
                elif row[2] == '1':
                    label = 2
                else:
                    label = 3

                this_match = MatchExample(this_match_attributes, label, row[4])
                matchExamples.append(this_match)


def train_then_predict():
    global features
    global input_shape

    # todo: input layer
    model = Sequential()
    model.add(Dense(features * 3 / 2, input_shape=input_shape, activation='relu'))
    model.add(Dense(features * 3 / 2, activation='relu'))
    model.add(Dense(4, activation='sigmoid'))

    print(model.summary())

    inputList = []
    output = []

    for m in matchExamples:
        inputList.append(m.getFeatures())
        output.append(m.getLabel())

    model.fit(inputList, output, 1, 10)

    predict_att = []

    for s in label_names:
        p = input("Insert value (0 - " + max_second_dim.__str__() + ") For: " + s)
        predict_att.append(p)


if __name__ == '__main__':
    fromCSV()
    train_then_predict()

