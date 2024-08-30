from Config import Config
from llm import generate_response, rate_reply

import os
import json

lenQuestions = 0
questions = {}

def calculate():
    results = []
    global questions
    questions = load_document_json(Config.DATA_FILE)
    global lenQuestions
    lenQuestions = len(questions)
    #print(questions)
    modelId=-1
    for model in Config.MODELS:
        modelId = modelId + 1
        modelName = model['stable']+ ' - ' + model['model']
        print("--------------------------------------------------------------------")
        print(f"--------- {modelName}")
        print("--------------------------------------------------------------------")
        results.append([modelId,model['stable'],model['model'],0])

        for question in questions:
            for i in range(Config.NUMBER_OF_REPETITIONS):
                myReq = question['question']
                myRes = generate_response(model['stable'], model['model'], myReq)
                rate = rate_reply(question['question'], myRes, question['verification'])
                if (rate==0):
                    print("-------------------------------------------------------------------------------------------")
                    print(question['verification'].replace("{modelAnswer}", myRes))
                    print("-------------------------------------------------------------------------------------------")
                results[modelId][3] += rate
                print(results)

    results.sort(key=lambda x: x[3], reverse=True)
    return results


def load_document_json(file: str):
    file_path = os.path.join(Config.DATA_PATH, file)
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    documents = []
    for item in data['questions']:
        documents.append({'question':  item['question'], 'verification': item['verification']})
    return documents


def report(results):
    maxPoints = lenQuestions * Config.NUMBER_OF_REPETITIONS
    with open("README.md", "w", encoding="utf-8") as file:
        file.write("# Test 'rozumienia' języka polskiego przez wybrane modele LLM\n\n")

        file.write(f"Liczba pytań: {lenQuestions}\n\n")
        file.write(f"Liczba powtórzeń jednego pytania: {Config.NUMBER_OF_REPETITIONS}\n\n")

        file.write("| Platforma | Model LLM | Wynik (%) |\n")
        file.write("|-----------|-----------|--------|\n")
        for item in results:
            percent = round((100*item[3])/maxPoints)
            file.write(f"|{item[1]}|{item[2]}|{percent} %|\n")

        file.write("\n\n")

        file.write("### Pytania:\n\n\n")
        for question in questions:
            file.write("---\n")
            file.write(question['question'])
            file.write("\n\n")


def main():
    res = calculate()
    report(res)

if __name__ == "__main__":
    main()