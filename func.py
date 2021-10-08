import csv
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# print(getQuestion('13.2.187'))

def getAnswerInArray(answerarray: str):
    answ = []
    if answerarray.find('A.') >= 0 and answerarray.find('B.') > 0:
        answ.append(answerarray[answerarray.find('A.'):answerarray.find('B.')])
    if answerarray.find('C.') == -1 and answerarray.find('B.') > 0:
        answ.append(answerarray[answerarray.find('B.'):])
    elif answerarray.find('C.') > 0:
        answ.append(answerarray[answerarray.find('B.'):answerarray.find('C.')])
    if answerarray.find('D.') == -1 and answerarray.find('C.') > 0:
        answ.append(answerarray[answerarray.find('C.'):])
    elif answerarray.find('D.') > 0:
        answ.append(answerarray[answerarray.find('C.'):answerarray.find('D.')])
    if answerarray.find('E.') == -1 and answerarray.find('D.') > 0:
        answ.append(answerarray[answerarray.find('D.'):])
    elif answerarray.find('E.') > 0:
        answ.append(answerarray[answerarray.find('D.'):answerarray.find('E.')])
        answ.append(answerarray[answerarray.find('E.'):])

    return answ


def parseAnswer():
    answers = []

    with open('answ.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            answers.append(row)
    return answers


answers = parseAnswer()


# получить верный ответ
def getAnswer(question_number: str):
    answer = ''
    for i in answers:
        if i[1] == question_number:
            answer = i[2]
            break
        else:
            answer = 'Answer was not found!'
    return answer


def parseQuestions():
    questions = []

    with open('questions.txt', 'r') as file:
        data = file.read().replace('\n', ' ')
        ques = data.split('КОД ')
        ques.pop(0)

    for qi in ques:
        q = qi.replace(' ВОПРОСА: ', '').split('Ответы:')
        if len(q) < 2:
            print(qi)
        z = q[0].split(' ', 1)
        z.append(getAnswerInArray(q[1]))
        z.append(z[0].replace(' ', '').split('.'))
        z.append(getAnswer(z[0]))
        questions.append(z)
    return questions


questions = parseQuestions()


# print(questions[5])


# получить вопрос
def getQuestion(question_number: str):
    quest = []
    for i in questions:
        if i[0] == question_number:
            quest = i
            break
        else:
            # print(i[0])
            quest = 'Question was not Found!'
    return quest


# кол-во баллов
def getScore(question_number: str, result: bool):
    if result:
        score = question_number.split('.')[1]

    else:
        score = 0
    return int(score)


# print(getScore('13.2.187', False) )

# кол-во баллов. Верно - стоимость вопроса. 0 - неверно
def voteQuestion(question_number: str, answer: str, total_score: int):
    res_description = ''

    if getAnswer(question_number) == answer:
        res = True
        res_description = 'Верно!'
        total_score = total_score + getScore(question_number, res)
        scor_ball = getScore(question_number, True)
    else:
        res = False
        res_description = 'Неверно!' + ' Верный ответ: ' + getAnswer(question_number)
        scor_ball=getScore(question_number, True)
    return [res_description, scor_ball, total_score]


# кол-во и бальность вопросов
questions4test = [
    {'chapter': 1, '1b': 6, '2b': 2},
    {'chapter': 2, '1b': 6, '2b': 2},
    {'chapter': 3, '1b': 6, '2b': 2},
    {'chapter': 4, '1b': 5, '2b': 2},
    {'chapter': 5, '1b': 4, '2b': 0},
    {'chapter': 6, '1b': 4, '2b': 0},
    {'chapter': 7, '1b': 10, '2b': 0},
    {'chapter': 8, '1b': 6, '2b': 2},
    {'chapter': 9, '1b': 3, '2b': 1},
    {'chapter': 10, '1b': 4, '2b': 3},
    {'chapter': 11, '1b': 4, '2b': 0},
    {'chapter': 12, '1b': 5, '2b': 1},
    {'chapter': 13, '1b': 3, '2b': 2}]
# print(questions4test[0]['1b'])

# Проходной балл, 80%
# 80
allowScore = 80
# Количество баллов в тесте
# 100
ScoreInTicket = 100

# Количество вопросов в тесте
# 83
QuestionInTicket = 83


def getRandomQuestion():
    random_q = random.choice(questions)
    return random_q


def getScoreFromQ(somearray):
    return somearray[0].split('.')[1]


def getChapterFromQ(somearray):
    return somearray[0].split('.')[0]


# print(getRandomQuestion())
# Вопросы по главе
def getQuestionsByChapter(chapter: int, oneballquestion: int, twoballquestion: int):
    random_q = []
    allquestioninchapter_q = []
    oneballQinChapter_q = []
    twoballQinChapter_q = []
    for i in questions:
        if i[3][0] == str(chapter):
            allquestioninchapter_q.append(i)

    for i in allquestioninchapter_q:
        if i[3][1] == '1':
            oneballQinChapter_q.append(i)
        if i[3][1] == '2':
            twoballQinChapter_q.append(i)

    while len(random_q) < oneballquestion + twoballquestion:
        for i in range(oneballquestion):
            random_q.append(random.choice(oneballQinChapter_q))
        if len(twoballQinChapter_q) > 0:
            for i in range(twoballquestion):
                random_q.append(random.choice(twoballQinChapter_q))

    return random_q


# Итоговый список вопросов
def getQuestionList4Answers():
    listOfQuestion = []
    tmplistOfQuestion = []
    for i in questions4test:
        tmplistOfQuestion.append(getQuestionsByChapter(i['chapter'], i['1b'], i['2b']))
    for i in tmplistOfQuestion:
        for j in i:
            listOfQuestion.append(j)

    return sorted(listOfQuestion, key=lambda x: random.random())


# print(getQuestionList4Answers())


# Random Question
def getRandomQuestion():
    random_q = random.choice(questions)
    return random_q

# for i in questions:
#  print(str(getScore(i[0], True)) +' -'+ i[0])
