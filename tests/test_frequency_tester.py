from types import SimpleNamespace
import pytest
import sys


class DummyTk:
    def title(self, t):
        pass
    def bind(self, *a, **kw):
        pass
    def mainloop(self):
        pass

class DummyWidget:
    def __init__(self, *a, **kw):
        pass
    def grid(self, *a, **kw):
        pass
    def config(self, *a, **kw):
        pass
    def delete(self, *a, **kw):
        pass

class DummyEntry(DummyWidget):
    def __init__(self, *a, textvariable=None, **kw):
        super().__init__(*a, **kw)
        self.textvariable = textvariable
    def delete(self, *a, **kw):
        if self.textvariable:
            self.textvariable.set('')

class DummyVar:
    def __init__(self):
        self._value = ''
    def get(self):
        return self._value
    def set(self, val):
        self._value = val

@pytest.fixture
def freq_tester(monkeypatch):
    monkeypatch.setattr('tkinter.Tk', DummyTk)
    monkeypatch.setattr('tkinter.Button', DummyWidget)
    monkeypatch.setattr('tkinter.Label', DummyWidget)
    monkeypatch.setattr('tkinter.Entry', DummyEntry)
    monkeypatch.setattr('tkinter.StringVar', DummyVar)

    class FakeArray:
        def astype(self, dtype):
            return self
        def __getitem__(self, item):
            return self
        def __mul__(self, other):
            return self
        __rmul__ = __mul__
        def __truediv__(self, other):
            return self

    class FakeNumpy:
        pi = 3.14159
        newaxis = None
        int16 = int
        def sin(self, x):
            return FakeArray()
        def arange(self, n):
            return FakeArray()
        def repeat(self, array, repeats, axis=None):
            return array

    fake_np = FakeNumpy()

    class FakeSound(SimpleNamespace):
        def play(self):
            pass
        def stop(self):
            pass

    class FakeSndArray(SimpleNamespace):
        numpy = fake_np
        def make_sound(self, arr):
            return FakeSound()

    class FakePygame(SimpleNamespace):
        def init(self):
            pass
        sndarray = FakeSndArray()

    fake_pygame = FakePygame()
    monkeypatch.setitem(sys.modules, 'pygame', fake_pygame)

    monkeypatch.setitem(sys.modules, 'numpy', fake_np)
    fake_pygame.sndarray.numpy = fake_np
    import importlib, os
    module_dir = os.path.dirname(os.path.dirname(__file__))
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)
    ft = importlib.import_module('FrequencyTester')
    importlib.reload(ft)
    return ft


def test_check_answer_increments_score(freq_tester, monkeypatch):
    ft = freq_tester
    ft.frequency = 500
    ft.tests_taken = 0
    ft.score = 0
    ft.answer_var.set('500')
    monkeypatch.setattr(ft, 'play_sound', lambda: None)
    ft.check_answer()
    assert ft.score == 1


def test_play_sound_sets_random_frequency(freq_tester, monkeypatch):
    ft = freq_tester
    monkeypatch.setattr(ft.random, 'choice', lambda seq: 123)
    monkeypatch.setattr(ft.time, 'sleep', lambda x: None)
    ft.play_sound()
    assert ft.frequency == 123
