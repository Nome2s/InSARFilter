import numpy as np
# import S_T_coherence
import scipy
import scipy.interpolate
from dask.optimization import inline
from numpy.fft import ifftshift, ifft, fft2, fftshift, ifft2
from scipy.optimize import curve_fit
from scipy.signal import convolve2d
from scipy import optimize as op

def cv_goldstein_sim(IFG, left, CC_map, block=32, step=4, Alpha=0.35):
    # 多项式系数拟合
    # IFG 需要滤波的复数干涉图文件
    # left: Input the interferogram without fringes
    # CC_map: Input coherence map
    #  block: Filtering window, should be even a umber, such as 32 or 64, default 32
    # step: the step of sliding window
    # Alpha：可调节幂指数
    B=cv_alpha_fit (left, CC_map, block, step, Alpha)
    # B[0,0] = np.round(B[0,0], 2)
    # B[0,1] = np.round(B[0,1], 2)
    # B[0,2] = np.round(B[0,2], 2)
    Size_IFG=IFG.shape
    #  Set parameter
    lines = Size_IFG[0]
    width = Size_IFG[1]
    Filtered_IFG = 0*IFG
    Filtered_IFG = IFG
    # Calculate filtering image size
    overlap = (block - step) / 2
    Start_Col = overlap + 1
    End_Col = width - (block - overlap) + 1
    Start_Row = overlap + 1
    End_Row = lines - (block - overlap) + 1
    overlap=int(overlap)
    Start_Col = int(Start_Col)
    End_Col = int(End_Col)
    Start_Row = int(Start_Row)
    End_Row = int(End_Row)
    step=int(step)
    # 计算K函数
    N = 5
    K = np.ones((N, N))
    K = K /np.sum(np.sum(K,axis=1))
    K = fftshift(fft2(K))
#   滤波
    # up-left corner
    window = IFG[1-1:block,1-1:block]
    H = fft2(window)
    H = fftshift(H)
    S = scipy.signal.convolve2d(abs(H), K, 'same')
    S= (S - np.min(S))/(np.max(S)-np.min(S))
    tmp = np.reshape(S, (block * block, 1), order="F")
    tmp = abs(tmp)
    u = np.mean(tmp)
    sigma = np.std(tmp)
    cv = sigma/u
    alpha = Alpha
    S = S**(alpha)
    H = H*S
    H = ifftshift(H)
    H1 = ifft2(H)
    Filtered_IFG[1-1:block,1-1:block] = H1

    #up-right corner
    window = IFG[1-1:block, End_Col-overlap-1:width]
    H = fft2(window)
    H = fftshift(H)
    S = scipy.signal.convolve2d(abs(H), K, 'same')
    S = (S - np.min(S)) / (np.max(S) - np.min(S))
    tmp = np.reshape(S, (block * block, 1), order="F")
    tmp = abs(tmp)
    u = np.mean(tmp)
    sigma = np.std(tmp)
    cv = sigma / u
    # alpha = B[0,0]*((cv+B[0,2])**(-1))+B[0,1]
    S = S ** (alpha)
    H = H * S
    H = ifftshift(H)
    H1 = ifft2(H)
    Filtered_IFG[1-1:block, End_Col-overlap-1:width] = H1

    #down-left corner
    window = IFG[End_Row-overlap-1:lines,1-1:block]
    H = fft2(window)
    H = fftshift(H)
    S = scipy.signal.convolve2d(abs(H), K, 'same')
    S = (S - np.min(S)) / (np.max(S) - np.min(S))
    tmp = np.reshape(S, (block * block, 1), order="F")
    tmp = abs(tmp)
    u = np.mean(tmp)
    sigma = np.std(tmp)
    cv = sigma / u
    # alpha = B[0,0]*((cv+B[0,2])**(-1))+B[0,1]
    S = S ** (alpha)
    H = H * S
    H = ifftshift(H)
    H1 = ifft2(H)
    Filtered_IFG[End_Row-overlap-1:lines,1-1:block] = H1

    #down-right corner
    window = IFG[End_Row-overlap-1:lines,End_Col-overlap-1:width]
    H = fft2(window)
    H = fftshift(H)
    S = scipy.signal.convolve2d(abs(H), K, 'same')
    S = (S - np.min(S)) / (np.max(S) - np.min(S))
    tmp = np.reshape(S, (block * block, 1), order="F")
    tmp = abs(tmp)
    u = np.mean(tmp)
    sigma = np.std(tmp)
    cv = sigma / u
    # alpha = B[0,0]*((cv+B[0,2])**(-1))+B[0,1]
    S = S ** (alpha)
    H = H * S
    H = ifftshift(H)
    H1 = ifft2(H)
    Filtered_IFG[End_Row-overlap-1:lines,End_Col-overlap-1:width] = H1

    #Filter the first and last row

    for jj in range(Start_Col,End_Col,step):
        #first row
        window = IFG[1-1:block,jj-overlap-1:jj+(block-overlap)-1]
        H = fft2(window)
        H = fftshift(H)
        S = scipy.signal.convolve2d(abs(H), K, 'same')
        S = (S - np.min(S)) / (np.max(S) - np.min(S))
        tmp = np.reshape(S, (block * block, 1), order="F")
        tmp = abs(tmp)
        u = np.mean(tmp)
        sigma = np.std(tmp)
        cv = sigma / u
        # alpha = B[0,0]*((cv+B[0,2])**(-1))+B[0,1]
        S = S ** (alpha)
        H = H * S
        H = ifftshift(H)
        H1 = ifft2(H)
        Filtered_IFG[1-1:block, jj-1:jj+ step-1] = H1[:, overlap+1-1:block-overlap]

        # last row
        window = IFG[lines-block+1-1: lines, jj - overlap-1:jj + (block - overlap) - 1]
        H = fft2(window)
        H = fftshift(H)
        S = scipy.signal.convolve2d(abs(H), K, 'same')
        S = (S - np.min(S)) / (np.max(S) - np.min(S))
        tmp = np.reshape(S, (block * block, 1), order="F")
        tmp = abs(tmp)
        u = np.mean(tmp)
        sigma = np.std(tmp)
        cv = sigma / u
        # alpha = B[0,0]*((cv+B[0,2])**(-1))+B[0,1]
        S = S ** (alpha)
        H = H * S
        H = ifftshift(H)
        H1 = ifft2(H)
        Filtered_IFG[lines-block+1-1: lines,jj-1:jj+step-1] = H1[:,overlap+1-1:block-overlap]

    # Filter the first and last column

    for ii in range(Start_Row,End_Row,step):

        # first column
        window = IFG[ii - overlap-1:ii + (block - overlap) - 1,1-1:block]
        H = fft2(window)
        H = fftshift(H)
        S = scipy.signal.convolve2d(abs(H), K, 'same')
        S = (S - np.min(S)) / (np.max(S) - np.min(S))
        tmp = np.reshape(S, (block * block, 1), order="F")
        tmp = abs(tmp)
        u = np.mean(tmp)
        sigma = np.std(tmp)
        cv = sigma / u
        # alpha = B[0,0]*((cv+B[0,2])**(-1))+B[0,1]
        S = S ** (alpha)
        H = H * S
        H = ifftshift(H)
        H1 = ifft2(H)
        Filtered_IFG[ii-1:ii+step-1,1-1:block] = H1[overlap+1-1:block-overlap,:]

        # last column
        window = IFG[ii-overlap-1:ii+(block-overlap)-1,width-block+1-1:width]
        H = fft2(window)
        H = fftshift(H)
        S = scipy.signal.convolve2d(abs(H), K, 'same')
        S = (S - np.min(S)) / (np.max(S) - np.min(S))
        tmp = np.reshape(S, (block * block, 1), order="F")
        tmp = abs(tmp)
        u = np.mean(tmp)
        sigma = np.std(tmp)
        cv = sigma / u
        # alpha = B[0,0]*((cv+B[0,2])**(-1))+B[0,1]
        S = S ** (alpha)
        H = H * S
        H = ifftshift(H)
        H1 = ifft2(H)
        Filtered_IFG[ii-1:ii+step-1,width-block+1-1:width] = H1[overlap+1-1:block-overlap,:]

    # Filter the center part

    for ii in range(Start_Row,End_Row,step):
        for jj in range(Start_Col,End_Col,step):

            window = IFG[ii - overlap-1:ii + (block - overlap) - 1, jj-overlap-1:jj+(block-overlap)-1]
            H = fft2(window)
            H = fftshift(H)
            S = scipy.signal.convolve2d(abs(H), K, 'same')
            S = (S - np.min(S)) / (np.max(S) - np.min(S))
            tmp = np.reshape(S, (block * block, 1), order="F")
            tmp = abs(tmp)
            u = np.mean(tmp)
            sigma = np.std(tmp)
            cv = sigma / u
            # alpha = B[0,0]*((cv+B[0,2])**(-1))+B[0,1]
            S = S ** (alpha)
            H = H * S
            H = ifftshift(H)
            H1 = ifft2(H)
            a = H1[overlap + 1-1:block - overlap,overlap+1-1:block-overlap]
            Filtered_IFG[ii-1:ii + step - 1, jj-1:jj+step-1] = H1[overlap + 1-1:block - overlap,overlap+1-1:block-overlap]
    return Filtered_IFG, B
# def model(x, a):
#     return a[0]*((x+a[2]) ** (-1))+a[1]
def model(x, a, b, c):
    return a * ((x + c) ** (-1)) + b

def cv_alpha_fit(left, CC_map, block, step, Alpha):
    Size_IFG = left.shape
    Size_CC = CC_map.shape
    cv=cv_main(left, block, step)
    x_cv=np.array([[cv[0,0],cv[1,0],cv[2,0]]])
    y_alpha= np.array([[Alpha, Alpha, Alpha]])
    p=np.array([[1,0,0]])
    # x_cv = (x_cv[0], x_cv[0], x_cv[0])
    # y_alpha = (x_cv[0], x_cv[0], x_cv[0])
    # x_cv = (0.79, 1, 0)
    # y_alpha = (0.8, 0.9, 1)
    # model = lambda a, x: a[0]*((x+a[2]) ** (-1))+a[1]
    # B, R, J, Cov, MSE = nlinfit(x_cv, y_alpha, model, p)
    # B, cov = curve_fit(model, x_cv, y_alpha,p0=None)
    B=np.array([[1.15,0.05,-0.46]])
    # B=p
    return B

def cv_main(left, block, step):
    lines, width = left.shape
    overlap = (block - step) / 2
    Start_Col = overlap + 1
    End_Col = width-(block-overlap)+1
    Start_Row = overlap+1
    End_Row = lines-(block-overlap)+1
    n = (End_Col - Start_Col) / 4 + 1
    m = (End_Row - Start_Col) / 4 + 1
    m=int(m)
    n=int(n)
    End_Col = int(End_Col)
    overlap = int(overlap)
    End_Col = int(End_Col)
    End_Row = int(End_Row)
    Start_Row = int(Start_Row)
    Start_Col = int(Start_Col)
    CV = np.zeros((m + 2, n + 2))
    # up-left corner
    window = left[0:block, 0: block]
    cv = cv_calculation(window, block)
    CV[1-1, 1-1] = cv
    #  up-rightcorner

    window = left[1-1:block, End_Col - overlap-1: width]
    cv = cv_calculation(window, block)
    CV[1-1, n + 2-1] = cv
    #down-left corner
    window = left[End_Row - overlap-1:lines, 1-1: block]
    cv = cv_calculation(window, block)
    CV[m + 2-1, 1-1] = cv
    #down-right corner
    window = left[End_Row-overlap-1:lines,End_Col-overlap-1:width]
    cv = cv_calculation(window, block)
    CV[m+2-1,n+2-1]= cv
    # Filter the first and last row
    nn = 2
    for jj in range(Start_Col,End_Col,step):
        window = left[1-1:block, jj - overlap-1: jj + (block - overlap) - 1]
        cv = cv_calculation(window, block)
        CV[1-1, nn-1] = cv
        window = left[1-1:block,jj-overlap-1:jj+(block-overlap)]
        cv = cv_calculation(window, block)
        CV[m+2-1,nn-1] = cv
        nn = nn+1
    # Filter the first and last column
    mm = 2
    for ii in range(Start_Row,End_Row,step):
        window = left[ii - overlap-1:ii + (block - overlap) - 1, 1-1: block]
        cv = cv_calculation(window, block)
        CV[mm-1, 1-1] = cv
        window = left[ii-overlap-1:ii+(block-overlap)-1,width-block+1-1:width]
        cv=cv_calculation( window, block )
        CV[mm-1,n+2-1] = cv
        mm = mm+1
    # Calculate the center part
    mm = 2
    for ii in range(Start_Row, End_Row,step):
        nn = 2
        for jj in range(Start_Col,End_Col,step):
            window = left[ii - overlap-1:ii + (block - overlap) - 1, jj - overlap-1: jj + (block - overlap) - 1]
            cv = cv_calculation(window, block)
            CV[mm-1, nn-1] = cv
            nn = nn + 1
        mm = mm + 1
    cv = np.reshape(CV, ((m+2)*(n+2), 1), order="F")
    return cv

def cv_calculation ( window, block ):
    H = window[1-1:block, 1-1: block]
    H = fft2(H)
    H = fftshift(H)
    N = 3
    K = np.ones((N, N))
    K = K / np.sum(np.sum(K, axis=1))
    K = fftshift(fft2(K))
    S = scipy.signal.convolve2d(abs(H), K, 'same')
    S = (S - np.min(S))/(np.max(S)-np.min(S))
    tmp = np.reshape(S, (block * block, 1), order="F")
    tmp = abs(tmp)
    u = np.mean(tmp)
    sigma = np.std(tmp)
    cv= sigma/u
    return cv