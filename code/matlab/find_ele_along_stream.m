clear;close all;clc;
​
str = fileread('flowline_simplified.geojson');
data = jsondecode(str);
​
tile = 'n35w080';
if strcmp(tile(1),'n')
    ymin = str2double(tile(2:3));
elseif strcmp(tile(1),'s')
    ymin = -str2double(tile(2:3));
end
​
ymax = ymin + 5;
​
if strcmp(tile(4),'w')
    xmin = -str2double(tile(5:7));
elseif strcmp(tile(4),'e')
    xmin = str2double(tile(5:7));
end
​
xmax = xmin + 5;
​
dx = 5 / 6000;
dy = 5 / 6000;
​
x = xmin + dx/2 : dx : xmax - dx/2;
y = ymax - dy/2 : -dy : ymin + dy/2;
​
ix = find( x >= -76.6 & x <= -75.9);
iy = find( y >= 39.4  & y <= 40);
​
[x,y] = meshgrid(x(ix),y(iy));
    
dem = double(imread('n35w080_dem.tif'));
dem = dem(iy(1) : iy(end), ix(1) : ix(end));
​
​
figure;
dem(dem == -9999) = NaN;
imAlpha = ones(size(dem));
imAlpha(isnan(dem)) = 0;
imagesc([x(1,1),x(end,end)],[y(1,1),y(end,end)],dem,'AlphaData',imAlpha); hold on;   
set(gca,'YDir','normal'); hold on; colormap(gca,viridis);
​
for i = 1 %: 7
    coord = data.features(i).geometry.coordinates;
    plot(coord(1,1),coord(1,2),'go'); hold on;
    plot(coord(:,1),coord(:,2),'-'); 
end
​
ind = find(abs(coord(:,2) - 40) == min(abs(coord(:,2) - 40)));
​
dem_stream  = [];
travel_dist = [];
​
proj = projcrs(3338,'Authority','EPSG');
​
for i = length(coord(:,2)) : - 1 : ind
    disp(['i = ' num2str(i) '\' num2str(length(coord(:,2)))]);
    dist = (x - coord(i,1)).^2 + (y - coord(i,2)).^2;
    [~,imin] = sort(dist(:));
    imin = imin(1:20);
    dem_stream = [dem_stream; nanmean(dem(imin))];
    if i == length(coord(:,2))
        td = 0;
    else
        [tmpx1,tmpy1] = projfwd(proj,coord(i,2),coord(i,1));
        [tmpx2,tmpy2] = projfwd(proj,coord(i+1,2),coord(i+1,1));
        td = td + sqrt((tmpx1 - tmpx2)^2 + (tmpy1 - tmpy2)^2);
    end
    travel_dist = [travel_dist; td];
end
figure;
plot(travel_dist,dem_stream,'k-','LineWidth',2); grid on;
ylabel('Elevation [m]','FontSize',15,'FontWeight','bold');
xlabel('Travel distance [m]','FontSize',15,'FontWeight','bold');