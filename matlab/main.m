 %% Load all that data!
offset_table = readtable("offset_from165.csv");
offset = table2array(offset_table);
header = string(offset_table.Properties.VariableNames);

b14_table = readtable("14bit_reading.csv");
b14 = table2array(b14_table);

distances = 0:7;
heights = load("heights.csv");

%% Visualize that data!
[distances_m, heights_m] = meshgrid(heights, distances);
figure;
mesh(heights_m, distances_m, offset)
title("Offset From 1.65 output for each height and displacement")
ylabel("heights (mm)")
xlabel("distances (mm)")

figure;
mesh(heights_m, distances_m, b14)
title("14 bit readings output for each height and displacement")
ylabel("heights (mm)")
xlabel("distances (mm)")

%% Fit that data! 
hm = heights_m(:);
dm = distances_m(:);
offsetm = offset(:);
b14m = b14(:);

figure;
f_offset = fit([hm, dm], offsetm,'cubicinterp');
%f_offset = fit([hm, dm], offsetm,'thinplateinterp');
plot(f_offset, [hm, dm], offsetm);
title("Offset From 1.65 output for each height and displacement");
ylabel("heights (mm)");
xlabel("distances (mm)");

figure;
f_b14 = fit([hm, dm], b14m,'cubicinterp');
%f_b14 = fit([hm, dm], b14m,['thinplateinterp']);
plot(f_b14, [hm, dm], b14m);
title("14 bit readings output for each height and displacement");
ylabel("heights (mm)");
xlabel("distances (mm)");

%% Mkay though what are these fittings tho?
disp(f_offset);

% Save the coefficients and formula
offset_coeffs = coeffvalues(f_offset); % Extract coefficients
offset_formula = formula(f_offset);    % Extract formula
save('sfit_offset.mat', 'offset_coeffs', 'offset_formula');

disp(f_b14);

% Save the coefficients and formula
b14_coeffs = coeffvalues(f_b14); % Extract coefficients
b14_formula = formula(f_b14);    % Extract formula
save('sfit_b14.mat', 'b14_coeffs', 'b14_formula');

%% Fit that data again! (but this time with only ONE particular chess piece)...
for i = 1:size(offset,1)
    x_dense = linspace(min(distances), max(distances), 100)';

    f_offset = fit(distances', offset(:, i),'pchipinterp');
    figure;
    plot(f_offset, distances', offset(:, i));
    title("Offset From 1.65 output v displacement (" + header(i) + ")");
    xlabel("distances (mm)");
    ylabel("sensor output");
    % Generate dense grid for interpolation
    y_dense = f_offset(x_dense');
    writematrix([y_dense], strcat(header(i), '_sfit_offset.csv'));

    f_b14 = fit(distances', b14(:, i),'pchipinterp');
    figure;
    plot(f_b14, distances', b14(:, i));
    title("14 bit reading v displacement (" + header(i) + ")");
    xlabel("distances (mm)");
    ylabel("sensor output");
    % Generate dense grid for interpolation
    y_dense = f_b14(x_dense');
    writematrix([y_dense], strcat(header(i), '_sfit_b14.csv'));
end

%% Fit that data again again! (but this time with only ONE particular position displacement)...
for i = 1:size(offset,2)+2
    x_dense = linspace(min(heights), max(heights), 100)';

    f_offset = fit(heights', offset(i, :)','pchipinterp');
    figure;
    plot(f_offset, heights', offset(i, :));
    title("Offset From 1.65 output v heights (" + string(distances(i)) + ")");
    xlabel("heights (mm)");
    ylabel("sensor output");
    % Generate dense grid for interpolation
    y_dense = f_offset(x_dense');
    writematrix([y_dense], strcat(string(distances(i)), '_sfit_offset.csv'));

    f_b14 = fit(heights', b14(i, :)','pchipinterp');
    figure;
    plot(f_b14, heights', b14(i, :));
    title("14 bit reading v displacement (" + string(distances(i)) + ")");
    xlabel("heights (mm)");
    ylabel("sensor output");
    % Generate dense grid for interpolation
    y_dense = f_b14(x_dense');
    writematrix([y_dense], strcat(string(distances(i)), '_sfit_b14.csv'));
end