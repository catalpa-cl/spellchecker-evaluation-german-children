import pandas as pd

# Modified version of the function (compare litkey_2.py script)
# Adjusted for Language Tool purposes
def removeCharactersWords_x(df):
    # REMOVE CHARACTERS
    # Remove "|" and "_" characters, i. e. original is one/two-word whereas target is two/one-word
    # df['original']=df['original'].str.replace(r'[\|\_]', '', regex=True)
    # df['corrected']=df['corrected'].str.replace(r'[\|\_]', '', regex=True)

    # Remove intended line-break characters '^', '-^', '^-'
    # pattern = r'(\-\^)|(\^\-)|(\^)'
    # data_raw_token['original'] = data_raw_token['original'].str.replace(pattern, '', regex=True)

    # REMOVE WORDS
    # Remove words containing illegible character(s), i. e. containing '*' (original)
    # df = df[~df.original.str.contains(r'\*')]

    # Remove non-words ('?' target not identifiable or no standardized spelling | '~' target non existing word form)
    # df = df[~df.corrected.str.contains(r'\?|\~')]

    # Remove proper names ('Lea', 'Lars', 'Dodo') (corrected)
    df = df[~df.corrected.str.contains(r'Lea|Lars|Dodo|lea|lars|dodo')]

    # Remove common abbreviations/words that contain a dot (corrected), also sentence boundaries
    df = df[~df.corrected.str.contains(r'\.')]

    # Remove words less than 2 characters (corrected)
    df = df[df.corrected.str.contains(r'[A-Za-zÄÖÜäöüß]{2,}')]

    return df