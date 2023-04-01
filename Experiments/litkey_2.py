"""Helper functions for comparing spell checkers on the litkey dataset."""

import glob
import csv
from tqdm.notebook import tqdm
import pandas as pd
import seaborn as sns
import os

#from Experiments import helpers_litkey_2
import helpers_litkey_2

# types = litkey_2.load() 
# token = litkey_2.load(toss_duplicates=False) 

# Important: Change litkey_data_path 
def load(litkey_data_path = "./litkey-data/", lower_case=False, keep_correct_words=False, toss_duplicates=True):
    """Load and preprocess litkey dataset. Return pandas DataFrame"""
    
    data = helpers_litkey_2.combineCsvsToDataframe(litkey_data_path)
    
    # REMOVE NA-CASES, i. e. line-ends (^) (no other relevant NA-cases)
    #data.dropna(inplace=True)
    data.dropna(subset=['original','corrected'], inplace=True)
    
    # Conditional: lower-case
    # False per default
    if lower_case is True:
        data['original']=data['original'].str.lower()
        data['corrected']=data['corrected'].str.lower()
   
    data = helpers_litkey_2.removeCharactersWords(data)
    
    # False per default
    if keep_correct_words is False:
        data = helpers_litkey_2.removeCorrectWords(data)
        
    # Remove duplicates after storing token frequency
    # Tupel frequency is returned as a multi-indexed Series, therefore merging is different
    data['freq_ori'] = data.groupby('original').size()[data.original].values
    data['freq_cor'] = data.groupby('corrected').size()[data.corrected].values
    
    freq_tupel = data.groupby(['original','corrected']).size()
    data = data.merge(freq_tupel.to_frame(), how='left', left_on=['original', 'corrected'], right_on=['original', 'corrected'])
    data.rename({0: 'freq_tup'}, axis='columns', inplace = True)
     
    # True per default    
    if toss_duplicates is True:    
        data.drop_duplicates(subset=['original', 'corrected'],inplace=True)
    
  
    # Reset index
    data.reset_index(drop=True, inplace=True)
    
    return data


def load_raw(litkey_data_path = "./litkey-data/", remove_characters_words=False, keep_correct_words=True, toss_duplicates=False):
    """Load litkey dataset and do no preprocessing. Return pandas DataFrame"""

    data = helpers_litkey_2.combineCsvsToDataframe(litkey_data_path)

    # REMOVE NA-CASES, i. e. line-ends (^) (no other relevant NA-cases)
    data.dropna(subset=['original','corrected'], inplace=True)
    
    # REMOVE HEADLINE MARKERS, i. e. \h
    data = data[~data.original.str.contains(r'\\h')]
    
    # False per default
    if remove_characters_words is True:
        data = helpers_litkey_2.removeCharactersWords(data)
    
    # True per default
    if keep_correct_words is False:
        data = helpers_litkey_2.removeCorrectWords(data)
    
    # False per default    
    if toss_duplicates is True:    
        data.drop_duplicates(subset=['original', 'corrected'],inplace=True)
    
    # Reset index
    data.reset_index(drop=True, inplace=True)
    
    return data

    
def evaluate(data, lower_case=True):
    """Evaluate results. Create new columns in DataFrame (in_sugg, sugg_idx, idx0)."""
    # Making a copy is very important here, because the dataframe is modified directly
    # Without copying df, you cannot pass same df as argument more than one time
    # This is different to load function, where data is read in from path every function call
    data_c = data.copy()
    
    if lower_case is True:       
        data_c[['original', 'corrected']] = data_c[['original', 'corrected']].apply(lambda c: c.str.lower())
        # Do if list/string is not empty, else (if it is empty) empty string (adopted from hunspell analysis)
        data_c['suggestions'] = data_c['suggestions'].apply(lambda l: [x.lower() for x in l] if l else '')
        
        
    # Create columns
    # Is the corrected word in the suggestions? If yes, also save the index of the suggestion.    
    for rec in tqdm(range(len(data_c)), leave=False):
        
        #in_sugg = not data_c.suggestions.isna()[rec] and (data_c.corrected.iloc[rec] in data_c.suggestions.iloc[rec])
        in_sugg = data_c.corrected.iloc[rec] in data_c.suggestions.iloc[rec] # Returns True or False
        data_c.loc[rec, 'in_sugg'] = in_sugg # Append boolean to 'in_sugg' column
            
        
        if in_sugg:
            # In suggestions list, access index of corrected word
            # Append index to 'sugg_idx' column
            data_c.loc[rec, 'sugg_idx'] = data_c.suggestions.iloc[rec].index(data_c.corrected.iloc[rec])
            
            
    #TODO: Integrate
    # How often is it not in suggestions at all? dummy index -1
    # data['sugg_idx'].fillna(-1, inplace=True)

            
    data_c['idx0'] = data_c.sugg_idx == 0
        
    return data_c


# Difference to evaluate: suggestion-column contains String instead of List and only one suggestions
def evaluate_norma(data, lower_case=True):
    
    data_c = data.copy()
    
    if lower_case is True:       
        data_c[['original', 'corrected']] = data_c[['original', 'corrected']].apply(lambda c: c.str.lower())
        # Do if list/string is not empty, else (if it is empty) empty string (adopted from hunspell analysis)
        data_c['suggestions'] = [s.lower() if s else '' for s in data_c['suggestions']]
    
    for rec in tqdm(range(len(data_c)), leave=False):
        
        in_sugg = data_c.corrected.iloc[rec] == data_c.suggestions.iloc[rec] # Returns true or False
        data_c.loc[rec, 'in_sugg'] = in_sugg # Append boolean to 'in_sugg' column
        
        if in_sugg:
            data_c.loc[rec, 'sugg_idx'] = 0
            data_c.loc[rec, 'idx0'] = True
        else:
            data_c.loc[rec, 'sugg_idx'] = float('NaN') # Set to NaN, if target is not in suggestions                                                                 
            data_c.loc[rec, 'idx0'] = False
            
            
    return data_c
            