# Short Form
_The statistic is on tupel-base, i. e. one tupel consists of (original, corrected)-pair._
- data_raw_token: Contains all token that are contained in litkey data set
- data_clean_token: Contains all token, correct and incorrect tupel, that we are interested in for analysis
- data_error_token : Contains only the erroneous tupel out of "data_clean_token"

**Vice versa with type base.**

# More Detailed Description

### ( I. ) Data_raw_token (unprocessed data set)
For the analysis in this notebook, a version of the data set without preprocessing is needed. In this case, only NA-cases (line ends(^)) and headline markers (\h) are removed (as these have been added for annotation purposes). No other preprocessing did take place.

The head this version of the dataframe is shown below.


### ( II. ) Data_clean_token (preprocessed data set)
Now, the data set from above ( I. ) is preprocessed/cleaned. This includes ...
- ... that characters from normalization are removed, namely
    - "|" and "_", i. e. original is one/two-word whereas target is two/one-word
    - intended line-break characters '^', '-^', '^-'

- ... the exlucsion of some words from further analysis, namely
    - words containing illegible character(s), i. e. containing '*' (original)
    - non-words ('?' target not identifiable or no standardized spelling | '~' target non existing word form)
    - proper names ('Lea', 'Lars', 'Dodo') (corrected)
    - common abbreviations/words that contain a dot (corrected), also sentence boundaries
    - words less than 2 characters (corrected)

These measures result in corresponding head of data frame shown below (for comparison see ( I. )).

### ( III. ) Data_error_types (errors from preprocessed data set)
In addition to preprocessing steps in ( II. ), all correct words are not considered anymore. Only missspellings from litkey data set after preprocessing are kept.

Description of column names:
- *freq_ori*: how often does original appear in overall data set <br>
- *freq_cor*: how often does corrected appear in overall data set <br>
- *freq_tup*: how often does this tupel of (original, corrected) appear in overall data set

These measures result in corresponding head of data frame shown below (for comparison see ( II. ) and ( I. )).
