import pydicom
import os
import nibabel
'''计算每个病人的肺栓塞体积,并保存在txt文件中
数据：|--dcm文件夹
        |--病人数据1
            |--dicom文件
            |--mask.nii.gz
        |--病人数据2
        |--病人数据3
'''

# Calculate the number of voxels
def get_pixels_No(bmp_data_dir):
    pixels_No = 0
    nib_img = nibabel.load(bmp_data_dir)
    img = nib_img.get_fdata()
    img_array_int = img.astype(int)//img.astype(int)
    pixels_No = pixels_No + img_array_int.sum()
    return pixels_No


# Calculate the volume per voxel
def get_pixel_info(dcm_data_dir):

    pixel_infos = []
    dcm_files = os.listdir(dcm_data_dir)

    dcm_file_1 = os.path.join(dcm_data_dir, dcm_files[1])
    dcm_tag_1 = pydicom.read_file(dcm_file_1)
   

    spacex, spacey = dcm_tag_1.PixelSpacing    # 获取像素间距.
   
    # 获取层间距
    # 有些 dcm图像并不是按照InstanceNumber进行排序的，不能直接用最后一张的slicelocation减去第一张，再除以张数
    SliceLocations = []
    ImagePositon_z = []
    for dcm in dcm_files:
        dcm_file = os.path.join(dcm_data_dir, dcm)
        if(dcm_file.endswith(".IMA")):
            dcm_tag = pydicom.read_file(dcm_file)
            SliceLocations.append(dcm_tag.SliceLocation)   #获取层间距
            ImagePositon_z.append(dcm_tag.ImagePositionPatient[2])
    SliceLocations_max = max(SliceLocations)
    SliceLocations_min = min(SliceLocations)
    ImagePositon_z_max = max(ImagePositon_z)
    ImagePositon_z_min = min(ImagePositon_z)
  
    if SliceLocations_max - SliceLocations_min < 1e-10:
        spacez = abs(ImagePositon_z_max - ImagePositon_z_min) / (len(dcm_files) - 1)
    else:
        spacez = abs(SliceLocations_max - SliceLocations_min) / (len(dcm_files) - 1)
    pixel_infos = [spacex, spacey, spacez]
    return pixel_infos


def get_volume(dcm_data_dir, bmp_data_dir):
    pixel_infos = get_pixel_info(dcm_data_dir)
    pixels_No = get_pixels_No(bmp_data_dir)
    volume = pixel_infos[0] * pixel_infos[1] * pixel_infos[2] * pixels_No / 1000
    return volume


def get_dcm_fime_path(work_path):
    dcm_path = []
    for root, dirs, files in os.walk(work_path):
        for file in files:
            if file.endswith(".IMA"):
                dcm_path.append(root)
                break

    return dcm_path


dcm_path = "./datasets/volume/dicom/" # 所有dicom文件总目录
mask_volume_path = "./datasets/volume/"# 存放计算体积结果txt的目录

mask_volume = open(mask_volume_path + "mask_volume.txt","w+")
mask_volume.truncate()
dcm_list = get_dcm_fime_path(dcm_path)

mask_volume.write("   肺栓塞的体积，单位（cm3）   ")
mask_volume.write("\n")

for dcm_path in dcm_list:
    for root, dirs, files in os.walk(dcm_path):
        for file in files:
            if file.endswith(".nii.gz"):
                mask_path = os.path.join(root, file)
                mask_name = mask_path.split("\\")[-1].split("-")[0]
                volume = round(get_volume(dcm_path,mask_path),3)
                print(mask_name)
                print( mask_name + " volume is %.3f" % volume)
                mask_volume.write("Mask " + mask_name + " volume is " + str(volume))
                mask_volume.write("\n")
mask_volume.close()
