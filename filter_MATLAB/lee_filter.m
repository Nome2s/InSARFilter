function out_cpx = lee_filter(cpx, w)
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

    % 计算全局噪声方差
    global_noise_var = var(cpx(:));

    % 遍历输入矩阵中的每个像素
    for r = 1:rows
        for c = 1:cols
            % 初始化局部均值和局部方差
            local_mean = complex(0, 0);
            local_var = complex(0, 0);
            count = 0;

            % 遍历滤波窗口内的每个像素
            for i = -half_w:half_w
                for j = -half_w:half_w
                    % 计算当前像素在输入矩阵中的行列坐标
                    row_idx = r + i;
                    col_idx = c + j;

                    % 检查坐标是否在输入矩阵的范围内
                    if row_idx > 0 && row_idx <= rows && col_idx > 0 && col_idx <= cols
                        % 更新局部均值
                        local_mean = local_mean + cpx(row_idx, col_idx);
                        count = count + 1;
                    end
                end
            end

            % 计算局部均值
            local_mean = local_mean / count;

            % 计算局部方差
            for i = -half_w:half_w
                for j = -half_w:half_w
                    row_idx = r + i;
                    col_idx = c + j;

                    if row_idx > 0 && row_idx <= rows && col_idx > 0 && col_idx <= cols
                        local_var = local_var + (cpx(row_idx, col_idx) - local_mean) * conj(cpx(row_idx, col_idx) - local_mean);
                    end
                end
            end

            local_var = local_var / count;

            % 计算滤波权重
            filter_weight = (global_noise_var - local_var) / global_noise_var;
            filter_weight = max(min(real(filter_weight), 1), 0);  % 限制滤波权重在0到1之间

            % 计算滤波后的像素值
            filtered_pixel = filter_weight * cpx(r, c) + (1 - filter_weight) * local_mean;

            % 将滤波后的像素值存储到输出矩阵中
            out_cpx(r, c) = filtered_pixel;
        end
    end

    % 对掩膜原来是空值的像元进行处理
    idx = angle(cpx) == 0;
    out_cpx(idx) = 0;
    idx = isnan(angle(cpx));
    out_cpx(idx) = nan;
end
