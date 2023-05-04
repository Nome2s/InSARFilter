function main()

    clear all;clc

    % 图像长宽
    width = 2551;
    %length = 2108;
    
    % 创建主界面
    fig = uifigure('Name', 'Goldstein Filter', 'Position', [100 100 400 250]);

    % 创建文件路径标签
    filePathLabel = uilabel(fig, 'Position', [100 200 250 22], 'Text', '待处理文件路径:');

    % 创建浏览按钮
    browseButton = uibutton(fig, 'Text', '浏览', 'Position', [50 200 50 22], 'ButtonPushedFcn', @browseButtonPushed);

    % 创建滤波参数输入框和标签
    alphaEditField = uieditfield(fig, 'numeric', 'Position', [50 140 80 22], 'Value', 0.5);
    alphaLabel = uilabel(fig, 'Position', [50 165 80 22], 'Text', '滤波参数:');

    % 创建滑动窗口大小输入框和标签
    windowSizeEditField = uieditfield(fig, 'numeric', 'Position', [180 140 80 22], 'Value', 32);
    windowSizeLabel = uilabel(fig, 'Position', [180 165 80 22], 'Text', '滑动窗口大小:');

    % 创建滑动窗口步长输入框和标签
    stepSizeEditField = uieditfield(fig, 'numeric', 'Position', [310 140 80 22], 'Value', 8);
    stepSizeLabel = uilabel(fig, 'Position', [310 165 80 22], 'Text', '滑动窗口步长:');

    % 创建处理按钮
    processButton = uibutton(fig, 'Text', '处理', 'Position', [160 50 80 22], 'ButtonPushedFcn', @processButtonPushed);

    % 处理按钮的回调函数
    function processButtonPushed(~, ~)
        % 获取用户输入的滤波参数、滑动窗口大小和滑动窗口步长
        alpha = alphaEditField.Value;
        windowSize = windowSizeEditField.Value;
        stepSize = stepSizeEditField.Value;

        % 获取待处理的文件
        file = filePathLabel.Text;
        if ~strcmp(file, '待处理文件路径:')
            % 构造输出文件夹路径
            folderName = sprintf('filter_f%.1f_w%d_s%d', alpha, windowSize, stepSize);
            outputPath = fullfile('./data', folderName);

            % 如果输出文件夹不存在，则创建
            if ~exist(outputPath, 'dir')
                mkdir(outputPath);
            end

            % 读取干涉图复数数据
            data = read_int(file, width);
            
            % 显示滤波前的相位图
            phase = angle(data);
            figure,imagesc(phase,[-pi,pi]);colormap('jet');colorbar;
            title('Original Phase');

            % 计算并显示原图的幅值图
            amplitude = abs(data);
            figure, imagesc(log10(amplitude)); colormap('gray'); colorbar;
            title('Original Amplitude (log10 scale)');

            
            %显示原图像的（伪）相干图
            coh = est_cc(data, 5);
            figure,imagesc(coh);colormap('jet');colorbar;
            title('Coherence of Original Image');
            
            %显示原图的相位标准差
            ps_std = phase_std(data, 5);
            figure,imagesc(ps_std);colormap('jet');colorbar;
            title('Original Phase Standard Deviation')

            % 进行Goldstein滤波
            filteredData = goldstein_filter(data, alpha, windowSize, stepSize);

            % 显示滤波后的干涉图
            phase_out=angle(filteredData);
            figure,imagesc(phase_out,[-pi,pi]);colormap('jet');colorbar;
            title('Filtered Phase');

            % 计算并显示滤波后的幅值干涉图
            amplitude_out = abs(filteredData);
            figure, imagesc(log10(amplitude_out)); colormap('gray'); colorbar;
            title('Filtered Amplitude (log10 scale)');
            
            %显示滤波后图像的（伪）相干性
            coh = est_cc(filteredData, 5);
            figure,imagesc(coh);colormap('jet');colorbar;
            title('Coherence of Filtered Image');


            %显示滤波后图像的相位标准差
            ps_std_filtered = phase_std(data, 5);
            figure,imagesc(ps_std_filtered);colormap('jet');colorbar;
            title('Filtered Phase Standard Deviation')

            % 计算滤波前后的差值并显示
            diff=phase_out-phase;
            figure,imagesc(diff);colormap('jet');colorbar;
            title('Phase Difference');

            % 构造输出文件路径
            [~, ~] = fileparts(file);
            intOutputPath = fullfile(outputPath, 'filtered.int');
            imageOutputPath = fullfile(outputPath, 'filtered.int.tif');

            % 保存滤波后的int文件
            write_int(intOutputPath, filteredData);

            % 将滤波后的干涉图保存为图像
            phase2raster(filteredData, imageOutputPath);

            % 显示处理完成的消息对话框
            uialert(fig, '处理完成！', '提示', 'Icon', 'success');
        else
            uialert(fig, '请选择一个待处理的文件', '提示', 'Icon', 'warning');
        end
    end

    % 浏览按钮的回调函数
    function browseButtonPushed(~, ~)
        % 打开文件选择对话框
        [file, path] = uigetfile('*.int', '选择待处理的文件');

        % 如果选择了文件，则更新文件路径显示
        if file ~= 0
            filePath = fullfile(path, file);
            filePathLabel.Text = filePath;
        end
    end
end
