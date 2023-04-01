"""Helper functions for loading/perform action on the litkey dataset."""
import glob
import csv
from tqdm.notebook import tqdm
import pandas as pd
import os

# Combine all csv-files from directory into DataFrame
def combineCsvsToDataframe(data_path):
    df=[] # type: list
    for csv_file in sorted(glob.glob(data_path+"*.csv")):
        frame = pd.read_csv(filepath_or_buffer=csv_file, sep='\t', quoting=csv.QUOTE_NONE, names=['original', 'corrected']) # Get columns (o & c)
        frame['filename'] = os.path.basename(csv_file) # Get column filename
        df.append(frame)
    #display(type(frame)) : DataFrame
    #display(type(df)) : List
    df = pd.concat(df)
    return df


# Remove certain characters and words that are excluded/ignored for analysis
def removeCharactersWords(df): 
    # REMOVE CHARACTERS

    # Remove "|" and "_" characters, i. e. original is one/two-word whereas target is two/one-word
    df['original']=df['original'].str.replace(r'[\|\_]', '', regex=True)
    df['corrected']=df['corrected'].str.replace(r'[\|\_]', '', regex=True)

    # Remove intended line-break characters '^', '-^', '^-'
    pattern = r'(\-\^)|(\^\-)|(\^)'
    df['original'] = df['original'].str.replace(pattern, '', regex=True)


    # REMOVE WORDS

    # Remove words containing illegible character(s), i. e. containing '*' (original)
    df = df[~df.original.str.contains(r'\*')]

    # Remove non-words ('?' target not identifiable or no standardized spelling | '~' target non existing word form)
    df = df[~df.corrected.str.contains(r'\?|\~')]

    # Remove proper names ('Lea', 'Lars', 'Dodo') (corrected)
    df = df[~df.corrected.str.contains(r'Lea|Lars|Dodo|lea|lars|dodo')]

    # Remove common abbreviations/words that contain a dot (corrected), also sentence boundaries
    df = df[~df.corrected.str.contains(r'\.')]

    # Remove words less than 2 characters (corrected)
    df = df[df.corrected.str.contains(r'[A-Za-zÄÖÜäöüß]{2,}')]   
    
    return df


# Remove all correct words (ignoring case)
def removeCorrectWords(df):
    df_lc = df.copy()
    df_lc['original'] = df_lc['original'].str.lower() # lower-case original
    df_lc['corrected'] = df_lc['corrected'].str.lower() # lower-case corrected
    
    df = df[df_lc.original != df_lc.corrected]
    
    return df

