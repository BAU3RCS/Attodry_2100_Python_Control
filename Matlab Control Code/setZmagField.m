% Set Z-Magnetic Field         
function ZField = setZmagField(setZField)
    calllib('attoDRYxyz64bit','AttoDRY_Interface_setUserMagneticFieldZ',single(setZField/10000));
    ZField=setZField;
end      

