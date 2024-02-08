# -*- encoding: utf-8 -*-
'''
@Description:   1. Compute mu = mean(var).
                2. Break var into the tail (as var < mu) and the head (as var > mu).
                3. Assess if the proportion of head over var is lower or equal than a given threshold (i.e. length(head)/length(var) <= thr)
                4. If 3 is TRUE, repeat 1 to 3 until the condition is FALSE or no more partitions are possible (i.e. head has less than two elements expressed as length(head) < 2).
@Author: Haofeng Tan
@Date: 2024-02-02 10:44:03
'''

import pandas as pd
import numpy as np

#get required arguments
def parse_arg():
    parser =  argparse.ArgumentParser()
    parser.add_argument("-f", "--file_path", type=str)
    parser.add_argument("-c", "--column_index", type=int)
    parser.add_argument("-v", "--headtail_version", type=int)
    args = parser.parse_args()
    return args

#compute head tail break points version1
def htb1(data):
    '''
    @param data: array of data to apply head/tail breaks
    @return results: break points
    @return detail_df: dataframe of head/tail breaks
    '''
    
    #comupute ht breaks recursively
    def htb_inner(data, result, df):

        #get head parts
        data_mean = np.mean(data)
        head = data[data > data_mean]

        data_len = len(data)
        head_len = len(head)
        tail_len = data_len - head_len
        head_percent = head_len/float(data_len)
        tail_percent = tail_len/float(data_len)

        while head_len >= 1 and head_percent < 0.40:
            row_data = {'rows': data_len, 'mean': data_mean, 'head': head_len, 'tail': tail_len, 'head percentage': head_percent, 'tail percentage': tail_percent}
            df.loc[len(df)] = row_data
            result.append(data_mean)
            return htb_inner(head, result, df)
    
    assert data.all()

    #array of break points
    results = []
    #dataframe of break details
    detail_df = pd.DataFrame(columns=['rows', 'mean', 'head', 'tail', 'head percentage', 'tail percentage'])

    htb_inner(data, results, detail_df)
    
    return results, detail_df
    

#compute head tail break points version2
def htb2(data):
    '''
    @param data: array of data to apply ht-breaks
    @return results: break points
    @return detail_df: dataframe of head/tail breaks
    '''

    #comupute ht breaks recursively
    def htb_inner(data, result, weight, df):

        #get head parts
        data_mean = np.mean(data)
        head = data[data > data_mean]

        data_len = len(data)
        head_len = len(head)
        tail_len = data_len - head_len
        head_percent = head_len/float(data_len)
        tail_percent = tail_len/float(data_len)

        #weight head percentage
        weight.append(head_percent)
        avg_head_percent = sum(weight) / len(weight)

        while len(head) >= 1 and avg_head_percent < 0.40:
            row_data = {'rows': data_len, 'mean': data_mean, 'head': head_len, 'tail': tail_len, 'head percentage': head_percent, 'tail percentage': tail_percent, 'avg head percentage': avg_head_percent}
            df.loc[len(df)] = row_data
            result.append(data_mean)
            return htb_inner(head, result, weight, df)
    
    assert data.all()

    #array of break points
    results = []
    #head weights
    weights = []  
    #dataframe of break details
    detail_df = pd.DataFrame(columns=['rows', 'mean', 'head', 'tail', 'head percentage', 'tail percentage', 'avg head percentage'])

    htb_inner(data, results, weights, detail_df)
    
    return results, detail_df


def main(excel_file_path:str, index:int, version:int):
    """
    @param excel_file_path
    @param index: column index to be analyzed
    @param version: head/tail break version
    """
    #get excel column and exclude first row
    df = pd.read_excel(excel_file_path)
    analyze_column = df.iloc[1:, index].to_numpy()
    if version == 1:
        break_pts, detail_table = htb1(analyze_column)
    elif version ==2:
        break_pts, detail_table = htb2(analyze_column)

    print('============================================================')
    print('Head/tail version{} Break Detail:'.format(version))
    print(detail_table)
    print('============================================================')
    print('Break Points:')
    print(break_pts)


if __name__ == "__main__":
    
    # file_path = '/Users/***/****/test.xlsx'
    # main(file_path, 0, 2)
  
    args = parse_arg()
    main(args.file_path, args.column_index, args.headtail_version)
  
