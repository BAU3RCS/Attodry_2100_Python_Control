function cryoStatus = disconnectCryo()
    cryoStatus="Disconnected";
    calllib('attoDRYxyz64bit','AttoDRY_Interface_Disconnect');
    calllib('attoDRYxyz64bit','AttoDRY_Interface_end');
    unloadlibrary attoDRYxyz64bit
    clear;
end

