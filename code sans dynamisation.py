import nltk
from nltk.stem.snowball import FrenchStemmer
stemmer = FrenchStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle

with open("D:\\Projet enjeu\\intents.json", encoding="utf-8-sig") as file:
    data = json.load(file, strict=False)
    
words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern, language='french')
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])
    if intent["tag"] not in labels:
        labels.append(intent["tag"])
words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []
    wrds = [stemmer.stem(w.lower()) for w in doc]
    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = numpy.array(training)
output = numpy.array(output)

with open("data.pickle", "wb") as f:
    pickle.dump((words, labels, training, output), f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 65)
net = tflearn.fully_connected(net, 65)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
"""
model.fit(training, output, n_epoch=5000, batch_size=8, show_metric=True)
model.save("D:\\Projet enjeu\\model.tflearn")
"""
model.load("D:\\Projet enjeu\\model.tflearn")
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s, language='french')
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)

def chat(inp):
    results = model.predict([bag_of_words(inp, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    for tg in data["intents"]:
        if tg['tag'] == tag:
                responses = tg["responses"] 
    if numpy.max(results) < 0.59 :
        r= "je ne sais pas"
    else:
        r=random.choice(responses)
        print(numpy.max(results))
    return (r)     
#Creating GUI with tkinter
import tkinter
from tkinter import *
def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        res = chat(msg)
        if res=="je ne sais pas":
            ChatLog.insert(END, "Bot: " + res + '\n\n')
        else :
            ChatLog.insert(END, "Bot: " +'\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        return res

base = Tk()
base.title("Comprendre la mécanique quantique")
base.geometry("700x700")
base.resizable(width=FALSE, height=FALSE)
base.iconbitmap(r'D://projet enjeu//kuroko.ico')

#define exit function
def close_main():
    base.destroy()
    #exit()


#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)                       
#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set
                       
#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command=send )
#exit button
ExitButton=Button(base,font=("Verdana",12,'bold'),text="Exit",width="12",height=5,
                    bd=0, bg="#000000", activebackground="#3c9d9b",fg='#ffffff',command=close_main)
#Create the box to enter message
EntryBox = Text(base, bd=0,bg="white",width="29", height="5", font="Arial")
#create a label
label= Label(base,text="Comprendre la mecanique quantique",bg="black",fg="white",font="none 12 bold")
#EntryBox.bind("<Return>", send)
#create a photo1
res=send()
photo1=PhotoImage(file=res)
pho1=Label(base,image=photo2,bg="white")
#create a photo2
photo2=PhotoImage(file="chat.gif")
pho2=Label(base,image=photo3,bg="white")
#Place all components on the screen
label.place(x=200,y=0, height=40, width=329)
scrollbar.place(x=680,y=41, height=570)
ChatLog.place(x=6,y=41, height=100, width=673)
pho1.place(x=6,y=141, height=470, width=673)
EntryBox.place(x=128, y=610, height=90, width=482)
pho2.place(x=610,y=610, height=90, width=90)
SendButton.place(x=6, y=610, height=45)
ExitButton.place(x=6, y=655, height=45)
base.mainloop()


