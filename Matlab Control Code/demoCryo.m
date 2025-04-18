% clear;
% clc;
isConnected = cryoAttoDry.connectCryo('COM3');
R=200;%170;%2.3797e+03;%1660;
theta=-15;%85.5;%87.2;%47;%60.3;%53.5;%56.67;%53.5;
phi=5;%100;%98;%34.5;%38.6;%38;%38.4;%38.6; %38

% Bx=-86.84;
% By=(-18.3843);
% Bz=-1.2217;
%               
% 
% R=sqrt(Bx^2+By^2+Bz^2);
% theta=acos(Bz/R)*180/3.14159265359;
% phi=atan(By/Bx)*180/3.14159265359;
% if(Bx<0&&By<0)
%     phi=-180+atan(By/Bx)*180/3.14159265359;
% end
% if(Bx<0&&By>0)
%     phi=180+atan(By/Bx)*180/3.14159265359;
% end

cryoAttoDry.setVectorField(isConnected,R,theta,phi);
disp("Done");
cryoAttoDry.getSampleTemp(isConnected)
%cryoAttoDry.disconnectCryo(isConnected);
%pause(10);
[r,x,y,z]=getMagField(isConnected);
%cryoAttoDry.setUserTemp(isConnected,300);
disp(r);