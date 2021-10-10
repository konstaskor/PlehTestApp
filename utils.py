from random import random

import func


# кол-во баллов
def score(question_number: str):
    return int(question_number.split('.')[1])


# Проверка правильности
def checkAnswer(question_number: str, answer: str):
    result = False
    if func.getAnswer(question_number) == answer:
        result = True
    return result


class Questions:
    actual_question = ''
    total_score = 0
    rest_score = 0
    current_question = 0
    questions = []
    votes = []
    keyboard_available_button = {}
    qsum = 0
    isPassed = False

    def __init__(self):
        self.questions = func.getQuestionList4Answers()
        self.qsum = len(self.questions)
        self.rest_score = 100
        for i in self.questions:
            self.keyboard_available_button[i[0]] = ('A', 'B', 'C', 'D', 'E')[0:len(i[2])]
        self.qsum = len(self.questions)
        print(f"<Constructor {self.__class__} > ")

    # Сохранение голоса
    def vote(self, question_number: str, vote: str):
        self.votes.append({question_number: vote})

    #
    def return_questions(self):
        return self.questions


class Sessions:
    # sessions = {}  # [{'userid','экз Questions'}]

    def __init__(self):
        self.sessions = {}
        print(f"<Constructor {self.__class__} > ")

    def addUser(self, userid):
        self.sessions[userid] = Questions()
        print(f"<Add Questions to {userid} > ")

    def return_sessions(self):
        return self.sessions

# s=Sessions()
# #
# s.addUser(1234)
# if s.sessions.get(11) != None:
#     print('ok')
# else:
#     print('not ok')
