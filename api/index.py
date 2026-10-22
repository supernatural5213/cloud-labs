"""Student Grade Calculator: PaaS-приложение (Flask) для ЛР1 по облачным ИС."""
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
PASS_MARK = 50

PAGE = """<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Student Grade Calculator</title>
<style>
 body{font-family:system-ui,Segoe UI,Roboto,sans-serif;background:#f4f6fb;margin:0;display:flex;justify-content:center;padding:32px 16px;color:#1d2433}
 .card{background:#fff;max-width:380px;width:100%;border-radius:12px;box-shadow:0 4px 18px rgba(0,0,0,.08);padding:24px}
 h1{font-size:20px;text-align:center;letter-spacing:.06em;margin:0 0 20px}
 label{display:flex;justify-content:space-between;align-items:center;margin:10px 0;font-weight:600}
 input{width:170px;padding:8px;border:1px solid #c9d1e0;border-radius:6px;font-size:15px}
 button{width:100%;margin-top:16px;padding:11px;border:0;border-radius:8px;background:#2d6cdf;color:#fff;font-size:16px;font-weight:700;cursor:pointer}
 .res{margin-top:20px;border-top:1px dashed #c9d1e0;padding-top:14px;font-size:17px}
 .pass{color:#1a7f37;font-weight:700}.fail{color:#c62828;font-weight:700}.err{color:#c62828}
 footer{margin-top:18px;font-size:12px;color:#7a8499;text-align:center}
</style></head><body><div class="card">
<h1>STUDENT CALCULATOR</h1>
<form method="post">
 <label>Name <input name="name" value="{{ v.name }}" required maxlength="60"></label>
 <label>Test 1 <input name="t1" type="number" min="0" max="100" step="any" value="{{ v.t1 }}" required></label>
 <label>Test 2 <input name="t2" type="number" min="0" max="100" step="any" value="{{ v.t2 }}" required></label>
 <label>Exam <input name="exam" type="number" min="0" max="100" step="any" value="{{ v.exam }}" required></label>
 <button type="submit">CALCULATE</button>
</form>
{% if error %}<div class="res err">{{ error }}</div>{% endif %}
{% if r %}<div class="res">
 <div>Student: <b>{{ r.name }}</b></div>
 <div>Average: <b>{{ r.average }}</b></div>
 <div>Result: <span class="{{ 'pass' if r.passed else 'fail' }}">{{ r.result }}</span></div>
</div>{% endif %}
<footer>Pass mark: {{ pass_mark }} · deployed on PaaS</footer>
</div></body></html>"""


def calculate(name, t1, t2, exam):
    """Возвращает словарь с результатом или выбрасывает ValueError."""
    name = (name or "").strip()
    if not name:
        raise ValueError("Введите имя студента")
    scores = []
    for label, raw in (("Test 1", t1), ("Test 2", t2), ("Exam", exam)):
        try:
            value = float(str(raw).replace(",", "."))
        except (TypeError, ValueError):
            raise ValueError(f"{label}: введите число")
        if not 0 <= value <= 100:
            raise ValueError(f"{label}: значение должно быть от 0 до 100")
        scores.append(value)
    average = round(sum(scores) / 3, 1)
    passed = average >= PASS_MARK
    return {"name": name, "scores": scores, "average": average,
            "passed": passed, "result": "PASS" if passed else "FAIL"}


@app.route("/", methods=["GET", "POST"])
def index():
    v = {"name": "", "t1": "", "t2": "", "exam": ""}
    r = error = None
    if request.method == "POST":
        v = {k: request.form.get(k, "") for k in v}
        try:
            r = calculate(v["name"], v["t1"], v["t2"], v["exam"])
        except ValueError as e:
            error = str(e)
    return render_template_string(PAGE, v=v, r=r, error=error, pass_mark=PASS_MARK)


@app.route("/api/calculate")
def api_calculate():
    a = request.args
    try:
        return jsonify(calculate(a.get("name"), a.get("t1"), a.get("t2"), a.get("exam")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    import os
    app.run(host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "8080")))
