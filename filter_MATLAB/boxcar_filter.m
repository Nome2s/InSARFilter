function out_cpx = boxcar_filter(cpx, w)
    % 输入参数:
    % cpx - 需要滤波的干涉图复数矩阵
    % w - 滤波窗口的大小
    % 输出:
    % out_cpx - 滤波后的干涉图复数矩阵

    % 获取输入干涉图矩阵的行数和列数
    [rows, cols] = size(cpx);

    % 初始化输出干涉图复数矩阵
    out_cpx = complex(zeros(rows, cols));

    % 计算窗口大小对应的行列数
    half_w = floor(w / 2);

    % 遍历输入矩阵中的每个像素
    for r = 1:rows
        for c = 1:cols
            % 初始化滤波窗口内像素值的累计和
            sum_cpx = complex(0, 0);
            count = 0;

            % 遍历滤波窗口内的每个像素
            for i = -half_w:half_w
                for j = -half_w:half_w
                    % 计算当前像素在输入矩阵中的行列坐标
                    row_idx = r + i;
                    col_idx = c + j;

                    % 检查坐标是否在输入矩阵的范围内
                    if row_idx > 0 && row_idx <= rows && col_idx > 0 && col_idx <= cols
                        % 将当前像素值加入累计和
                        sum_cpx = sum_cpx + cpx(row_idx, col_idx);
                        count = count + 1;
                    end
                end
            end

            % 计算滤波后的像素值（平均值）
            out_cpx(r, c) = sum_cpx / count;
        end
    end



% 掩膜原来是空值的像元
idx=angle(cpx)==0;
out_cpx(idx)=0;
idx=isnan(angle(cpx));
out_cpx(idx)=nan;

end
