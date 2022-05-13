import tensorflow as tf
import csv
import keras.models
from keras.layers import Dense
from MatchExample import MatchExample

"""
Juan Francisco Patino

Professional soccer game result neural network

features: #TODO

labels: home win, draw, away win, no bet

//label as "no bet" AS WELL if obvious upset

"""

# control

matchExamples = []  # array of match example objects
attribute_names = []

features = 0  # determined after reading in CSV
number_of_examples = 0  # determined after reading in CSV
max_second_dim = 0
input_shape = (number_of_examples, features)


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
                        attribute_names.append(col)
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

                        val = float(col).__abs__()
                        this_match_attributes.append(val)
                        if val > max_second_dim:
                            max_second_dim = val

                thisLabel = []

                if row[0] == '1':  # home win
                    thisLabel.append(1)
                else:
                    thisLabel.append(0)
                if row[1] == '1':  # draw
                    thisLabel.append(1)
                else:
                    thisLabel.append(0)
                if row[2] == '1':  # away win
                    thisLabel.append(1)
                else:
                    thisLabel.append(0)
                if row[3] == '1':  # no bet
                    thisLabel.append(1)
                else:
                    thisLabel.append(0)

                this_match = MatchExample(this_match_attributes, thisLabel, row[4])
                matchExamples.append(this_match)


def train_then_predict():
    global features
    global input_shape

    input_shape = (None, number_of_examples, features)
    model = keras.models.Sequential()

    ratio = float(input("Ratio of hidden layer size to input layers? (i.e., 1.5)"))

    hiddenLayerSize = int(features * ratio)

    model.add(Dense(hiddenLayerSize, input_shape=input_shape, activation='relu'))

    h = input("How many (more) hidden layers?")

    for x in range(int(h)):
        model.add(Dense(hiddenLayerSize, activation='relu'))

    model.add(Dense(hiddenLayerSize, activation='relu'))
    model.add(Dense(4, activation='sigmoid'))

    print(model.summary())

    inputList = []
    output = []

    for m in matchExamples:
        inputList.append(m.getFeatures())
        output.append(m.getLabel())

    model.compile(optimizer='Adagrad', loss=tf.keras.losses.BinaryCrossentropy(from_logits=True))

    epochs = int(input("Number of epochs?"))

    model.fit(inputList, output, number_of_examples, epochs)

    predict_att = []

    i = input("Predict single match? (y/n)")

    if i == 'y':
        single = True
        ii = input("input manually or file? (m/f)")

        if ii == 'm':
            for s in attribute_names:
                p = input("Insert value (0 - " + max_second_dim.__str__() + ") For: " + s)
                predict_att.append(float(p))
        else:
            iii = input("Name of file?")
            f = open(iii, "r")
            for line in f:
                for row in line.split(','):
                    predict_att.append(float(row))

        predictions = [predict_att]

    else:  # todo: Predict a batch of matches
        single = False
        predictions = []

    res = model.predict(predictions)

    results = []

    for o in res:
        count = 0
        largest = 0.0
        largestIdx = 0
        for p in o:
            if p > largest:
                largest = p
                largestIdx = count
            count = count + 1

        noBetRatio = o[3]/o[largestIdx]

        if largestIdx == 0:
            results.append("Home win (" + str(1/o[0] * 100) + "%) with 'no bet' of " + str(noBetRatio * 100) + "%")
        if largestIdx == 1:
            results.append("Draw (" + str(1/o[1] * 100) + "%) with 'no bet' of " + str(noBetRatio * 100) + "%")
        if largestIdx == 2:
            results.append("Away win (" + str(1/o[2] * 100) + "%) with 'no bet' of " + str(noBetRatio * 100) + "%")
        if largestIdx == 3:
            results.append("No bet. (" + str(1/o[3]*100) + ")")

    if single:
        print("Prediction: " + results[0])
    else:
        xx = 123  # todo


if __name__ == '__main__':
    fromCSV()
    train_then_predict()
