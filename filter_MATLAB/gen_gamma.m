function gamma = gen_gamma(cpx)
% ----------------------------------
% 计算干涉图的相干系数
% 输入：
% cpx           干涉图复数矩阵
% 输出：
% gamma         整个干涉图的相干系数，介于01之间的常数
% ----------------------------------

% 创建一个掩码，用于忽略NaN值
non_nan_mask = ~isnan(cpx);

% 计算干涉图的相干系数
sum_cpx = abs(sum(cpx(non_nan_mask)));  % 计算cpx中非NaN元素的和的绝对值
abs_cpx = abs(cpx);          % 计算cpx中所有元素的绝对值
sum_abs_cpx = sum(abs_cpx(non_nan_mask));   % 计算cpx中非NaN元素的绝对值的和
gamma = sum_cpx / sum_abs_cpx;   % 计算整个干涉图的相干系数

end
