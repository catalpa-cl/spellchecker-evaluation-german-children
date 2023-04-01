import subprocess
from datetime import datetime

import sys
#sys.path.insert(0, '/Users/lisaprepens/_Programmierung/bodu-spell/spelling_correction')
#from Experiments import litkey_2

# TODO: default value, if parameter is not set whilst calling method
def run_brill(dict_file, train_data, test_data, window=3, minatoa=0.8):

    # Determine parameters for calling Brill via the console
    #brill_command = ['java', '-jar', r'../../BrillMooreSpellChecker-master/target/brillmoore-0.1-jar-with-dependencies.jar',
    brill_command = ['java', '-jar', './BrillMooreSpellChecker-master/target/brillmoore-0.1-jar-with-dependencies.jar',
                     '--dict', dict_file,
                     '--train', train_data,

                     '--test', test_data,
                     '--window', str(window), # window for expanding alignments (Brill and Moore's N; default 3)
                     '--minatoa', str(minatoa) # minimum a -> a probability (default 0.8)
                     ]
    # other possible command: --candidates, --lowercase, --single, --capitalized

    # TODO: Write chosen documents in file
    # Create a file to write console output for each run
    cur_time = datetime.now().strftime("%d-%m-%Y_%H.%M")
    brill_output = open(r'./Output/' + cur_time + '.txt', mode='w+', encoding='utf-8')
    # brill_output = open(r'output_spell_checker_boyd/TESTEST.txt', mode='w+')

    # Write parameters for the run
    print(brill_command[3:], file=brill_output)

    # Run command/Brill
    process = subprocess.run(brill_command, stdout=brill_output)
    brill_output.close()

# Define parameters
# Dictionary
#dict_brill = r'../../BrillMooreSpellChecker-master/data/aspell-wordlist-en_USGBsGBz.70-1.txt'
#dict_childlex = r'../../Lexicons/childlex_0.17.01_all_types.txt'
# oder german-utf8.dic

#dict_childlex_server = r'./Lexicons/childlex_0.17.01_all_types.txt'
#dict_childl_keywords_server = r'./Lexicons/childlex_0.17.01_all_types_keywords_Weg_Fundbuero.txt'
dict_hunspell = r'./Lexicons/hunspell_dict_de.txt'

# Training data
#train_brill = r'../../BrillMooreSpellChecker-master/data/aspell-common.train'
#train_count = r'../../Trainingdata/h1obi_train_misspellings.csv' # count
#train_count_700 = r'../../Trainingdata/h1obi_train_misspellings_700.tsv'

#train_count_700_server = r'./Trainingdata/h1obi_train_misspellings_700.tsv'
#train_count_server = r'./Trainingdata/h1obi_train_misspellings.csv'
train_count = r'./Trainingdata/h1obi_train_misspellings.csv'

# Test data
#test_brill = '../../BrillMooreSpellChecker-master/data/aspell-common.dev.first10'
#small_test_count = r'./Input/smaller_data_sets/2021-04-14_litkey_2_error_types_cs_count_100.tsv'
#small_test = r'./Input/smaller_data_sets/litkey_2_error_types_cs_NO_COUNT_100_2021-04-14.tsv'

#small_test_count_server = r'./Input_Server/smaller_data_sets/2021-04-14_litkey_2_error_types_cs_count_100.tsv'

test_count_server = r'./Input_Server/2021-04-14_litkey_2_error_types_cs_count.tsv'
#test_count = r'./Input/2021-04-14_litkey_2_error_types_cs_count.tsv'

# Function call
#run_brill(dict_brill, train_brill, test_brill)
#run_brill(dict_brill, train_brill, small_test_count)
#run_brill(dict_childlex, train_count_700, small_test_count)

#run_brill(dict_childlex_server, train_count_700_server, small_test_count_server)
#run_brill(dict_childl_keywords_server, train_count_server, test_count_server)
run_brill(dict_hunspell, train_count, test_count_server)