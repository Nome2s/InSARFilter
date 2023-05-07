function cc=est_cc(cpx, window_size)
% ----------------------------------
% 估计干涉图的伪相干性
% 输入：
% cpx           干涉图复数矩阵
% window_size   估计窗口大小,为奇数，如 5,7,9,...
% 输出：
% cc            伪相干矩阵
% ----------------------------------

R=floor((window_size-1)/2);
[rows,cols]=size(cpx);
cc=zeros(rows,cols);
mask=ones(rows,cols);
idx=isnan(cpx);
mask(idx)=0;
cpx_copy=cpx;
cpx_copy(idx)=0;


for ii=1:rows
    for jj=1:cols
        if mask(ii,jj)==0
            cc(ii,jj)=0;
            continue;
        end
        mm0=ii-R;
        if mm0<1
            mm0=1;
        end
        mm1=ii+R;
        if mm1>rows
            mm1=rows;
        end
        nn0=jj-R;
        if nn0<1
            nn0=1;
        end
        nn1=jj+R;
        if nn1>cols
            nn1=cols;
        end
        window=cpx_copy(mm0:mm1,nn0:nn1);
        sum_window=abs(sum(window(:)));
        abs_window=abs(window);
        sum_abs=sum(abs_window(:));
        cc(ii,jj)=sum_window/sum_abs;
    end
end