close all;clear;clc;
% 图像长宽
width=2551;
length=2108;

% 读取数据
data=read_int('data/original/original.int',width);
phase=angle(data);

% 显示滤波前的干涉图
figure,imagesc(phase,[-pi,pi]);colormap('jet');colorbar;
title('Original Image');

% 滤波
data_filter=goldstein_filter(data,0.5,32,8);

% 显示滤波后的干涉图
phase_out=angle(data_filter);
figure,imagesc(phase_out,[-pi,pi]);colormap('jet');colorbar;
title('Filtered Image')

% 计算滤波前后的差值并显示
diff=phase_out-phase;
figure,imagesc(diff);colormap('jet');colorbar;
title('Phase Difference')

% 保存滤波后的结果
write_int('data/out.int',data_filter);

% 输出图像，jet色带
phase2raster(data,'data/original.int.tif');
phase2raster(data_filter,'data/out.int.tif');
