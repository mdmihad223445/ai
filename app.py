# app.py - Core AI Engine
from flask import Flask, request, jsonify
from sympy import symbols, Eq, solve, simplify
import re

app = Flask(__name__)

class BangladeshSTEMAI:
    def __init__(self):
        self.math_keywords = ["solve", "integral", "derivative", "BdMO"]
        self.code_keywords = ["code", "program", "function"]

    def process(self, query):
        if any(kw in query.lower() for kw in self.math_keywords):
            return self._solve_math(query)
        elif any(kw in query.lower() for kw in self.code_keywords):
            return self._generate_code(query)
        else:
            return self._general_response(query)

    def _solve_math(self, problem):
        try:
            x = symbols('x')
            if "=" in problem:
                eq_str = problem.split("=")[0].strip() + "-(" + problem.split("=")[1].strip() + ")"
                solution = solve(eq_str, x)
                return f"Solution: {solution}"
            elif "integral" in problem:
                expr = re.search(r"integral of (.+?) with respect", problem).group(1)
                return f"Integral: {simplify(Integral(expr, x).doit())}"
            else:
                return "Ask math questions like: 'Solve x^2 - 4 = 0'"
        except:
            return "Could not solve. Try a clearer math problem."

    def _generate_code(self, prompt):
        if "prime" in prompt.lower():
            return '''def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True'''
        else:
            return "# Ask for specific code (e.g. 'Write a prime number checker')"

    def _general_response(self, query):
        responses = {
            "hello": "Hello! Ask me STEM questions in English or Bangla.",
            "hi": "Hi! I solve math/coding problems. Try: 'Solve x+5=9'",
            "help": "I can: 1) Solve math 2) Write code 3) Explain concepts"
        }
        return responses.get(query.lower(), "I specialize in STEM questions.")

ai = BangladeshSTEMAI()

@app.route('/api', methods=['POST'])
def api():
    query = request.json.get('query', '')
    return jsonify({"response": ai.process(query)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
