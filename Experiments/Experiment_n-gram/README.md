# Reranking with n-gram model
This folder is about the reranking of the suggestion list results of various spell checkers. See topmost notebooks in "spelling_correction" directory. The analysis notebooks for the reranking contain the same statistics as the general analysis notebooks.

As in analysis notebooks, most of the visualizations in analysis reranking notebooks show stats for lower case/case insensitive. **Lower case/case insensitive is default for analysis notebooks, ergo reranking notebooks**.


## Structure
As in the other folders, the operation/experiment as a whole is basically a 3 step process. This is done for every spell checker or suggestion list separately
1. preprocessing
  - _prep_ tag
2. operation itself, i. e. reranking
  - _reranking script_
3. postprocessing
  - _postpr_ tag
    - for all candidates
    - for X candidates

After that, the data is processed to be put in the analysis notebook.

_Note_: The analysis notebooks for candidate variants (3, 5) are adjusted at some places to fit the adjustment. This is the case for plots
- suggestion by spell checker on testpoint
- suggestion index on levenshtein distance

## Starting point
...

## Pickles
- 'data_error_types_boyd_evaluation_cs_preprocessed_reranking.pkl'; Types are reproduced to be token, so contains token --> text information

## Important
- Use **case sensitive** for all rerankings
  - token data for frame with offset information
  - type data if suggestions were made for individual spelling errors (see Boyd)
<!--- explain --->
  --> This is the only way to build the text chunks (needed for reranking) + refer back to the original data.


- Limitation of candidates, i. e. reranking only _n_ first candidates, is implemented within postprocessing
  - The candidates suggested by the spell checker are cut in this step
