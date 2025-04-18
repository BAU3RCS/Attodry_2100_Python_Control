function isConnected = connectCryo(comPort)
    if ~libisloaded('attoDRYxyz64bit')
       disp("Loading Library.....");
       loadlibrary('attoDRYxyz64bit.dll','attoDRYxyz64bit.h');
    end
    calllib('attoDRYxyz64bit','AttoDRY_Interface_begin',uint16(1)); %Begin interface
    calllib('attoDRYxyz64bit','AttoDRY_Interface_Connect',comPort); %connect to cryostat through com3
    CryoConnection = libpointer('int32Ptr',0);%create a pointer
    for i=1:10
        calllib('attoDRYxyz64bit','AttoDRY_Interface_isDeviceConnected',CryoConnection);
        disp(CryoConnection.Value);
        if CryoConnection.Value==1
            break
        end
        pause(1)
    end
    if CryoConnection.Value==1
        isConnected="True";
    else
        isConnected="False";
    end 
end

