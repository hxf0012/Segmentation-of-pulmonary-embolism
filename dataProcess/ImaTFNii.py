import SimpleITK as sitk
import numpy as np
import pydicom
import os

'''
将IMA后缀的文件，转成nii
功能：读取filepath下的dcm文件
返回值：读取得到的SimpleITK.SimpleITK.Image类   
其他说明：  file = sitk.ReadImage(filepath)
            获取基本信息，大小，像素间距，坐标原点，方向
            file.GetSize()
            file.GetOrigin()
            file.GetSpacing()
            file.GetDirection()
'''

# 生成的mask保存位置
result_path = ".\\results"


def get_dcm_fime_path(work_path):
    dcm_path = []
    for root, dirs, files in os.walk(work_path):
        for file in files: 
            if file.endswith(".IMA"):# 读取的文件类型
                dcm_path.append(root)
                break
    return dcm_path

def readdcm(filepath):
 
    series_id = sitk.ImageSeriesReader.GetGDCMSeriesIDs(filepath)
    series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(filepath, series_id[0])
    series_reader = sitk.ImageSeriesReader()  # 读取数据端口
    series_reader.SetFileNames(series_file_names)  # 读取名称
    images = series_reader.Execute()  # 读取数据
    return images

def save(path,dcm_images):

    split_name = path.split("\\")[-2]
    print(split_name)

    sitk.WriteImage(dcm_images, os.path.join(result_path + '\\'+ split_name + '.nii.gz'))

def main():
    # 数据所在文件地址
    get_work_path = " "
    dcm_list = get_dcm_fime_path(get_work_path)

    for path in dcm_list:
        dcm_images = readdcm(path)  # 读取文件
        save(path,dcm_images) 



if __name__ == '__main__':
    main()