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

    def __init__(self):
        
        self.holidays_dict = {datetime.date(2020, 1, 14): 'Makar Sankranti / Pongal',
                              datetime.date(2020, 1, 26): 'Republic Day',
                              datetime.date(2020, 8, 15): 'Independence Day',
                              datetime.date(2020, 10, 2): 'Gandhi Jayanti',
                              datetime.date(2020, 12, 25): 'Christmas',
                             }

    def mediaRatio(self, df) -> int:
        return ((df[df['Message'] == ' <Media omitted> '].Message.count()) / (df.Message.count()))*100

    def totalEmojis(self, df) -> int:
        return len([i for j in df.Emojis[df.Emojis!=0] for i in j])

    def uniqueEmojis(self, df) -> int:
        return len(set([i for j in df.Emojis[df.Emojis!=0] for i in j]))

    def frequentEmojis(self, df) -> object:
        emojiList = [i for j in df.Emojis[df.Emojis!=0] for i in j]
        emoji_dict = dict(Counter(emojiList))
        emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
        emoji_df = pd.DataFrame(emoji_dict, columns=['Emoji', 'Count'])
        if emoji_df.shape[0] <10:
            return emoji_df
        else:
            return emoji_df[:10]

    def activeMembers(self, df) -> object:
        authors = pd.DataFrame(df.Author.value_counts())
        authors = authors.rename(columns={'Author': 'Message Count'})
        authors.index.name = 'Author'
        if authors.shape[0] < 8:
            return authors
        else:
            return authors[:8]

    def lazyMembers(self, df) -> object:
        authors = pd.DataFrame(df.Author.value_counts())
        authors = authors.rename(columns={'Author': 'Message Count'})
        authors.index.name = 'Author'
        if authors.shape[0] < 5:
            return authors[::-1]
        else:
            return authors[-5:][::-1]

    def activityOverDates(self, df) -> object:
        result = df.groupby('Date').sum()
        result = result.rename(columns={'Emoji_num': 'Number of Messages'})
        return result

    def activityOverTime(self, df) -> object:
        result = df.groupby('Time').sum()
        result = result.rename(columns={'Emoji_num': 'Number of Messages'})
        return result

    def holidaysDataFrame(self, df) -> dict:
        df_dict = {}
        for date, event in self.holidays_dict.items():
            temp = df[(df.Date.dt.day==date.day) & (df.Date.dt.month==date.month)]
            df_dict[event] = temp

        return df_dict

    def nightOwls_earlyBirds(self, df) -> dict: