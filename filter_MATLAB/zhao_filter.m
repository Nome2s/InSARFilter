% function out_cpx=zhao_filter(cpx, window_size, step_size)
% % --------------------------------------------
% % Zhao滤波
% % 输入参数：
% %   cpx             需要滤波的干涉图复数矩阵
% %   window_size     滑动窗口大小
% %   step_size       滑动窗口步长
% % 输出：
% %   out_cpx         滤波后的干涉图复数矩阵
% % --------------------------------------------
% 
% 
% % 构造均值卷积核
% K = ones(3, 3);
% K = K/sum(K(:));
% K = fftshift(fft2(K));
% 
% [rows,cols]=size(cpx);
% 
% % 创建cpx的副本
% cpx_copy = cpx;
% 
% % 将NaN值替换为0
% cpx_copy(isnan(cpx_copy)) = 0;
% 
% out_cpx=zeros(rows,cols);
% for ii=1:step_size:rows
%     for jj=1:step_size:cols
%         mm=ii+window_size-1;
%         if mm>rows
%             mm=rows;
%         end
%         nn=jj+window_size-1;
%         if nn>cols
%             nn=cols;
%         end
% % -----------------------------------------
%         window=cpx_copy(ii:mm,jj:nn);
%         % 计算相干系数
%         coh = gen_coh(window);
%         % 根据相干系数计算滤波参数alpha
%         alpha = 1 - coh;
% %这段是不同于Goldstein滤波的地方，这里的alpha是根据相干系数计算的，而Goldstein滤波中的alpha是固定的
% % -----------------------------------------
%         H=fft2(window);
%         H=fftshift(H);
%         % 使用均值卷积核平滑
%         S = conv2(abs(H),K,'same');
%         % 归一化 S
%         S = S./max(S(:));
%         S = S .^ alpha;
%         H = H .* S;
%         H=ifftshift(H);
%         window=ifft2(H);
%         out_cpx(ii:mm,jj:nn)=window;
%     end
% end
% % 掩膜原来是空值的像元
% idx=angle(cpx)==0;
% out_cpx(idx)=0;
% idx=isnan(angle(cpx));
% out_cpx(idx)=nan;
% end



function out_cpx = zhao_filter(cpx, window_size, step_size)
    % --------------------------------------------
    % Zhao滤波
    % 输入参数：
    %   cpx             需要滤波的干涉图复数矩阵
    %   window_size     滑动窗口大小
    %   step_size       滑动窗口步长
    %
    % 输出：
    %   out_cpx         滤波后的干涉图复数矩阵
    % --------------------------------------------
    % 构造均值卷积核
    K = ones(3, 3);
    K = K/sum(K(:));
    K = fftshift(fft2(K));

    % 构造权阵
    if mod(window_size,2)~=0
        window_size=window_size-1;
    end
    x=[1:window_size/2];
    [X,Y]=meshgrid(x,x);
    X=X+Y;
    weight=[X,fliplr(X)];
    weight=[weight;flipud(weight)];

    [rows,cols]=size(cpx);
    out_cpx=zeros(rows,cols);

    % 创建cpx的副本
    cpx_copy = cpx;

    % 将NaN值替换为0
    cpx_copy(isnan(cpx_copy)) = 0;

    for ii=1:step_size:rows
        for jj=1:step_size:cols
            mm=ii+window_size-1;
            if mm>rows
                mm=rows;
            end
            nn=jj+window_size-1;
            if nn>cols
                nn=cols;
            end
            window=cpx_copy(ii:mm,jj:nn);
            ww=weight(1:(mm-ii+1),1:(nn-jj+1));
            % 计算相干系数
            coh = gen_coh(window);
            % 根据相干系数计算滤波参数alpha
            alpha = 1 - coh;
            H=fft2(window);
            H=fftshift(H);
            % 使用均值卷积核平滑
            S = conv2(abs(H),K,'same');
            % 归一化 S
            S = S./max(S(:));
            S = S .^ alpha;
            H = H .* S;
            H=ifftshift(H);
            window=ifft2(H);
            out_cpx(ii:mm,jj:nn)=out_cpx(ii:mm,jj:nn)+window.*ww;
        end
    end
    % 掩膜原来是空值的像元
    idx=angle(cpx)==0;
    out_cpx(idx)=0;
    idx=isnan(angle(cpx));
    out_cpx(idx)=nan;
end
