% Set X-Magnetic Field         
function XField = setXmagField(setXField)
    calllib('attoDRYxyz64bit','AttoDRY_Interface_setUserMagneticFieldX',single(setXField/10000));
    XField=setXField;
end        

