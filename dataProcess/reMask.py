'''
维度扩充，将mask的维度扩充成和dicom相同的维度
'''

import SimpleITK as sitk
import os

image_dir = "./datasets/Image/"
mask_dir = "./datasets/Mask/"
resize_mask_dir = "./datasets/resize_mask/"
img_dirs = []

for filepath, dirs, names in os.walk(image_dir):
    for name in names:
        img_dir = os.path.join(image_dir, name)
        img_dirs.append(img_dir)

for img_path in img_dirs:
    
    file_name = img_path.split("/")[-1].split(".nii.gz")[0]
    print(file_name)  # 文件名

    mask_name = "mask_" + file_name + ".nii.gz"
    mask_path = os.path.join(mask_dir,mask_name)
   
    image = sitk.ReadImage(img_path)
    mask = sitk.ReadImage(mask_path)

    rif = sitk.ResampleImageFilter()
    rif.SetReferenceImage(image)#需要重新采样的目标图像
    rif.SetOutputPixelType(mask.GetPixelID())
    rif.SetInterpolator(sitk.sitkNearestNeighbor)
    resMask = rif.Execute(mask)

    # 保存
    sitk.WriteImage(resMask, os.path.join(resize_mask_dir + '/' + file_name + '_RM.nii.gz'), True)


