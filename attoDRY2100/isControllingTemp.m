function tempControl = isControllingTemp(isConnected)
    toggledTempStatus = libpointer('int32Ptr',0);
    if isConnected=="True"  
        for i=1:6
             calllib('attoDRYxyz64bit','AttoDRY_Interface_isControllingTemperature',toggledTempStatus);
             toggled=toggledTempStatus.Value;
             disp(toggled);
             if toggled ==1 
                 tempControl = "True";
                 break
             elseif toggled ==0
                 tempControl="False";
             end
             pause(0.8)
        end
    end
end