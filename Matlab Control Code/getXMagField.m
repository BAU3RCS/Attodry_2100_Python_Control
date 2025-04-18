% Get Cryo X-magnet field         
function [xMagField,yMagField,zMagField] = getMagField(isConnected)
    if isConnected=="True"
        MagFieldX = libpointer('singlePtr',0);
        MagFieldY = libpointer('singlePtr',0);
        for i=1:2
            calllib('attoDRYxyz64bit','AttoDRY_Interface_getMagneticFieldX',MagFieldX);
            xMagField=MagFieldX.Value*10000;
            pause(0.5);
        end
    else
        xMagField=-420;
    end
end
