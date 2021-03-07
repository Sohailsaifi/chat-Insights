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
        test = re.match(date_time, line)
        if test is not None:
            return True
        else:
            return False

    def seperateData(self, line: str) -> tuple:
        entry_data = line.split(' - ')
        date, time = entry_data[0].split(', ')
        authMsg = entry_data[1].split(':')
        if len(authMsg) > 1:
            author = authMsg[0]
            message = ' '.join(authMsg[1:])
            return (date, time, author, message)
        else:
            return None

    def process(self):
        f = self.load_file()
        f.readline()
        full_message = []
        date = ''
        time = ''
        author = ''
        while True:
            line = f.readline()
            if not line:
                break
            
            if self.is_newEntry(line):
                
                if len(full_message)>0:
                    temp = ' '.join(full_message)
                    modified_replaced = temp.replace('\n', ' ')
                    self.data.append([date, time, author, modified_replaced])
                
                full_message.clear()
                received = self.seperateData(line)
                if received is not None:
                    date, time, author, message = received
                    full_message.append(message)
                else:
                    full_message.append(line)

        f.close()

    def emojis(self, msg: str) -> list:
        final_list = []
        for char in msg:
            if char in emoji.UNICODE_EMOJI:
                final_list.append(char)
                
        if len(final_list)==0:
            return 0
        else:
            return final_list

    def dataframe(self) -> object:
        df = pd.DataFrame(self.data, columns=['Date', 'Time', 'Author', 'Message'])
        df['Date'] = pd.to_datetime(df.Date)
        df['Emojis'] = df.Message.apply(self.emojis)
        df['Emoji_num'] = df.Emojis.str.len()
        return df



class GenerateStats: