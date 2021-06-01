# Segmentation-of-pulmonary-embolism

肺栓塞分割 网络nnUnet

### 数据预处理  dataProcess

> ImaTFNii.py

将IMA后缀的文件，转成nii
> reMask.py

维度扩充，将mask的维度扩充成和dicom相同的维度
> reLable.py

将label矫正成只有0和1，即大于0的全部设置为1

> 3DNiiVolume.py

肺栓塞体积计算



### 肺栓塞检测与分割

网络模型 nnUnet

> 数据格式

nnUNet_raw_data_base
	|--datasets
    	|--test
        	|--image：测试的nii格式数据
            |--mask
        |--train
       		|--image：训练的nii格式数据
            |--mask：mask标注也是nii格式

> 训练

```
Python main_train.py
```

