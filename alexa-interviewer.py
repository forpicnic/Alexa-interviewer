import json
import logging
import os
import time
import random
import requests
import re
import decimal
from random import randint

import boto3
from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, convert_errors


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def start():
    welcome_msg = 'Hi, I am your interviewer. What kind of interview would you like to mock up?'
    reprompt_msg = 'You can choose either job interview or custom interview.'
    return question(welcome_msg).reprompt(reprompt_msg)

@ask.intent("JobIntent")
def job():
    jobinfo_msg = 'In what company, what position would you like an interview?'
    reprompt_msg = 'You should say a position at a company.'
    return question(jobinfo_msg).reprompt(reprompt_msg)

@ask.intent("JobQuestionIntent")
def get_jobQuestions(company_name, position_name):
    job_msg = 'You want to mock an interview at {}, as a {}. I have processed the interview questions from Glassdoor and will take a random question from the pool. Are you ready?'.format(company_name, position_name)
    reprompt_msg = 'May I know are you ready?'
    return question(job_msg).reprompt(reprompt_msg)

@ask.intent("YesIntent")
def yes():
    url = ("https://s3.amazonaws.com/skill-interview/run_results.json")
    questions = requests.get(url).json()['interview_questions'][randint(0,9)]['question']
    msg = 'Ok, the question is, {}'.format(questions)
    return question(msg)

@ask.intent("NoIntent")
def end_round():
    bye_msg = 'Ok.'
    return question(bye_msg)

@ask.intent("NextIntent")
def next():
    url = ("https://s3.amazonaws.com/skill-interview/run_results.json")
    questions = requests.get(url).json()['interview_questions'][randint(0,9)]['question']
    msg = 'The next question is, {}'.format(questions)
    return question(msg).  

@ask.intent("CustomIntent")
def custom():
    url = ("https://s3.amazonaws.com/skill-interview/custom_questions.json")
    questions = requests.get(url).json()['interview_questions'][randint(0,9)]['question']
    custom_msg = "I have got your custom questions from your email. I will take a random question from the pool. Let's start.   {}.".format(questions)
    return question(custom_msg).

@ask.intent("AMAZON.StopIntent")
def stop():
    return statement('Stopping')

@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Goodbye")

@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':

    app.run(debug=True)
