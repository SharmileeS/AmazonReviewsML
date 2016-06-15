import sys, getopt, json, timeit
from textblob.classifiers import NaiveBayesClassifier

# Global variables
review_list = []
# has  given % of dataset
training_data = []
# has rest given% of dataset
testing_data = []

def read_input_data(filepath):
    with open(filepath, 'r') as json_file:
        try:
            data = json.loads(json_file.read())
            for review in data:
                review_orientation = {}
                rating = review['overall']
                review_orientation['text'] = review['reviewText']
                if rating < 3:
                    review_orientation['label'] = 'neg'
                else:
                    review_orientation['label'] = 'pos'
                review_list.append(review_orientation)
        except ValueError:
            # decoding failed
            print "***Value Error. Check input json***"
            exit(0)

# Code to get the reviews and then move to test list
def fetch_and_store (training_list, test_list, train_percent):
    length = int((float(train_percent)/100)*len(review_list))
    for i in range(0, length):
        training_list.append(review_list[i])
    for i in range(length, len(review_list)):
        test_list.append(review_list[i])
    return

def train_sentiment_analysis(train_percent):
    with open('TrainFiles/training_' + str(train_percent) + '.json', 'r') as train_fp:
        cl = NaiveBayesClassifier(train_fp, format="json")
        return cl

def test_sentiment_analysis(train_percent,classifier):
    with open('TestFiles/testing_' + str(100-int(train_percent)) + '.json', 'r') as test_fp:
        test_data = json.loads(test_fp.read())
        final_res_list = []
        count = 0
        for data in test_data["reviews"]:
            res_dict = {}
            res_dict["text"] = data["text"]
            count += 1
            print count
            prob_dist = classifier.prob_classify(data["text"])
            res_dict["max_sentiment"] = prob_dist.max()
            res_dict["pos_est"] = round(prob_dist.prob("pos"), 2)
            res_dict["neg_est"] = round(prob_dist.prob("neg"), 2)
            final_res_list.append(res_dict)
    with open('stats_result.json', 'w') as write_res:
        json.dump(final_res_list, write_res, indent=4, sort_keys=True)
    classifier.show_informative_features()

def main(argv):
    source_path = ''
    train_percent = 75  # default
    try:
        opts, args = getopt.getopt(argv, "hs:p:", ["source=", "train_percent="])
    except getopt.GetoptError:
        print("textblob_sentiment.py -s <source_path> -p <train_percent>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("textblob_sentiment.py -s <source_path> -p <train_percent>")
            sys.exit()
        elif opt in ("-s", "--source"):
            source_path = arg
        elif opt in ("-p", "--percent"):
            train_percent = arg
    print("DEBUG: Source file is {filename}".format(filename=source_path))
    print("DEBUG: Training data percent is {train_percent}".format(train_percent=train_percent))

    read_input_data(source_path)
    fetch_and_store(training_data, testing_data, train_percent)
    print 'Dumping train and test files ...'
    with open('TrainFiles/training_' + str(train_percent) + '.json', 'w') as fp:
        json.dump(training_data, fp, indent=4, sort_keys=True)
    with open('TestFiles/testing_' + (str(100 - int(train_percent)) + '.json'), 'w') as fp:
        fp.write('{ "reviews":')
        json.dump(testing_data, fp, indent=4, sort_keys=True)
        fp.write('}')
    print 'Train and Testing files created ...'
    print 'Performing analysis with training data ...'
    start = timeit.default_timer()
    classifier = train_sentiment_analysis(train_percent)
    stop = timeit.default_timer()
    print 'Training took ' + str(stop - start) + " ..."
    print 'Calculating stats using testing data ...'
    start = timeit.default_timer()
    test_sentiment_analysis(train_percent, classifier)
    stop = timeit.default_timer()
    print 'Testing took ' + str(stop - start) + " ..."
    print 'Done !!!'
    return


# Calling main
if __name__ == "__main__":
    main(sys.argv[1:])


