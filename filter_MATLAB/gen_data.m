function gen_data()
%批量产生数据，为实验报告提供素材


    for alpha=0:0.1:1


            width = 2551;
            % 获取待处理的文件
            file = './data/original/original.int';
        
            % 读取干涉图复数数据
            data = read_int(file, width);
            windowSize=32;
            stepSize=8;

            %显示参数
            display(alpha);


            % 构造输出文件夹路径
            folderName = sprintf('%s_f%.1f_w%d_s%d', 'Goldstein', alpha, windowSize, stepSize);

            outputPath = fullfile('./data', folderName);

            % 如果输出文件夹不存在，则创建
            if ~exist(outputPath, 'dir')
                mkdir(outputPath);
            end


            % 显示滤波前的相位图
            phase = angle(data);
            figure, imagesc(phase,[-pi,pi]); colormap('jet'); colorbar;
            title('Original Phase');
            saveas(gcf, fullfile(outputPath, 'OriginalPhase'), 'tiffn');
        
            % 计算并显示原图的幅值图
            amplitude = abs(data);
            figure, imagesc(log10(amplitude)); colormap('gray'); colorbar;
            title('Original Amplitude (log10 scale)');
            saveas(gcf, fullfile(outputPath, 'OriginalAmplitude'), 'tiffn');
        
        
            % 显示原图的幅度图直方图
            figure, histogram(log10(amplitude), 'BinEdges', -2.5:0.005:2.5, 'Normalization', 'probability');
            title('Histogram of Original Amplitude (log10 scale)');
            xlabel('Amplitude');
            ylabel('Probability');
            xlim([-2.5 2.5]);
            saveas(gcf, fullfile(outputPath, 'OriginalHistogram'), 'tiffn');
        
            %显示原图像的（伪）相干图
            coh = est_cc(data, 5);
            figure, imagesc(coh); colormap('jet'); colorbar;
            title('Coherence of Original Image');
            saveas(gcf, fullfile(outputPath, 'OriginalcCoh'), 'tiffn');
        
            %显示原图的相位标准差
            ps_std = phase_std(data, 5);
            figure, imagesc(ps_std); colormap('jet'); colorbar;
            title('Original Phase Standard Deviation');
            saveas(gcf, fullfile(outputPath, 'OriginalPhaseStd'), 'tiffn');

            %打印原图相位平均标准差
            display('Original Phase Standard Deviation Mean:');
            display(mean(ps_std(:)));

            %显示原图像相位标准差的直方图
            figure, histogram(ps_std, 'BinEdges', 0:0.005:3.5, 'Normalization', 'probability');
            title('Histogram of Original Phase Standard Deviation');
            xlabel('Phase Standard Deviation');
            ylabel('Probability');
            xlim([0 3.5]);
            saveas(gcf, fullfile(outputPath, 'OriginalPhaseStdHistogram'), 'tiffn');

            %显示原图的幅值标准差
            amplitude_std_original = amplitude_std(data, 5);
            figure, imagesc(amplitude_std_original); colormap('jet'); colorbar;
            title('Original Amplitude Standard Deviation');
            saveas(gcf, fullfile(outputPath, 'OriginalAmplitudeStd'), 'tiffn');

            %打印原图幅值平均标准差
            display('Original Amplitude Standard Deviation Mean:');
            display(mean(amplitude_std_original(:)));

            %显示原图像幅值标准差的直方图
            figure, histogram(amplitude_std_original, 'BinEdges', 0:0.005:3.5, 'Normalization', 'probability');
            title('Histogram of Original Amplitude Standard Deviation');
            xlabel('Amplitude Standard Deviation');
            ylabel('Probability');
            xlim([0 3.5]);
            saveas(gcf, fullfile(outputPath, 'OriginalAmplitudeStdHistogram'), 'tiffn');

            % 执行滤波
            
            filteredData = goldstein_filter(data, alpha, windowSize, stepSize);

            % 显示滤波后的相位图
            phase_out=angle(filteredData);
            figure, imagesc(phase_out,[-pi,pi]); colormap('jet'); colorbar;
            title('Filtered Phase');
            saveas(gcf, fullfile(outputPath, 'FilteredPhase'), 'tiffn');
        
            % 计算并显示滤波后的幅值图
            amplitude_out = abs(filteredData);
            figure, imagesc(log10(amplitude_out)); colormap('gray'); colorbar;
            title('Filtered Amplitude (log10 scale)');
            saveas(gcf, fullfile(outputPath, 'FilteredAmplitude'), 'tiffn');

            % 显示滤波后的幅度直方图
            figure, histogram(log10(amplitude_out), 'BinEdges', -2.5:0.005:2.5, 'Normalization', 'probability');
            title('Histogram of Filtered Amplitude (log10 scale)');
            xlabel('Amplitude');
            ylabel('Probability');
            xlim([-2.5 2.5]);
            saveas(gcf, fullfile(outputPath, 'FilteredHistogram'), 'tiffn');
        
            %显示滤波后图像的（伪）相干性
            coh_filetered = est_cc(filteredData, 5);
            figure, imagesc(coh_filetered); colormap('jet'); colorbar;
            title('Coherence of Filtered Image');
            saveas(gcf, fullfile(outputPath, 'FilteredCoh'), 'tiffn');
        
            %显示滤波后图像的相位标准差
            ps_std_filtered = phase_std(filteredData, 5);
            figure, imagesc(ps_std_filtered); colormap('jet'); colorbar;
            title('Filtered Phase Standard Deviation');
            saveas(gcf, fullfile(outputPath, 'FilteredPhaseStd'), 'tiffn');

            %打印滤波后图像相位平均标准差
            display('Filtered Phase Standard Deviation Mean:');
            display(mean(ps_std_filtered(:)));

            %显示滤波后图像相位标准差的直方图
            figure, histogram(ps_std_filtered, 'BinEdges', 0:0.005:3.5, 'Normalization', 'probability');
            title('Histogram of Filtered Phase Standard Deviation');
            xlabel('Phase Standard Deviation');
            ylabel('Probability');
            xlim([0 3.5]);
            saveas(gcf, fullfile(outputPath, 'FilteredPhaseStdHistogram'), 'tiffn');

            %显示滤波后图像的幅值标准差
            amplitude_std_filtered = amplitude_std(filteredData, 5);
            figure, imagesc(amplitude_std_filtered); colormap('jet'); colorbar;
            title('Filtered Amplitude Standard Deviation');
            saveas(gcf, fullfile(outputPath, 'FilteredAmplitudeStd'), 'tiffn');


            %打印滤波后图像幅值平均标准差
            display('Filtered Amplitude Standard Deviation Mean:');
            display(mean(amplitude_std_filtered(:)));


            %显示滤波后图像幅值标准差的直方图
            figure, histogram(amplitude_std_filtered, 'BinEdges', 0:0.005:3.5, 'Normalization', 'probability');
            title('Histogram of Filtered Amplitude Standard Deviation');
            xlabel('Amplitude Standard Deviation');
            ylabel('Probability');
            xlim([0 3.5]);
            saveas(gcf, fullfile(outputPath, 'FilteredAmplitudeStdHistogram'), 'tiffn');

            
            % 计算滤波前后相位的差值并显示
            phase_diff=phase_out-phase;
            figure, imagesc(phase_diff); colormap('jet'); colorbar;
            title('Phase Difference');
            saveas(gcf, fullfile(outputPath, 'PhaseDiff'),  'tiffn');

            % 计算滤波后相干性的差值并显示
            coh_diff=coh_filetered-coh;
            figure, imagesc(coh_diff); colormap('jet'); colorbar;
            title('Coherence Difference');
            saveas(gcf, fullfile(outputPath, 'CohDiff'),  'tiffn');

            % 计算相干性差直方图并显示
            figure, histogram(coh_diff, 'BinEdges', -1:0.01:1, 'Normalization', 'probability');
            title('Histogram of Coherence Difference');
            xlabel('Coherence Difference');
            ylabel('Probability');
            xlim([-1 1]);
            saveas(gcf, fullfile(outputPath, 'CohDiffHistogram'), 'tiffn');



            % 构造输出文件路径
            [~, ~] = fileparts(file);
            intOutputPath = fullfile(outputPath, 'filtered.int');

            % 保存滤波后的int文件
            write_int(intOutputPath, filteredData);


            clear all;
            close all;
    end
end
