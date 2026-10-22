"""ЛР4: тот же бизнес-сценарий (расчёт итоговой оценки) как serverless-функция (FaaS).
Вызов: GET /api/grade_fn?t1=85&t2=90&exam=86"""
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json, os, time

COLD = True                     # переменная модуля живёт, пока жив экземпляр функции
STARTED = time.time()


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global COLD
        q = parse_qs(urlparse(self.path).query)
        try:
            scores = [float(q[k][0]) for k in ("t1", "t2", "exam")]
            if not all(0 <= s <= 100 for s in scores):
                raise ValueError
            avg = round(sum(scores) / 3, 1)
            body, status = {"average": avg, "result": "PASS" if avg >= 50 else "FAIL"}, 200
        except (KeyError, ValueError):
            body, status = {"error": "t1, t2, exam: числа от 0 до 100"}, 400
        body["runtime"] = {"cold_start": COLD, "instance_age_s": round(time.time() - STARTED, 2),
                           "region": os.environ.get("VERCEL_REGION", "local"), "python": os.sys.version.split()[0]}
        COLD = False
        data = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(data)
