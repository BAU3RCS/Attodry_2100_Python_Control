function fieldControl = isControllingField(isConnected)
    toggledStatus = libpointer('int32Ptr',0);
    if isConnected=="True"  
        for i=1:6
             calllib('attoDRYxyz64bit','AttoDRY_Interface_isControllingField',toggledStatus);
             toggled=toggledStatus.Value;
             disp(toggled);
             if toggled ==1 
                 fieldControl = "True";
                 break
             elseif toggled ==0
                 fieldControl="False";
             end
             pause(0.8)
        end
    end
end