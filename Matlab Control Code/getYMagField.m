 % Get Cryo Z-magnet field         
function yMagField = getYMagField(isConnected)
    if isConnected=="True"
        MagFieldY = libpointer('singlePtr',0);
        for i=1:2
            calllib('attoDRYxyz64bit','AttoDRY_Interface_getMagneticField',MagFieldY);
            yMagField=MagFieldY.Value*10000;
            pause(0.5);
        end
    else
        yMagField=-420;
    end
end