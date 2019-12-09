from django.shortcuts import render, redirect
from django import forms
# Create your views here.
from django.http import HttpResponse
from datetime import date
import calendar
from calendar import HTMLCalendar
from textblob.classifiers import NaiveBayesClassifier
import pandas as pd
import pickle
from django.conf import settings
import os
import random


class ContactForm(forms.Form):
    message_field = forms.CharField(label='Sentiment Analysis')


class MachineLearningModel:
    train = [
        ('I love this sandwich.', 'pos'),
        ('this is an amazing place!', 'pos'),
        ('I feel very good about these beers.', 'pos'),
        ('I am in such a good mood', 'pos'),
        ('We love new talent, with good vibes', 'pos'),
        ('Very easy to use tablet. Lots of apps and game available.', 'pos'),
        ('this is my best work.', 'pos'),
        ("what an awesome view", 'pos'),
        ("A beer after a long day is aboslutely great", "pos"),
        ('I am so happy, just got a new car', 'pos'),
        ('My best friend just proposes to his gf', 'pos'),
        ('Yayyy its friday, finally weekend time', 'pos'),
        ('Congratulations you just landed your first job', 'pos'),
        ('I do not like this restaurant', 'neg'),
        ('I am tired of this stuff.', 'neg'),
        ("I can't deal with this", 'neg'),
        ('he is my sworn enemy!', 'neg'),
        ('My girlfriend is so annoying sometimes', 'neg'),
        ("You're disgusting dude!", 'neg'),
        ("My friend is so disrespectul, you know", 'neg'),
        ('I ordered this thing, and it came late', 'neg'),
        ('Believe when i say they not the one', 'neg'),
        ('I absolutely hate spicy food', 'neg'),
        ('Today is going to be a very long day', 'neg'),
        ('I hate getting out of bed', 'neg')
    ]

    message = ""

    test = [
        ('the beer was good.', 'pos'),
        ('I do not enjoy my job', 'neg'),
        ("I ain't feeling dandy today.", 'neg'),
        ("I feel amazing!", 'pos'),
        ('Gary is a friend of mine.', 'pos'),
        ("I can't believe I'm doing this.", 'neg')
    ]
    classifier = NaiveBayesClassifier(train)

    def load_instance(self):
        f = open('my_classifier.pickle', 'rb')
        classifier = pickle.load(f)
        f.close()

    def save_instance(self):

        # On get, save the most recent model for later interogation
        f = open('my_classifier.pickle', 'wb')
        pickle.dump(self.classifier, f)
        f.close()

    def load_data(self, path):
        count = 0
        train = []
        df = pd.read_csv(path)
        for i in range(len(df)):
            if df.loc[i, "sentiment"] == 'positive':
                train.append((df.loc[i, "review"].replace("<br/>", "").replace("<br />", ""), 'pos'))
            else:
                train.append((df.loc[i, "review"].replace("<br/>", "").replace("<br />", ""), 'neg'))

            count += 1
            if count == 10000:
                break
        self.train += train

        return train

    def classify(self, input_data):
        prob_dist = self.classifier.prob_classify(input_data)
        x = prob_dist.max() + ""
        return x


def index(request, year=date.today().year, month=date.today().month):
    year = int(year)
    month = int(month)
    if year < 1900 or year > 2099:
        year = date.today().year
    month_name = calendar.month_name[month]
    title = "Welcome to Botza Sentiment Analysis- %s %s" % (month_name, year)
    cal = HTMLCalendar().formatmonth(year, month)
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'index.html', {'title': title, 'cal': cal})


def result(request):
    return render(request, "result.html")


def message(request):
    url = os.path.join(settings.BASE_DIR + '/sentiment_analysis/static/datasource/IMDBDataset.csv')

    ai = MachineLearningModel()
    # ai.load_instance()
    # ai.load_data(url)
    if request.method == 'POST':  # 0
        # Create a form instance with the submitted data
        message_field = request.POST['message_data']  # 1

        # Validate the form
        if not message_field == "":

            resultOutput = ai.classify(message_field)
            ai.save_instance()
            # If the form is valid, perform some kind of
            # operation, for example sending a message

            # After the operation was successful,
            # redirect to some other page
            response_pos = [
                "You're going to go through tough times - that's life. But I say, 'Nothing happens to you, it happens for you.' See the positive in negative events. Joel Osteen",
                "If you're not making mistakes, then you're not doing anything. I'm positive that a doer makes mistakes. John Wooden",
                "People deal too much with the negative, with what is wrong. Why not try and see positive "
                "things, to just touch those things and make them bloom? Thich Nhat Hanh",
                "You are the sum total of everything you've ever seen, heard, eaten, smelled, been told, forgot - it's all there. Everything influences each of us, and because of that I try to make sure that my experiences are positive. Maya Angelou",
                "I know it's cheesy but I'm sure you feel grate,"
                "How do horses greet others? Hayyy!!",
                "It sounds like someone woke up on the right side of the bed!"

                ]
            response_neg = [
                "My dad was a very quiet person, and unbelievably tough. But my grandmother gave me my first look at "
                "negative thinking to bring about positive results. When I was just a little guy, anytime I came to "
                "my grandmother and said I wish for this or that, Grandma would say, 'If wishes were horses, "
                "beggars would ride.'Bobby Knight",
                "What did the fruit say to the other fruit? We make a good pear",
                "Why are ghosts such bad liars? because they so transparent",
                "Why is Peter Pan always flying? He neverlands",
                "Your response was very negative is everything GENUINELY OKAY ?"
            ]
            pos_v = response_pos[random.randint(0, len(response_pos))]
            neg_v = response_neg[random.randint(0, len(response_neg))]
            return render(request, 'details.html',
                          {"title": resultOutput, "pos_response": pos_v, "neg_response": neg_v})
        else:
            return HttpResponse("I never reached the post method")
    return HttpResponse('Something went wrong')
