import re
import pandas as pd
import emoji
from collections import Counter
import datetime

class ExtractDataFrame:
    def __init__(self, file_path):
        self.path = file_path
        self.data = []