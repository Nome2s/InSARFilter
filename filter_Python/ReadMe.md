# Goldstein滤波算法及其Python实现

## 文件说明

`original.int`：用于测试的干涉图原图

`original.int.tif`：原干涉图相位的假彩色图像

`original.int.xml`：指定原干涉图大小、精度等的xml文件

`filtered_test.int`：经过滤波后的干涉图

`filtered_test.int.tif`.：经过滤波后的干涉图的假彩色图像

`goldstein_filter.py`：对int文件进行滤波的程序，该代码从命令行接收参数，例如：

```shell
python goldstein_filter.py original.int [0.5] [32] [8]
```

`gen_tif.py`：将int文件转化为tif文件，需要在命令行中提供文件名、宽度和高度作为参数。例如：

```shell
python gen_tif.py filtered_test.int 2551 2108
```

