# AmazonReviewsML
A machine learning exercise on amazon reviews using NaiveBayesClassifier

<h2> How to use this project? </h2>
<p>The textblob_sentiment.py file can be run from PyCharm or a command line tool. Pass the sourcepath of file and the percent of 
training data (optionally) for splitting the given dataset as input to the program with proper flags. Use -h to get help on how to use.</p>

<h2> What does the program do? </h2>
<p>Based on the <i>Patio_Lawn_and_Garden_1000.json</i> input file format, the program extracts reviewText and overall ratings from the 
<i>Patio_Lawn_and_Garden_5.json</i> (the original dataset from <a href="jmcauley.ucsd.edu/data/amazon/">Product reviews</a> and gives
labels to the given data using overall rating (If rating > 3, set label as 'pos' else 'neg'). Next, it splits the extracted content to given <i> training_ <percent>.json </i> and <i> testing_ <percent>.json </i> files under the TrainFiles 
and TestFiles folder. It then calls the train_sentiment_analysis function and performs training using the NaiveBayesClassifier and gives
trainer classifier as output. It then calls the test_sentiment_analysis function and tests the data using this classifier, evaluates
pos/neg and gives the label distribution for each review - <i> stats_result.json </i>. The program also shows top informative features 
as an output - <i> features_information.txt </i> </p>
