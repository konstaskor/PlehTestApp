import csv
import logging
import random

logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Проходной балл, 80%
# 80
allowScore = 80
# Количество баллов в тесте
# 100
ScoreInTicket = 100

# Количество вопросов в тесте
# 83
QuestionInTicket = 83
# кол-во и бальность вопросов
questions4test = [
    {'chapter': 1, 'topic': 'Глава 1. Рынок ценных бумаг', '1b': 6, '2b': 2},
    {'chapter': 2, 'topic': 'Глава 2. Участники рынка ценных бумаг. Инфраструктурные организации', '1b': 6, '2b': 2},
    {'chapter': 3, 'topic': 'Глава 3. Эмиссия ценных бумаг. Обращение финансовых инструментов', '1b': 6, '2b': 2},
    {'chapter': 4, 'topic': 'Глава 4. Институты коллективного инвестирования', '1b': 5, '2b': 2},
    {'chapter': 5, 'topic': 'Глава 5. Государственные ценные бумаги. Государственный долг', '1b': 4, '2b': 0},
    {'chapter': 6, 'topic': 'Глава 6. Гражданско-правовые основы ведения предпринимательской деятельности', '1b': 4, '2b': 0},
    {'chapter': 7, 'topic': 'Глава 7. Корпоративное право', '1b': 10, '2b': 0},
    {'chapter': 8, 'topic': 'Глава 8. Регулирование финансового рынка и надзор на финансовом рынке. Защита прав и законных интересов инвесторов на финансовом рынке', '1b': 6, '2b': 2},
    {'chapter': 9, 'topic': 'Глава 9. Административные правонарушения и уголовные преступления на финансовом рынке', '1b': 3, '2b': 1},
    {'chapter': 10, 'topic': 'Глава 10. Финансовая математика и статистика', '1b': 4, '2b': 3},
    {'chapter': 11, 'topic': 'Глава 11. Основы бухгалтерского учета и финансовой отчетности на финансовом рынке', '1b': 4, '2b': 0},
    {'chapter': 12, 'topic': 'Глава 12. Налогообложение на финансовом рынке', '1b': 5, '2b': 1},
    {'chapter': 13, 'topic': 'Глава 13. Мировой финансовый рынок', '1b': 3, '2b': 2}]


# кол-во баллов
def score(question_number: str):
    return int(question_number.split('.')[1])


class Dictionary:
    questions = []
    answers = []

    def parseAnswers(self):
        with open('answ.csv', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                self.answers.append(row)

    def parseQuestions(self):
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
            z.append(self.getAnswer(z[0]))
            self.questions.append(z)

    def __init__(self):
        self.parseAnswers()
        self.parseQuestions()
        #self.topics=questions4test
        logger.info(f"<Constructor {self.__class__} > ")

    # Получить верный ответ или нет
    def getAnswer(self, question_number: str):
        answer = ''
        for i in self.answers:
            if i[1] == question_number:
                answer = i[2]
                break
            else:
                answer = 'Answer was not found!'
        return answer

    # Проверка правильности
    def checkAnswer(self, question_number: str, answer: str):
        result = False
        if self.getAnswer(question_number) == answer:
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

    # isPassed = False

    def __init__(self, dic: list):
        self.questions = getQuestionList4Answers(dic)
        self.qsum = len(self.questions)
        self.rest_score = 100
        for i in self.questions:
            self.keyboard_available_button[i[0]] = ('A', 'B', 'C', 'D', 'E')[0:len(i[2])]
        self.qsum = len(self.questions)
        logger.info(f"<Constructor {self.__class__} > ")

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
        # Создаем словарь с вопросами и оветами
        self.globe_dictionary = Dictionary()
        logger.info(f"<Constructor {self.__class__} > ")
        # print(self.globe_dictionary.questions)

    def addUser(self, userid, dic: list):
        self.sessions[userid] = Questions(dic)
        logger.info(f"<Add Questions to {userid} > ")

    def return_sessions(self):
        return self.sessions


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


def getQuestionsByChapter(questions: list, chapter: int, oneballquestion: int, twoballquestion: int):
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
    # print(f"Chapter {chapter}: 1b:{len(oneballQinChapter_q)}  2b:{len(twoballQinChapter_q)}")

    while len(random_q) < oneballquestion + twoballquestion:
        for i in range(oneballquestion):
            random_q.append(random.choice(oneballQinChapter_q))

        if len(twoballQinChapter_q) > 0:
            for i in range(twoballquestion):
                random_q.append(random.choice(twoballQinChapter_q))
    # print(random_q)
    return random_q


# Итоговый список вопросов
def getQuestionList4Answers(questions: list):
    listOfQuestion = []
    tmplistOfQuestion = []
    for i in questions4test:
        tmplistOfQuestion.append(getQuestionsByChapter(questions, i['chapter'], i['1b'], i['2b']))
    # print(len(tmplistOfQuestion))
    for i in tmplistOfQuestion:
        for j in i:
            listOfQuestion.append(j)

    return sorted(listOfQuestion, key=lambda x: random.random())

# d = Dictionary()
# print(getQuestionList4Answers(d.questions))

# d=Dictionary()
# print(d.getAnswer('1.1.1'))
