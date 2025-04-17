function toggleTempControl(isConnected)
    if isConnected=="True"
        calllib('attoDRYxyz64bit','AttoDRY_Interface_toggleFullTemperatureControl');
    end
end      

