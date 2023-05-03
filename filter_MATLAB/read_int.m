function data=read_int(file_name,width)
% -------------------------------------
% 读取小端存储的二进制float类型的干涉图数据
% 输入参数：
%   file_name   干涉图数据文件名
%   width       干涉图宽度，即列数
% 输出：
%   data        干涉图复数矩阵
% -------------------------------------

fid=fopen(file_name,'r');
[data,count]=fread(fid,'float32');
fclose(fid);
data = complex(data(1:2:count),data(2:2:count));
lines=count/width/2;
data=reshape(data,width,lines).';