import collections
import os
import SimpleITK as sitk
import numpy as np
''' 作用： 将Mask1中非0的label值都置为1'''
work_path = "" # 原nii文件路径
result_path = ''# 重标注nii文件路径

if not os.path.exists(result_path):
        os.makedirs(result_path)

rowIndex1 = 1
i = 1
mask_paths = []

for root, dirs, files in os.walk(work_path):
    for file in files:
        if file.endswith("nii.gz"):
            mask_paths.append(os.path.join(root, file))

ori_name = os.path.join(work_path, 'image.nii.gz')

for path in mask_paths:

    mask1_path = path

    split_name = mask1_path.split("\\")[-1]
  

    num = split_name.split("-")[0]

    # 获取Mask1和Mask2中所有的label值
    mask1 = sitk.ReadImage(mask1_path)
    mask1Array = sitk.GetArrayFromImage(mask1)
    values1 = np.unique(mask1Array)

    featureVector = collections.OrderedDict()
    featureVector['image'] = os.path.dirname(ori_name) + '/image.nii.gz' # Save the whole path of image
    
    tmp = mask1Array.copy()
   
    # 将Mask1中非0的label值都置为1
    tmp[tmp != 0] = 1
   

    masktmp = sitk.GetImageFromArray(tmp)
    masktmp.CopyInformation(mask1)

    sitk.WriteImage(masktmp, os.path.join(result_path + '/'+"Mask" + str(num) + '.nii.gz'))
    mask1_new_path = os.path.join(result_path, 'mask_new.nii.gz')
    featureVector['mask'] = os.path.basename(mask1_new_path)


