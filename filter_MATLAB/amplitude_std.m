function astd = amplitude_std(cpx, window_size)
% ----------------------------------
% 计算干涉图的幅值标准差
% 输入：
%   cpx           干涉图复数矩阵
%   window_size   估计窗口大小,为奇数，如 5,7,9,...
% 输出：
%   astd          幅值标准差
% ----------------------------------

R = floor((window_size-1)/2);
[rows,cols] = size(cpx);
astd = zeros(rows,cols);
mask = ones(rows,cols);
idx = isnan(cpx);
mask(idx) = 0;
for ii = 1:rows
    for jj = 1:cols
        if mask(ii,jj) == 0
            astd(ii,jj) = nan;
            continue;
        end
        mm0 = ii-R;
        if mm0 < 1
            mm0 = 1;
        end
        mm1 = ii+R;
        if mm1 > rows
            mm1 = rows;
        end
        nn0 = jj-R;
        if nn0 < 1
            nn0 = 1;
        end
        nn1 = jj+R;
        if nn1 > cols
            nn1 = cols;
        end
        window = cpx(mm0:mm1,nn0:nn1);
        idx = ~isnan(window);
        amplitude = abs(window(idx));
        astd(ii,jj) = std(amplitude(:));%这个函数是matlab自带的，容易出错
    end
end
