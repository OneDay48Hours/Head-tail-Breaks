'''
@Description: 
@Date: 2024-02-27 10:38:07
@LastEditTime: 2024-02-27 12:56:14
@LastEditors: Haofeng Tan
'''
import numpy as np
from osgeo import gdal
import argparse

#get required arguments
def parse_arg():
    parser =  argparse.ArgumentParser()
    parser.add_argument("-p", "--image_path", type=str)
    args = parser.parse_args()
    return args

def htb(data):
    """
    @param data: array of data to apply ht-breaks
    @return results: break points
    """
    assert data.all()
    # assert all(isinstance(digit, int) or isinstance(digit, float) for digit in np.nditer(data))

    #array of break points
    results = []

    #comupute ht breaks recursively
    def htb_inner(data):
        
        data_length = float(len(data))
        data_mean = np.mean(data)
        results.append(data_mean)
        
        #get head parts
        head = data[data > data_mean]
        while len(head) > 1 and len(head) / data_length < 0.40:
            return htb_inner(head)
    
    htb_inner(data)
    
    return results

def get_image_pts(image_path):
    dataset = gdal.Open(image_path)

    if dataset is not None:
        image_array = dataset.ReadAsArray()  
        image_array_nodata = image_array[image_array > 0]

        pts = htb(image_array_nodata.flatten()) 
        print(pts)


if __name__ == "__main__":
    
    args = parse_arg()
    get_image_pts(args.image_path)
