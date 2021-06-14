import os
import json

SPEC_COUNT = 1822
SKLS_COUNT = 1667

# Собираем датасет

skills = []
specialties = []
for fl in os.listdir('./docs/vacancies'):
    f = open('./docs/vacancies/{}'.format(fl), encoding='utf8')
    jsonText = f.read()
    f.close()

    jsonObj = json.loads(jsonText)
    specialties.append(jsonObj["name"].upper())
    for i in jsonObj["key_skills"]:
        if skills.count(i["name"].upper()) == 0:
            skills.append(i["name"].upper())

skills.append("NOT A SKILL")
specialties.sort()

max_count = 0
for fl in os.listdir('./docs/vacancies'):
    f = open('./docs/vacancies/{}'.format(fl), encoding='utf8')
    jsonText = f.read()
    f.close()

    jsonObj = json.loads(jsonText)
    result = str(specialties.index(jsonObj["name"].upper()) / SPEC_COUNT)
    is_skills = False
    current_count = 0
    for i in jsonObj["key_skills"]:
        is_skills = True
        current_count = current_count + 1
        result = result + ";" + str(skills.index(i["name"].upper()) / SKLS_COUNT)
    for j in range(30-current_count):
        result = result + ";" + str((len(skills)-1) / SKLS_COUNT)
    if is_skills:
        #print(result)
        pass

csv_string = ""
for i in specialties:
    csv_string = csv_string + i + ";"

f = open('SPECIALTIES.csv', 'w', encoding='utf8')
f.write(csv_string)
f.close()

csv_string = ""
for i in skills:
    csv_string = csv_string + i + ";"

f = open('SKILLS.csv', 'w', encoding='utf8')
f.write(csv_string)
f.close()
