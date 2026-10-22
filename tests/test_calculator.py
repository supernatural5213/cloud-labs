import pytest
from index import app, calculate


def test_average_and_pass():
    r = calculate("Иван", 85, 90, 86)
    assert r["average"] == 87.0 and r["result"] == "PASS"


def test_fail_below_50():
    assert calculate("Анна", 40, 50, 45)["result"] == "FAIL"


def test_boundary_50_is_pass():
    assert calculate("Али", 50, 50, 50)["result"] == "PASS"


@pytest.mark.parametrize("bad", [-1, 101, "abc", ""])
def test_invalid_scores(bad):
    with pytest.raises(ValueError):
        calculate("X", bad, 50, 50)


def test_empty_name():
    with pytest.raises(ValueError):
        calculate("  ", 50, 50, 50)


def test_http_form_and_api():
    c = app.test_client()
    html = c.post("/", data={"name": "Иван", "t1": "85", "t2": "90", "exam": "86"}).get_data(as_text=True)
    assert "87.0" in html and "PASS" in html
    r = c.get("/api/calculate?name=A&t1=10&t2=20&exam=30")
    assert r.get_json()["result"] == "FAIL"
    assert c.get("/api/calculate?name=A&t1=200&t2=0&exam=0").status_code == 400
