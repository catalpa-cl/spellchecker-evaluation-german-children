import pandas as pd
import csv
from datetime import date

# Reference df & speller_df text information needed
def create_chunk_file(suggl_by, reference_df, speller_df):
    # Get date
    today = str(date.today())
    # Prep field names for output file
    field_names = ['chunk', 'candidate', 'err_idx', 'num_chunk_build']

    # Create iterator for loop
    num_text_list = list(reference_df.num_texts.unique())

    with open("./Input_chunk/chunk_generation_" + today + '_'+ suggl_by + ".csv", mode='w') as file:
        file_writer = csv.writer(file, delimiter="|", quoting=csv.QUOTE_NONE, escapechar="\\")
        file_writer.writerow(field_names)

        num_chunk_build = 0

        for i in num_text_list:  # 0-1921

            cut_ref = reference_df.loc[reference_df.num_texts == i]
            cut_err = speller_df.loc[speller_df.num_texts == i]

            # Get max value, i. e. boundary
            max_ = max(cut_ref.idx_per_text)

            # print("text count in outer loop: ",i)

            # Operation per token; Slice of error dataframe
            for err_idx, data in cut_err.iterrows():

                # Get suggestion list
                temp_s = data.suggestions
                #print(temp_s)
                #print(len(temp_s))

                # print("text count in inner loop, vorne: ",i)

                err_idx_per_text = reference_df.iloc[err_idx].idx_per_text

                # Iterate over suggestion list
                if len(temp_s) != 0:  # suggestion list

                    for c in temp_s:
                        # print("Candidate ", c)
                        # print("Error_idx ", err_idx)

                        # Define range
                        if err_idx_per_text >= 2 and err_idx_per_text <= (max_ - 2):
                            temp = reference_df.iloc[err_idx - 2].original + ' ' + reference_df.iloc[
                                err_idx - 1].original + ' %s ' + reference_df.iloc[err_idx + 1].original + ' ' + \
                                   reference_df.iloc[err_idx + 2].original

                        # start
                        elif err_idx_per_text == 0:
                            temp = ' %s ' + reference_df.iloc[err_idx + 1].original + ' ' + reference_df.iloc[
                                err_idx + 2].original
                        elif err_idx_per_text == 1:
                            temp = reference_df.iloc[err_idx - 1].original + ' %s ' + reference_df.iloc[
                                err_idx + 1].original + ' ' + reference_df.iloc[err_idx + 2].original

                        # end
                        elif err_idx_per_text == (max_ - 1):
                            temp = reference_df.iloc[err_idx - 2].original + ' ' + reference_df.iloc[
                                err_idx - 1].original + ' %s ' + reference_df.iloc[err_idx + 1].original
                        elif err_idx_per_text == max_:
                            temp = reference_df.iloc[err_idx - 2].original + ' ' + reference_df.iloc[
                                err_idx - 1].original + ' %s '

                        temp_res = temp % (c), c, err_idx, num_chunk_build

                        file_writer.writerow(temp_res)
                        # print(num_itr_sugg)
                        # print(temp_res)

                num_chunk_build += 1

                # elif len(temp_s) == 0: # suggestion list
                #    print('Liste ist leer')
                # else:
                #   print('ERROR')

            # print("text count in inner loop, hinten: ",i)

def rerank_suggs_by_prob(prob_df, set_candidates=None):
    # Prep
    num_chunk_build_id = list(prob_df.num_chunk_build.unique())
    # df['new_suggestions'] = ''
    err_idx_l = []
    num_chunk_build_l = []
    new_suggestions_l = []

    # Iterate over number of chunks
    for x in num_chunk_build_id:
        # Get respective segment of dataframe, i. e. one iteration through sugg list
        temp = prob_df.loc[prob_df.num_chunk_build == x]

        # print(temp)
        # If any parameter has been passed to argument
        # TODO: Allow for certain values only
        # TODO: Check whether value is not higher than available candidates
        if set_candidates != None:
            #len(temp)
            temp = temp[:set_candidates]

        # Sort dataframe segment by probability , descending
        new_order_df = temp.sort_values(by='prob', ascending=False)

        # Build list of candidates, descending order according to probability
        new_suggs = []
        for i, e in new_order_df.iterrows():
            new_suggs.append(str(e.candidate))
            # print(e.candidate)
        # print(new_suggs)

        # Save new suggestion list to original data frame
        # print(temp.err_idx.unique(), temp.num_chunk_build.unique(), new_suggs)
        err_idx_l.append(int(temp.err_idx.unique()))
        num_chunk_build_l.append(int(temp.num_chunk_build.unique()))
        new_suggestions_l.append(new_suggs)
        # num_chunk_build_l.append()
        # [new_suggs for j in df.loc[df.num_chunk_build == x].new_suggestions]

        # new_df = pd.DataFrame(new_data, columns=list(df))
        # return new_df

        new_data = list(zip(err_idx_l, num_chunk_build_l, new_suggestions_l))

        new_df = pd.DataFrame(data=new_data, columns=['err_idx', 'num_chunk_build', 'new_suggestions'])

    return new_df