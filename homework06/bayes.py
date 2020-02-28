from collections import Counter
from math import log

class NaiveBayesClassifier:

    def __init__(self, alpha):
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.dict_words_lables = Counter()
        self.numbers_words = Counter()
        self.lables_words = Counter()

        for ele, label in zip(X, y):
            for word in ele.split():
                self.dict_words_lables[word, label] += 1
                self.numbers_words[word] += 1
                self.lables_words[label] += 1
       
        self.dict_words_lables = dict(self.dict_words_lables)
        self.numbers_words = dict(self.numbers_words)
        self.labels_numbers = dict(Counter(y))

        self.label_procent = dict()
        for label in self.labels_numbers:
            self.label_procent[label] = self.labels_numbers[label] / len(y)
        
        self.word_procent = dict()
        for word in self.numbers_words:
            self.word_procent[word] = dict()
            for label in self.labels_numbers:
                self.word_procent[word][label] = (self.dict_words_lables.get((word, label), 0) + self.alpha) / (
                    self.labels_numbers[label] + self.alpha * self.numbers_words[word])
    
        return self.word_procent

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        predictions = []

        for item in X:
            max_procent = float('-inf')
            item_label = ''

            for label in self.label_procent:
                procent = log(self.label_procent[label])
                for word in item.split():
                    if word in self.word_procent and label in self.word_procent[word]:
                        procent += log(self.word_procent[word][label])

                if procent > max_procent:
                    max_procent = procent
                    label_to_give = label
            predictions.append(label_to_give)

        return predictions

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        predictions = self.predict(X_test)
        correct = 0

        for i in range(len(predictions)):
            if predictions[i] == y_test[i]:
                correct += 1
        return correct / len(y_test)
