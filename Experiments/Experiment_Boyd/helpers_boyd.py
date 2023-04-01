import pandas as pd
import numpy as np

# Create list of column names to build suggestions
cols = np.arange(3, 22, step=2).tolist() # start inclusive, stop exclusive

# TODO: Exception handling
# This is for an output with 10 candidates suggested (default)
def get_suggestions_list(df):
    df_c = df.copy()
    
    # Combine columns with suggestions
    df_c['suggestions'] = df_c[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

    # Create list; String.split() returns list
    df_c['suggestions'] = df_c.suggestions.apply(lambda x: x.split(' '))
    
    # Drop unnecessary columns (2-22)
    df_c.drop(np.arange(2,23), axis=1, inplace=True)

    # Rename
    df_c.rename({0:"original",1:"corrected"}, axis='columns', inplace=True)

    return df_c