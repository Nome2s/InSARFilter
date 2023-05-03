function write_int(file_name,data)
% -------------------------------------
% 保存小端存储的二进制float类型的干涉图数据
% 输入参数：
%   file_name   保存的干涉图数据文件名
%   data        干涉图复数矩阵
% -------------------------------------

fid=fopen(file_name,'w');
data=data';
data=data(:);
[m,n]=size(data);
imag_data=sin(data);
real_data=cos(data);
count=m*2*n;
data=zeros(count,1);
data(1:2:count)=real_data;
data(2:2:count)=imag_data;
fwrite(fid,data,'float32');
fclose(fid);