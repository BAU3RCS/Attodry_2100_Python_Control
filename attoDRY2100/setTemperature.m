% Set X-Magnetic Field         
function setTemp = setTemperature(temp)
    temperature = temp;
    if temp>300
        temperature = 300;
    elseif temp<1.65
        temperature = 1.65;
    end
    calllib('attoDRYxyz64bit','AttoDRY_Interface_setUserTemperature',single(temperature));
    setTemp=temperature;
end        

