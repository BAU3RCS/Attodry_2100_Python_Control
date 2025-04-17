% Get Cryo Z-magnet field         
function zMagField = getZMagField(isConnected)
    if isConnected=="True"
        MagFieldZ = libpointer('singlePtr',0);
        for i=1:2
            calllib('attoDRYxyz64bit','AttoDRY_Interface_getMagneticFieldZ',MagFieldZ);
            zMagField=MagFieldZ.Value*10000;
            pause(0.5);
        end
    else
        zMagField=-420;
    end
end