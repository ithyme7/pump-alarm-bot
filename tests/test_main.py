import os
import sys
from pathlib import Path
import pandas as pd

# Ensure the project root is on the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import create_chart, format_message, save_history


def test_save_history_and_chart(tmp_path):
    df = pd.DataFrame({'token_symbol': ['AAA', 'BBB'], 'total_volume_usd': [100, 200]})
    history = tmp_path / 'history.csv'
    chart = tmp_path / 'chart.png'

    save_history(df, history)
    assert history.exists()

    path = create_chart(df, chart)
    assert path.exists()


def test_format_message():
    df = pd.DataFrame({'token_symbol': ['AAA'], 'total_volume_usd': [1234]})
    msg = format_message(df, 24)
    assert 'AAA' in msg
    assert '1,234' in msg
