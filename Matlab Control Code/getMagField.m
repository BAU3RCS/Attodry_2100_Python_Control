% Get Cryo magnet field         
function [R,xMagField,yMagField,zMagField] = getMagField(isConnected)
    if isConnected=="True"
        MagFieldX = libpointer('singlePtr',0);
        MagFieldY = libpointer('singlePtr',0);
        MagFieldZ = libpointer('singlePtr',0);
        for i=1:2
            calllib('attoDRYxyz64bit','AttoDRY_Interface_getMagneticFieldX',MagFieldX);
            xMagField=MagFieldX.Value*10000;
            pause(0.2);
            calllib('attoDRYxyz64bit','AttoDRY_Interface_getMagneticFieldZ',MagFieldZ);
            zMagField=MagFieldZ.Value*10000;
            pause(0.2);
            calllib('attoDRYxyz64bit','AttoDRY_Interface_getMagneticField',MagFieldY);
            yMagField=MagFieldY.Value*10000;
            pause(0.2);
        end
        R = sqrt(xMagField^2 + yMagField^2 + zMagField^2);
    else
        xMagField=-420;
        yMagField=-420;
        zMagField=-420;
        R = -420;
    end
end


