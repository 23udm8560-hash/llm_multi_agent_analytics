import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from io import BytesIO
from analytics_system.data_processing.loader import load_csv


class FakeUpload:
    def getvalue(self):
        return b"a,b\n1,2\n3,4\n"


def test_load_csv():
    df = load_csv(FakeUpload())
    assert df.shape == (2, 2)
