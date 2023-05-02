% GoldsteinFilter.m
function GoldsteinFilter(filter_strength, window_size, step_size)
    if nargin == 0
        filter_strength = 0.5;
        window_size = 32;
        step_size = 8;
    end

    % 从XML文件中读取信息
    xml_file = 'original.int.xml';
    xml_struct = xml2struct(xml_file);
    width = str2double(xml_struct.imageFile.property{10}.value.Text);
    length = str2double(xml_struct.imageFile.property{14}.value.Text);

    % 读取干涉图数据
    interferogram_file = 'original.int';
    interferogram = read_complex(interferogram_file, width, length);

    % 应用Goldstein滤波
    filtered_interferogram = apply_goldstein_filter(interferogram, filter_strength, window_size, step_size);

    % 保存滤波后的干涉图
    output_file = 'filtered.int';
    write_complex(filtered_interferogram, output_file);
end

function data = read_complex(filename, width, length)
    fid = fopen(filename, 'r');
    data = fread(fid, [2 * width, length], 'float32');
    fclose(fid);
    data = complex(data(1:2:end, :), data(2:2:end, :));
end

function write_complex(data, filename)
    [width, length] = size(data);
    output_data = zeros(2 * width, length);
    output_data(1:2:end, :) = real(data);
    output_data(2:2:end, :) = imag(data);

    fid = fopen(filename, 'w');
    fwrite(fid, output_data, 'float32');
    fclose(fid);
end

function filtered = apply_goldstein_filter(interferogram, filter_strength, window_size, step_size)
    [width, length] = size(interferogram);
    filtered = interferogram;

    for i = 1:step_size:width - window_size + 1
        for j = 1:step_size:length - window_size + 1
            window = interferogram(i:i + window_size - 1, j:j + window_size - 1);
            window_filtered = goldstein_filter_single_window(window, filter_strength);
            filtered(i:i + window_size - 1, j:j + window_size - 1) = window_filtered;
        end
    end
end

function filtered_window = goldstein_filter_single_window(window, filter_strength)
    phase_window = angle(window);
    unwrapped_phase = unwrap(phase_window);
    phase_gradient = gradient(unwrapped_phase);
    phase_variance = var(phase_gradient(:));

    alpha = filter_strength / phase_variance;
    window_spectrum = fft2(window);
    w_hat = exp(-alpha * phase_variance);
    filtered_spectrum = window_spectrum * w_hat;

    filtered_window = ifft2(filtered_spectrum);
end
