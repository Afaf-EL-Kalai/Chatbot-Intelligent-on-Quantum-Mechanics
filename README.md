# Project Intelligent Chatbot

This is my first project about AI. I worked with other four collegemate to build an intelligent chatbot which purpose is to asses students in their learning of Quantum Mechanics.

This is a project about an intelligent chatbot using NLP and machine Learning.


## Dataset
I have created a dataset of 64 most important questions/answers about quantum Mechanics and then stored it in JSON file.

- The pdf version is named : Question&réponse_Mécanique quantique.pdf

- The JSON file version is named : intents-text.json

We have encountered a problem to read maths equations so we decided to convert every text-based answer into a screenshot and store the name of this image file in the JSON file.

- The JSON file version with images is named : intents-image.json
- The file containing images is named : images.rar

## Code
We first preprocessed our data which is the 'patterns', key of the json file, using methods of NLP : tokenization, stemming, and reming stopwords and punctuations. We convert it to a numeric array (vectorization) simply using the bag-of-words approach. We also creat a list of labels, in fact when a user inputs a question the model tries to predict the 'tag' or the label and then it outputs the corresponding 'responses'.

We create an user interface using Tkinter.


The file containing our code are code_chatbot_text.py and code_chatbot_image.py using the datasets intents-text.json and intents-image.json respectively.

# Result
Our chatbot seems to be performing well. But of course, only when we ask it questions related to quantum mechanics, and specially what it is covered by our dataset of 64 Questions/answers.
Even when inputing two questions differently formulated. It is also capable of outputing the correct answer even when the question contains spelling mistakes and punctuation.

-->See the presentation to vizualize some examples.







