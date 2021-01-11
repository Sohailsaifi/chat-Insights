import re
import pandas as pd
import emoji
from collections import Counter
import datetime

class ExtractDataFrame:
    def __init__(self, file_path):
        self.path = file_path
        self.data = []

    def load_file(self):
        file = open(self.path, 'r', encoding='utf-8')
        return file

    def is_newEntry(self, line: str) -> bool:
        date_time = '([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'