
import argparse
import cv2
import numpy as np
import pandas as pd
import os

from shapely.affinity import affine_transform
from shapely.geometry import Polygon  
import skimage.exposure
import re

"""
This file is to create the polygon for each image
You have to file the image_ID list in line 16 as [['image_name',image_id],['image_name',image_id],[...,...]]  
"""
#
# image_ID=[['4301099.png',6375],['4305247.png',5838],['4305255.png',6712],['4305261.png',6151]]

# path_to_images='/Users/osama-mac/Desktop/master/sim/Images' 
# path_to_data_csv='/Users/osama-mac/Desktop/master/sim/data.csv' 
# path_to_save_created_masks='/Users/osama-mac/Desktop/master/sim/output'
#


#--------------------------------- from this line and below no need to do anything here----------------------------
def get_mask_from_poly(
    image_ID, # [['image',id],['image',id],['image',id],.........]
    path_to_images, # images path
    path_to_data_csv, # path to converted csv file 
    path_to_save_created_masks, # output directory
):

    for im_id in image_ID:

        image_name=im_id[0]  # image name 
        Id=im_id[1] # id 
        
        #--------------------------------
        image = cv2.imread(os.path.join(path_to_images,image_name)) # the path to the images
        h, w, c = image.shape
        mask = np.zeros((h,w,3))
        combine_images = np.zeros((h,w, 3))
        
        
        window_name = 'Image'
        df=pd.read_csv(path_to_data_csv)
        df['WKT']=[re.findall(r'[-+]?\d*\.?\d+|\d+', i) for i in df['WKT']]
        # Polygon points coordinates
        i=0
        refine=[]
        for m in df['WKT']:
            y=[]
            for i in range(0,len(m)-1,2):
                y.append([float(m[i]),float(m[i+1])])
            refine.append(y)

        value=(df[df['Image']==Id].index.values)

        #
        for i in range(value[0],value[-1]+1,1):

            polygon = Polygon(refine[i])
            

            point2=affine_transform(polygon, [1, 0, 0, -1, 0, h])
            
            x, y = point2.exterior.coords.xy

            # print(pts)
            int_coords = lambda x: np.array(x).round().astype(np.int32)
            exterior = [int_coords(point2.exterior.coords)]


            isClosed = True

            # Blue color in BGR
            color = (255, 0, 0)

            # Line thickness of 2 px
            thickness = 2

            # Using cv2.polylines() method
            # Draw a Blue polygon with 
            # thickness of 1 px
            image_ = cv2.polylines(image, exterior, 
                                isClosed, color, thickness)

            filled = np.zeros_like(image)
            filled = cv2.fillPoly(filled, exterior, color =(255,255,255))
            result = skimage.exposure.rescale_intensity(filled, in_range=(127.5,255), out_range=(0,255)).astype(np.uint8)
            sav=os.path.join(path_to_save_created_masks,image_name) # to produce the mask
            #
            #
            mask = np.maximum(mask, result)
            combine_images=mask 

        cv2.imwrite(sav,combine_images)
#------------------------------ End of Script ------------------------------------------------------
def get_arg():
    parser = argparse.ArgumentParser(description='Create masks from polygon created by Cytomine')
    parser.add_argument('--image_id', type=list, help='images and id as list [[image,id],[image,id],...]')
    parser.add_argument('--images', type=str, help='images path')
    parser.add_argument('--csv_data', type=str, help='path to converted csv file ')
    parser.add_argument('--output', type=str, help='output directory')
    return parser.parse_args()

if __name__ == '__main__':
    args=get_arg()
    get_mask_from_poly(
        args.image_id,
        args.images,
        args.csv_data,
        args.output
    )
    print('Sucessfully created masks!')





