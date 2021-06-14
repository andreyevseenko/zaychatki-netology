# -*- coding: utf-8 -*-
import csv
import numpy
from keras.models import Sequential, load_model
from keras.layers import Dense
from flask import Flask, request, render_template, Markup
app = Flask(__name__)

SPEC_COUNT = 1822
SKLS_COUNT = 1667


def get_best_vacancy(skls, dataset, your_skills):
    max_score = 0
    best_vacancy = 0
    for row in dataset:
        score = 0
        vacancy_score = 0
        for i in row[1:]:
            vacancy_score = vacancy_score + 1
            if skls[round(float(i) * SKLS_COUNT)] != "NOT A SKILL":
                for j in your_skills:
                    if skls[round(float(i) * SKLS_COUNT)] == j:
                        score = score + 1
        if max_score < score / vacancy_score:
            max_score = score / vacancy_score
            best_vacancy = row[0]
    return float(best_vacancy)
    #specs[round(float(best_vacancy) * SPEC_COUNT)]


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/test', methods=['POST', 'GET'])
def test():
    f = open('./static/SPECIALTIES.csv', encoding='utf8')
    specialties = f.read().split(";")
    f.close()

    f = open('./static/SKILLS.csv', encoding='utf8')
    skills = f.read().split(";")
    f.close()

    if request.values.get('model') != '0':
        file = open("./static/DATASET.csv")
        reader = csv.reader(file, delimiter=';')
        rows = []
        for temp_row in reader:
            rows.append(temp_row)
        file.close()
        my_skills = request.values.get('skills').split(",")
        my_skills_without_spaces = []
        for i in my_skills:
            my_skills_without_spaces.append(i.strip(" "))
        my_uppercased_skills = []
        for i in my_skills_without_spaces:
            my_uppercased_skills.append(i.upper())
        best_vacancy = get_best_vacancy(skills, rows, my_uppercased_skills)
        found_skills = []
        for i in rows:
            for j in i[:1]:
                if float(j) == best_vacancy:
                    print(i[1:])
                    found_skills = i[1:]
        result = ""
        for i in found_skills:
            if float(i) != 1.0:
                if my_uppercased_skills.count(skills[round(float(i) * SKLS_COUNT)]) == 0:
                    result = result + "<a href=\"#\">" + skills[round(float(i) * SKLS_COUNT)] + "</a><br><br>"
        return render_template('result.html', spec=specialties[round(best_vacancy * SPEC_COUNT)], skls=Markup(result))

    dataset = numpy.loadtxt("DATASET.csv", delimiter=";")
    # разбиваем датасет на матрицу параметров (X) и вектор целевой переменной (Y)
    X, Y = dataset[:, 1:31], dataset[:, 0:1]

    model = load_model("model")

    my_skills = request.values.get('skills').split(",")
    my_skills_without_spaces = []
    for i in my_skills:
        my_skills_without_spaces.append(i.strip(" "))
    if len(my_skills_without_spaces) < 30:
        for i in range(30 - len(my_skills_without_spaces)):
            my_skills_without_spaces.append(skills[len(skills) - 1])
    prepared_skills = [[]]
    for i in my_skills_without_spaces:
        if skills.count(i) == 0:
            prepared_skills[0].append((len(skills) - 1) / SKLS_COUNT)
        else:
            prepared_skills[0].append(skills.index(i) / SKLS_COUNT)

    preds = model.predict(prepared_skills)
    return render_template('result.html', spec=specialties[round(preds[0][0] * SPEC_COUNT)], skls="TEST")


if __name__ == '__main__':
    app.run()
