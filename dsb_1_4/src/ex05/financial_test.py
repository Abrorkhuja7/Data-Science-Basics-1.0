# financial_test.py
import pytest
import financial

HTML_OK = """
<div class="row">
  <div class="column">Total Revenue</div>
  <div class="column">100</div>
  <div class="column">200</div>
</div>
"""

class Resp:
    def __init__(self, code, text=""):
        self.status_code = code
        self.text = text

class Session:
    def __init__(self, code=200, html=HTML_OK):
        self.headers = {}
        self._code = code
        self._html = html
        self._n = 0

    def get(self, url, allow_redirects=True):
        self._n += 1
        return Resp(200, "") if self._n == 1 else Resp(self._code, self._html)

def _patch(monkeypatch, code=200, html=HTML_OK):
    monkeypatch.setattr(financial.requests, "Session", lambda: Session(code, html))
    monkeypatch.setattr(financial.time, "sleep", lambda _: None)

def tot_rev_returns_tuple(monkeypatch):
    _patch(monkeypatch)
    out = financial.get_financial_data("AAPL", "Total Revenue")
    assert isinstance(out, tuple)

def tot_rev_is_correct_row(monkeypatch):
    _patch(monkeypatch)
    out = financial.get_financial_data("AAPL", "Total Revenue")
    assert out[0] == "Total Revenue" and out[1:] == ("100", "200")

def missing_field_raises(monkeypatch):
    _patch(monkeypatch, html='<div class="row"><div class="column">Other</div></div>')
    with pytest.raises(Exception):
        financial.get_financial_data("AAPL", "Total Revenue")
