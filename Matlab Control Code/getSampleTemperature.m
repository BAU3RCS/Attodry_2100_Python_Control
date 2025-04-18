% Get Cryo sampleTemperature         
function [sampleTemp] = getSampleTemperature(isConnected)
        if isConnected=="True"
                SampleTemperature = libpointer('singlePtr',0);
                calllib('attoDRYxyz64bit','AttoDRY_Interface_getSampleTemperature',SampleTemperature);
                sampleTemp=SampleTemperature.Value;
                for i=1:4
                    calllib('attoDRYxyz64bit','AttoDRY_Interface_getSampleTemperature',SampleTemperature);
                    if SampleTemperature.Value>0
                        sampleTemp=SampleTemperature.Value;
                        break
                    end
                    pause(0.6)
                end
            else
                sampleTemp=-1;
        end
end


