import imp
import pandas as pd
import os
import argparse
"""
in this file you just need to give the :

1. path to cytomine file  in line 13
2. path to save the output file in line 14

"""
def convert_Cytomine_data(
    path_to_file_from_cytomine,  # put the path directory for the cytomine file 
    path_to_save_converted_file   # put the path directory to save the converted file the  
):

    data=pd.read_csv(path_to_file_from_cytomine,sep=';')   
    data=data.drop(columns=['WKT '])
    data=data.rename(columns={'Perimeter':'WKT'})

    data.to_csv(os.path.join(path_to_save_converted_file,'data.csv'),index=False)


def get_arg():
    parser = argparse.ArgumentParser(description='Convert Cytomine data file to csv')
    parser.add_argument('--cytomine_file', type=str, help='cytomine_file path csv')
    parser.add_argument('--output_path', type=str, help='output save path')
    return parser.parse_args()

if __name__ == '__main__':
    args=get_arg()
    convert_Cytomine_data(args.cytomine_file,args.output_path)
    print('Sucessfully converted!')
