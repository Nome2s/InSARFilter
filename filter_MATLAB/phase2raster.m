function phase2raster(cpx,out_file_name)
% -------------------------------------------------------
% 将干涉图输出为高分辨率的栅格图像，方便查看，如png，tif，bmp等格式
% 输入参数：
%   cpx             干涉图复数数据矩阵
%   out_file_name   输出文件名
% -------------------------------------------------------

% 获取相位主值
phase=angle(cpx);
% 归一化
phase=(phase+pi)/(2*pi);
phase_rgb = ind2rgb(gray2ind(phase,255),jet(255));
% figure,imshow(phase_rgb);
imwrite(phase_rgb,out_file_name);

%%此函数在主函数中不再使用，但是可以生成高分辨率的tif图像，故保留