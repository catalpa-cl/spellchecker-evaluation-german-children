import kenlm
import pandas as pd
import csv

# Import csv with chunks generated in "reranking_prep"
# Change pathname only here (no '(...).csv' ending) !

#path = 'chunk_generation_2022-01-12_boyd'
#path= 'chunk_generation_2022-01-26_boyd'
#path = 'chunk_generation_2022-02-16_hunspell'
#path = 'chunk_generation_2022-02-16_lt_error_list'
#path = 'chunk_generation_2022-06-07_nuspell'
path = 'chunk_generation_2022-11-11_dkpro_childlex_3c_ngram3'

path_in = r'./Input_chunk/'+path+'.csv'
#path_in= r'./Input_chunk/chunk_generation_2022-01-04_boyd.csv'

df = pd.read_csv(path_in, sep='|')

# Set model
model = kenlm.LanguageModel('cmusphinx-voxforge-de.lm')
print('{0}-gram model'.format(model.order))

# Important: Lowercase input (capital-words are OOV) and set bos and eos parameters to false
df['prob'] = [model.score(chunk.lower(), bos=False, eos=False) for chunk in df.chunk]

#print(df.head(10))
#print(df.tail(10))

# Export

path_out = r'./Output_chunk/'+path+'_results.csv'
#path_out = r'./Output_chunk/chunk_generation_2022-01-12_results.csv'

df.to_csv(path_out, sep='|', quoting=csv.QUOTE_NONE, escapechar="\\", index=False)
#df.to_csv(r'./Output_chunk/chunk_generation_2022-01-12_results.csv', sep='|', quoting=csv.QUOTE_NONE, escapechar="\\", index=False)