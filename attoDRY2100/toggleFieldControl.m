function toggleFieldControl(isConnected)
    if isConnected=="True"
        calllib('attoDRYxyz64bit','AttoDRY_Interface_toggleMagneticFieldControl');
    end
end      

