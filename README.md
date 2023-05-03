# GoldsteinFilter
InSAR中经典的Goldstein滤波算法的实现

## Requirements

download at:https://disk.pku.edu.cn:443/link/5CB824412F45BBA73FA67BE18DE2F993 


Using Python or other programming languages to implement the interferogram filtering algorithm in the following paper

Goldstein and Werner, 1998, Radar interferogram filtering for geophysical applications, GEOPHYSICAL RESEARCH LETTERS.

The resulting program should accept the following user-controlled parameters

(1) filter strength
(2) filter window size
(3) moving step size of the filter window

For doing test, commonly used filtering parameters are as follows
(1) filter strength: 0.5
(2) filter window size: 32
(3) moving step size of the filter window: 8
You can try different parameters to see the resulting filtering effects.


The interferogram for doing test is also provided. It is a simple 2-d matrix. There is only one band in the image. Each pixel is a complex number, and has a real part and an imaginary part, both in four-byte float format. The interferogram is stored as


real_part imaginary_part real_part imaginary_part ... real_part imaginary_part

real_part imaginary_part real_part imaginary_part ... real_part imaginary_part

...

real_part imaginary_part real_part imaginary_part ... real_part imaginary_part



You can import the interferogram into any image applications, such as Python, Matlab and ENVI. You can view its phase and magnitude. Magnitude usually has a large dynamic range, so you can take its logarithm when displaying it.


Below is the list of the files.

* Goldstein_1998_Radar interferogram filtering for geophysical applications.pdf --- The paper
* diff_150405-150503_10rlks_56alks.int --- the interferogram for doing test
* diff_150405-150503_10rlks_56alks.int.xml --- xml file specifying interferogram size, precision, etc.
* diff_150405-150503_10rlks_56alks.int.tif --- a false color image of the phase of the inteferogram. You should be able to see the same thing in any image applications when you display the interferogram, although you may use a different colormap, e.g. rainbow, jet etc.



Results should include:

* your codes
* experimental results with your codes, e.g. images before and after filtering (such as diff_150405-150503_10rlks_56alks.int.tif), parameters you used for filtering.
* a simple report about your work in which you discuss your insights into the method, e.g., why it works as a filter, possible improvements, etc.

## 要求

下载地址：https://disk.pku.edu.cn:443/link/5CB824412F45BBA73FA67BE18DE2F993

使用Python或其他编程语言来实现以下论文中的干涉图滤波算法。

Goldstein and Werner, 1998, Radar interferogram filtering for geophysical applications, GEOPHYSICAL RESEARCH LETTERS.

由此产生的程序应接受以下用户控制的参数

(1) 滤波强度
(2) 滤波器窗口大小
(3) 滤波窗口的移动步骤大小

在做试验时，常用的滤波参数如下
(1) 滤波强度：0.5
(2) 滤波窗大小：32
(3) 滤波窗的移动步长： 8
你可以尝试不同的参数，看看产生的滤波效果。

还提供了做测试的干涉图。它是一个简单的2维矩阵。图像中只有一个波段。每个像素是一个复数，有一个实部和一个虚部，都是四字节的浮点数格式。干涉图被存储为

real_part imaginary_part real_part imaginary_part ... real_part imaginary_part

real_part imaginary_part real_part imaginary_part ... real_part imaginary_part

...

real_part imaginary_part real_part imaginary_part ... real_part imaginary_part

你可以将干涉图导入任何图像应用程序，如Python、Matlab和ENVI。你可以查看它的相位和幅值。幅值通常有很大的动态范围，所以你可以在显示它时取其对数。

下面是文件的列表。

- Goldstein_1998_地球物理应用中的雷达干涉图滤波.pdf ---该论文

- diff_150405-150503_10rlks_56alks.int ---做测试的干涉图

- diff_150405-150503_10rlks_56alks.int.xml ---指定干涉图大小、精度等的xml文件。

- diff_150405-150503_10rlks_56alks.int.tif ---干涉图的相位的假彩色图像。当你显示干涉图时，你应该能在任何图像应用程序中看到同样的东西，尽管你可以使用不同的颜色映射，如rainbow, jet等。

你的结果应包括：

- 你的代码

- 用你的代码进行的实验结果，例如过滤前后的图像（如diff_150405-150503_10rlks_56alks.int.tif），你用于过滤的参数。

- 一份关于你的工作的简单报告，在报告中谈谈你对这个方法的见解，例如，为什么它能起到滤波的作用，可能的改进方法等
