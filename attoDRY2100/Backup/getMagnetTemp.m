function magnetTemp = getMagnetTemp()
    if libisloaded('attoDRYxyz64bit')
        MagnetTemperature = libpointer('singlePtr',0);
        calllib('attoDRYxyz64bit','AttoDRY_Interface_get4KStageTemperature',MagnetTemperature);
        magnetTemp=MagnetTemperature.Value;
        for i=1:6
            calllib('attoDRYxyz64bit','AttoDRY_Interface_get4KStageTemperature',MagnetTemperature);
            if MagnetTemperature.Value>0
                magnetTemp=MagnetTemperature.Value;
                break
            end
        end
    else
        magnetTemp=-1;
    end
    
end

