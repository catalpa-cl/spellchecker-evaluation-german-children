import pandas as pd

# Reload pickle
# Load df from pickle
#data_error_token = pd.read_pickle('data_error_token_hunspell_evaluation.pkl')
#data_error_types = pd.read_pickle('data_error_types_hunspell_evaluation.pkl')

# Get means as aid for interpreting percent stacked bar plot over testpoints
# Testpoints 1-5 and 6-10
def print_AM_half_tp(shares_list):
    for e in shares_list:
        print(round(sum(e[0:5])/5,2))
        print(round(sum(e[5:10])/5,2))
        print('*'*20)
        
  
