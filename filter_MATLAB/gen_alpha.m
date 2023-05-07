function alpha = gen_alpha(cpx, phi_max, phi_min)
% ----------------------------------
% 计算自适应滤波参数alpha，用于yu_filter
% 输入：
% cpx_global           局部干涉图复数矩阵
% phi_max              全局相位标准差最大值
% phi_min              全局相位标准差最小值
% 输出：
% alpha         自适应滤波参数，介于01之间的常数
% ----------------------------------


% 创建cpx的副本
cpx_copy = cpx;


% 将NaN值替换为0
cpx_copy(isnan(cpx_copy)) = 0;

phi_mean=mean(phase_std(cpx_copy,3),'all');

alpha=(phi_mean-phi_min)/(phi_max-phi_min);

end
