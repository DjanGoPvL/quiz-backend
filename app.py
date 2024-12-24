from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Разрешаем запросы с других доменов

# Хранилище для тестов и ответов
tests = {}

@app.route("/create_test", methods=["POST"])
def create_test():
    data = request.json
    test_name = data.get("test_name")
    test_code = str(random.randint(100000, 999999))
    tests[test_code] = {"name": test_name, "results": []}
    return jsonify({"test_code": test_code})

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = request.json
    test_code = data.get("test_code")
    student_name = data.get("student_name")
    question = data.get("question")
    answer = data.get("answer")
    is_correct = data.get("is_correct")

    if test_code in tests:
        tests[test_code]["results"].append({
            "student_name": student_name,
            "question": question,
            "answer": answer,
            "is_correct": is_correct
        })
        return jsonify({"status": "success"})
    return jsonify({"error": "Test not found"}), 404

@app.route("/get_results/<test_code>", methods=["GET"])
def get_results(test_code):
    if test_code in tests:
        return jsonify(tests[test_code]["results"])
    return jsonify({"error": "Test not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
