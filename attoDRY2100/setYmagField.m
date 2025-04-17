% Set Y-Magnetic Field in Orested or Gauss         
function YField = setYmagField(setYField)
    calllib('attoDRYxyz64bit','AttoDRY_Interface_setUserMagneticField',single(setYField/10000));
    YField=setYField;
end        

