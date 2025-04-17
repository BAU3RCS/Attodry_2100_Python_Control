%+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
%   Programmer : Sashi Nepal                                                       +
%   Email      : sashinpl@udel.edu                                                 +
%   Program    : Module to communicate with attoDRY cryostat 2100XL.               + 
%                The class below can connect to cryostat. Inquire the              +
%                sample temperature and magnet temperature.                        +
%                It can control the vector magnetic field.                         +
%+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

classdef cryoAttoDry

    properties
        cryoModel ="2100XL";
    end
        
    methods (Static)
%=================================================================================================================================  
        %This fuction connects the cryo to the specified comport. Make sure
        %you enter the comPort in single quote like 'COM3'
        function isConnected = connectCryo(comPort)
            if ~libisloaded('attoDRYxyz64bit')
               disp("Loading Library.....");
               [xx,yy] = loadlibrary('attoDRYxyz64bit.dll','attoDRYxyz64bit.h');
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
%=================================================================================================================================          
        % disconnect Cryo connection interface        
        function cryoStatus = disconnectCryo(isConnected)
            if isConnected=="True"
                cryoStatus=calllib('attoDRYxyz64bit','AttoDRY_Interface_Disconnect');
                calllib('attoDRYxyz64bit','AttoDRY_Interface_end');
                fieldControl=isControllingField(isConnected);
                if fieldControl=="True"
                    toggleFieldControl(isConnected);                  
                end
                unloadlibrary attoDRYxyz64bit
            else
                cryoStatus="Already disconnected";
                
            end
        end
%=================================================================================================================================          
        % unload library
        function cryoStatus = unloadCryoLib(isConnected)
             if isConnected=="True"
                unloadlibrary attoDRYxyz64bit
            else
                cryoStatus="Already disconnected";
            end
        end
%=================================================================================================================================        
        % Get Cryo magnet temp         
        function magnetTemp = getMagnetTemp(isConnected)
            if isConnected=="True"
                MagnetTemperature = libpointer('singlePtr',0);
                for i=1:4
                    calllib('attoDRYxyz64bit','AttoDRY_Interface_get4KStageTemperature',MagnetTemperature);
                    if MagnetTemperature.Value>0
                        magnetTemp=MagnetTemperature.Value;
                        break
                    end
                    pause(0.6)
                end
            else
                magnetTemp=-1;
            end

        end
%=================================================================================================================================          
        % Get Cryo sample temp         
        function sampleTemp = getSampleTemp(isConnected)
            [sampleTemp]=getSampleTemperature(isConnected);
        end %getSampleTemp end
%=================================================================================================================================  
        % Set user temp        
        function userTemp = setUserTemp(isConnected,temp)          
            if isConnected=="True"
                tempControl=isControllingTemp(isConnected);
                if tempControl=="False"
                    toggleTempControl(isConnected);
                    tempControl=isControllingTemp(isConnected);                   
                end
                if tempControl=="True"
                    setTemperature(temp)
                end
                disp("isCryoControllingTemp =" + tempControl);
                disp(' ');
                targetTemp = temp;
                [initTemp]=getSampleTemperature(isConnected);
                targetTempReached="False";
                reverseStr = '';
                printtext = sprintf('Target Temp = %4.3f Kelvin \n',targetTemp);
                fprintf(['',printtext]);
                count =0;
                disp(' ');
                while targetTempReached=="False"
                    [currentTemp]=getSampleTemperature(isConnected);
                    if abs(initTemp - targetTemp) <=0.1 || abs(currentTemp - targetTemp) <=0.1
                        progress1 = 100;
                    else
                        progress1 = (abs(currentTemp-initTemp)/abs(initTemp-targetTemp))*100;
                    end
                    msg = sprintf('Ramping Temperature Progress: %3.1f/100 | Current Sample Temperature = %4.3f Kelvin \n', progress1,currentTemp); %Don't forget this semicolon
                    fprintf([reverseStr, msg]);
                    reverseStr = repmat(sprintf('\b'), 1, length(msg));
                    pause(20);
                    if progress1>= 99.0
                        if abs(targetTemp-currentTemp)<=0.1
                            count = count+1;
                            if count==2
                                targetTempReached="True";
                            end 
                        end
                    end
                    pause(2);
                end
                userTemp = currentTemp;
                disp(' ');
            end
        end%setUserTemp end
%=================================================================================================================================  
        % Z-Field is Gauss or Oerested Control        
        function ZField = setZField(isConnected,setField)
            if setField>50000 || setField<-50000
                error("Magnitude of Z-field should be in range -50kG to +50kG. Please adjust the value of R to the suggest range.");
            end            
            if isConnected=="True" && setField <=50000 && setField>=-50000
                fieldControl=isControllingField(isConnected);
                if fieldControl=="False"
                    toggleFieldControl(isConnected);
                    fieldControl=isControllingField(isConnected);                   
                end
                if fieldControl=="True"
                    setZmagField(setField)
                end
                disp("isCryoControllingField =" + fieldControl);
                disp(' ');
                ZField=setField;
            end
        end %setZField end
%=================================================================================================================================  
        % Y-Field is Gauss or Oerested Control        
        function YField = setYField(isConnected,setField)
            if setField>10000 || setField<-10000
                error("Magnitude of Y-field should be in range -10kG to +10kG. Please adjust the value of R to the suggest range.");
            end            
            if isConnected=="True" && setField <=10000 && setField>=-10000
                fieldControl=isControllingField(isConnected);
                if fieldControl=="False"
                    toggleFieldControl(isConnected);
                    fieldControl=isControllingField(isConnected);                   
                end
                if fieldControl=="True"
                    setYmagField(setField)
                end
                disp("isCryoControllingField =" + fieldControl);
                YField=setField;
                disp(' ');
            end
        end %setYField end
%=================================================================================================================================  
        % X-Field is Gauss or Oerested Control        
        function XField = setXField(isConnected,setField)
            if setField>10000 || setField<-10000
                error("Magnitude of X-field should be in range -10kG to +10kG. Please adjust the value of R to the suggest range.");
            end
            if isConnected=="True" && setField <=10000 && setField>=-10000
                fieldControl=isControllingField(isConnected);
                if fieldControl=="False"
                    toggleFieldControl(isConnected);
                    fieldControl=isControllingField(isConnected);                   
                end
                if fieldControl=="True"
                    setXmagField(setField)
                end
                disp("isCryoControllingField =" + fieldControl);
                disp(' ');
                XField=setField;
            end
        end %setXField end
        
%=================================================================================================================================  
        % Vector Field in Gauss or Oerested Control, supply R in Oerested or Gauss. Theta and Phi in degrees        
        function [targetR,targetX,targetY,targetZ] = setVectorField(isConnected,R,theta,phi)
            X = R*sin(deg2rad(theta))*cos(deg2rad(phi));
            Y = R*sin(deg2rad(theta))*sin(deg2rad(phi));
            Z = R*cos(deg2rad(theta));
            targetR = R;
            targetX = X;
            targetY = Y;
            targetZ = Z;
            if R>10000 || R<-10000
                error("Magnitude of vector field should be in range -10kG to +10kG. Please adjust the value of R to the suggest range.");
            end
            if isConnected=="True" && R <=10000 && R>=-10000
                fieldControl=isControllingField(isConnected);
                if fieldControl=="False"
                    toggleFieldControl(isConnected);
                    fieldControl=isControllingField(isConnected);                   
                end
                if fieldControl=="True"
                    setXmagField(X)
                    setYmagField(Y)
                    setZmagField(Z)
                end
                disp("isCryoControllingField =" + fieldControl);
                disp(' ');
                
                %===============================Monitoring the Field =====
                [initR,initX,initY,initZ]=getMagField(isConnected);
                targetFieldReached="False";
                reverseStr = '';
                printtext = sprintf('Target R = %4.3f | kG Target X-Field = %4.3f kG | Target Y-Field = %4.3f kG | Target Z-Field = %4.3f kG\n',targetR/1000,targetX/1000,targetY/1000,targetZ/1000);
                fprintf(['',printtext]);
                count =0;
                disp(' ');
                while targetFieldReached=="False"
                    [currentR, X,Y,Z]=getMagField(isConnected);
                    if abs(initX - targetX) <=4 || abs(X - targetX) <=4
                        progress1 = 100;
                    else
                        progress1 = (abs(X-initX)/abs(initX-targetX))*100;
                    end
                    if abs(initY - targetY) <=4 || abs(Y-targetY)<=4
                        progress2 = 100;
                    else
                        progress2 = (abs(Y-initY)/abs(initY-targetY))*100;
                    end
                    if abs(initZ - targetZ) <=4 || abs(Z-targetZ)<=4
                        progress3 = 100;
                    else
                        progress3 = (abs(Z-initZ)/abs(initZ-targetZ))*100;
                    end
                    msg = sprintf('Ramping X Progress: %3.1f/100 | Ramping Y Progress: %3.1f/100 | Ramping Z Progress: %3.1f/100 |\nR = %4.3f kG | X = %4.3f kG | Y = %4.3f kG | Z = %4.3f kG \n', progress1,progress2 ,progress3 ,currentR/1000,X/1000,Y/1000,Z/1000); %Don't forget this semicolon
                    fprintf([reverseStr, msg]);
                    reverseStr = repmat(sprintf('\b'), 1, length(msg));
                    pause(0.05);
                    if progress1>= 90.0 && progress2 >= 90.0 && progress3 >= 90.0
                        if abs(targetX-X)<=4 && abs(targetY-Y)<=4 && abs(targetZ-Z)<=4
                            count = count+1;
                            if count==4
                                targetFieldReached="True";
                            end 
                        end
                    end
                    pause(1)
                end
                disp(' ');
            end
        end %setVectorField end
        
 %=================================================================================================================================           
 
 % Monitor vectorField Ramping     
        function monitorVectorField(isConnected,targetR,targetX,targetY, targetZ)
            if isConnected == "True"
                [initR,initX,initY,initZ]=getMagField(isConnected);
                targetFieldReached="False";
                reverseStr = '';
                printtext = sprintf('Target R = %4.3f | kG Target X-Field = %4.3f kG | Target Y-Field = %4.3f kG | Target Z-Field = %4.3f kG\n',targetR/1000,targetX/1000,targetY/1000,targetZ/1000);
                fprintf(['',printtext]);
                count =0;
                disp(' ');
                while targetFieldReached=="False"
                    [currentR, X,Y,Z]=getMagField(isConnected);
                    if abs(initX - targetX) <=4 || abs(X - targetX) <=4
                        progress1 = 100;
                    else
                        progress1 = (abs(X-initX)/abs(initX-targetX))*100;
                    end
                    if abs(initY - targetY) <=4 || abs(Y-targetY)<=4
                        progress2 = 100;
                    else
                        progress2 = (abs(Y-initY)/abs(initY-targetY))*100;
                    end
                    if abs(initZ - targetZ) <=4 || abs(Z-targetZ)<=4
                        progress3 = 100;
                    else
                        progress3 = (abs(Z-initZ)/abs(initZ-targetZ))*100;
                    end
                    msg = sprintf('Ramping X Progress: %3.1f/100 | Ramping Y Progress: %3.1f/100 | Ramping Z Progress: %3.1f/100 |\nR = %4.3f kG | X = %4.3f kG | Y = %4.3f kG | Z = %4.3f kG \n', progress1,progress2 ,progress3 ,currentR/1000,X/1000,Y/1000,Z/1000); %Don't forget this semicolon
                    fprintf([reverseStr, msg]);
                    reverseStr = repmat(sprintf('\b'), 1, length(msg));
                    pause(0.05);
                    if progress1>= 90.0 && progress2 >= 90.0 && progress3 >= 90.0
                        if abs(targetX-X)<=4 && abs(targetY-Y)<=4 && abs(targetZ-Z)<=4
                            count = count+1;
                            if count==4
                                targetFieldReached="True";
                            end 
                        end
                    end
                end
                disp(' ');
            end
        end %monitorVectorField       
%=================================================================================================================================  
        % Monitor XField Ramping     
        function monitorXField(isConnected,targetX)
            initX=getXMagField(isConnected);
            targetFieldReached="False";
            reverseStr = '';
            count =0;
            while targetFieldReached=="False"
                currentField = getXMagField(isConnected);
                if abs(initX - targetX) <=4 || abs(currentField - targetX) <=4
                    progress = 100;
                else
                    progress = (abs(currentField-initX)/abs(initX-targetX))*100;
                end      
                msg = sprintf('Ramping X-Field to %4.3f kG | Progress: %3.1f/100 | X-Field = %4.3f kG',targetX/1000, progress,currentField/1000); %Don't forget this semicolon
                fprintf([reverseStr, msg]);
                reverseStr = repmat(sprintf('\b'), 1, length(msg));
                pause(0.05);
                if progress>90.0
                    if abs(currentField-targetX)<=4
                        count = count+1;
                        if count==4
                            targetFieldReached="True";
                        end 
                    end
                end
            end
            disp(' ');
        end %monitorXField       
%=================================================================================================================================  
        % Monitor YField Ramping     
        function monitorYField(isConnected,targetY)
            initY=getYMagField(isConnected);
            targetFieldReached="False";
            reverseStr = '';
            count =0;
            while targetFieldReached=="False"
                currentField = getYMagField(isConnected);
                if abs(initY - targetY) <=4 || abs(currentField - targetY) <=4
                    progress = 100;
                else
                    progress = (abs(currentField-initY)/abs(initY-targetY))*100;
                end      
                msg = sprintf('Ramping Y-Field to %4.3f kG | Progress: %3.1f/100 | Y-Field = %4.3f kG',targetY/1000, progress,currentField/1000); %Don't forget this semicolon
                fprintf([reverseStr, msg]);
                reverseStr = repmat(sprintf('\b'), 1, length(msg));
                pause(0.05);
                if progress>90.0
                    if abs(currentField-targetY)<=4
                        count = count+1;
                        if count==4
                            targetFieldReached="True";
                        end 
                    end
                end
            end
            disp(' ');
        end %monitorYField    
%=================================================================================================================================  
        % Monitor ZField Ramping     
        function monitorZField(isConnected,targetZ)
            initZ=getZMagField(isConnected);
            targetFieldReached="False";
            reverseStr = '';
            count =0;
            while targetFieldReached=="False"
                currentField = getZMagField(isConnected);
                if abs(initZ - targetZ) <=4 || abs(currentField - targetZ) <=4
                    progress = 100;
                else
                    progress = (abs(currentField-initZ)/abs(initZ-targetZ))*100;
                end      
                msg = sprintf('Ramping Z-Field to %4.3f kG | Progress: %3.1f/100 | Z-Field = %4.3f kG',targetZ/1000, progress,currentField/1000); %Don't forget this semicolon
                fprintf([reverseStr, msg]);
                reverseStr = repmat(sprintf('\b'), 1, length(msg));
                pause(0.05);
                if progress>90.0
                    if abs(currentField-targetZ)<=4
                        count = count+1;
                        if count==4
                            targetFieldReached="True";
                        end 
                    end
                end
            end
            disp(' ');
        end %monitorZField  
        
%=================================================================================================================================  
        % checkSafe    
        function checkSafe(isConnected,targetField)
            if isConnected =="True" && targetField<10000
                [x_,y_,z]=getMagField(isConnected);
                if z > 10000
                    printtext = sprintf('Current Field is %4.3f kG. To use vector field it is safe to use Z-Field < 10 kG.\n',targetX/1000,targetY/1000,targetZ/1000);
                    fprintf(['',printtext]);
                    fieldControl=isControllingField(isConnected);
                    if fieldControl=="False"
                        toggleFieldControl(isConnected);
                        fieldControl=isControllingField(isConnected);                   
                    end
                    if fieldControl=="True"
                        setZmagField(targetField)
                    end
                    initField=getZMagField(isConnected);
                    targetFieldReached="False";
                    reverseStr = '';
                    count =0;
                    while targetFieldReached=="False"
                        currentField = getZMagField(isConnected);
                        progress = (abs(currentField-initField)/abs(initField-targetField))*100;
                        msg = sprintf('Ramping Z-Field Progress: %3.1f | Z-Field = %4.3f kG', progress,currentField/1000); %Don't forget this semicolon
                        fprintf([reverseStr, msg]);
                        reverseStr = repmat(sprintf('\b'), 1, length(msg));
                        pause(0.05);
                        if abs(currentField-targetField)<=4
                            count = count+1;
                            if count==4
                                targetFieldReached="True";
                            end 
                        end
                    end
                    disp(' ');
                end
            end
       end %checkSafe 
%=================================================================================================================================       
    end % method end
    
end % class end

