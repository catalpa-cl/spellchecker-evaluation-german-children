# Script to be run on server; WHOLE TEXTS as input
import language_tool_python
import glob
import os
import pickle
import pandas as pd

# Initialize LanguageTool object locally, i. e. default

tool = language_tool_python.LanguageTool('de-DE')
# Disable UPPERCASE_SENTENCE_START rule
tool.disabled_rules = set(["UPPERCASE_SENTENCE_START", "COMMA_PARENTHESIS_WHITESPACE"])

matches = []

for csv_file in sorted(glob.glob(r'./Input_texts_csv/'+'*.csv')):
    with open(csv_file, 'r', encoding='utf-8') as f:
        # not readlines
        # read file as a whole, i. e. all texts
        text = f.read()
        text_prep = text.replace('\n', ' ')
        #text_prep = text_n.replace(' .', '.')

        matches.append(tool.check(text_prep))


#print(matches)

# Replace new lines regex
#texts_n = texts.replace('\n', ' ')

#texts_prep = texts_n.replace(' .', '.')

# Check
#matches = tool.check(texts_prep)

# Write pickle to file
# Parameter wb (write binary) creates file, if it does not exist yet
with open('matches_texts.pkl', 'wb') as f:
    # Pickle list
    pickle.dump(matches, f, protocol=3)