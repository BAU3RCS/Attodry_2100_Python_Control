import os
from ctypes import c_int32, c_float, c_char_p, c_int, c_uint8, POINTER
from enum import IntEnum

loc = r"..\64 bit\attoDRYxyz64bit.dll"

# Helper type aliases
IntPointer = POINTER(c_int)
FloatPointer = POINTER(c_float)

from enum import IntEnum

class AttoDevice(IntEnum):
    ATTODRY2100 = 1

class TimeDelay(IntEnum):
    _1SECOND     = 0
    _5SECONDS    = 1
    _30SECONDS   = 2
    _1MINUTE     = 3
    _5MINUTES    = 4

# Define ctypes wrappers for the additional AttoDRY C API
class AttoDRYInterface:
    """
    Python ctypes interface for the AttoDRY cryostat control system.
    Wraps the AttoDRY C API for device communication and control.
    """

    def __init__(self, dll_path=loc: str):
        """
        Load the AttoDRY DLL from the specified path.

        Args:
            dll_path (str): Path to the AttoDRY shared library (.dll or .so).
        """
        self.lib = ctypes.CDLL(dll_path)

    def _check_return(self, ret_code):
        """
        Internal helper to raise an exception if the C function returned an error.

        Args:
            ret_code (int): Return code from a C function.

        Raises:
            RuntimeError: If the return code is non-zero.
        """
        if ret_code != 0:
            raise RuntimeError(f"C function returned error code: {ret_code}")

    def Begin(self, device=ATTODRY2100: int) -> None:
        """
        Starts the server that communicates with the attoDRY and loads the software 
        for the device specified by <B> Device </B>. This VI needs to be run before 
        commands can be sent or received. The <B>UI Queue</B> is an event queue for 
        updating the GUI. It should not be used when calling the function from a DLL.

        Starts the communication server for a specified device.

        Args:
            device (int): Device identifier.
        """
        self._check_return(self.lib.AttoDRY_Interface_begin(c_uint16(device)))

    def Connect(self, com_port="COM3": str) -> None:
        """
        Connects to the attoDRY using the specified COM Port
        Establishes connection with the AttoDRY over the specified COM port.

        Args:
            com_port (str): Name of the COM port (e.g., 'COM3').
        """
        self._check_return(self.lib.AttoDRY_Interface_Connect(com_port.encode('utf-8')))

    def Disconnect(self) -> None:
        """
        Terminates the connection with the AttoDRY device.

        Disconnects from the attoDRY, if already connected. This should be run 
        before the <B>end.vi</B>
        """
        self._check_return(self.lib.AttoDRY_Interface_Disconnect())

    def Cancel(self) -> None:
    """
    Sends a 'Cancel' command to the attoDRY.
    Use this method to cancel an ongoing action or respond negatively to a pop-up prompt.
    """
    self._check_return(self.lib.AttoDRY_Interface_Cancel())

    def Confirm(self) -> None:
        """
        Sends a 'Confirm' command to the attoDRY.
        Use this method to confirm an action or respond positively to a pop-up prompt.
        """
        self._check_return(self.lib.AttoDRY_Interface_Confirm())


    def End(self) -> None:
        """
        Stops the server that is communicating with the attoDRY. The 
        <B>Disconnect.vi</B> should be run before this. This VI should be run 
        before closing your program.

        Stops the server. Device must be disconnected first.
        """
        self._check_return(self.lib.AttoDRY_Interface_end())

#####################################
#STOPPED HERE
#####################################

    def IsConnected(self) -> bool:
        """
        Checks whether the AttoDRY is currently connected.

        Returns:
            bool: True if connected, False otherwise.
        """
        status = c_int()
        self._check_return(self.lib.AttoDRY_Interface_isDeviceConnected(ctypes.byref(status)))
        return bool(status.value)

    def IsInitialised(self) -> bool:
        """
        Checks if the AttoDRY device is initialised and ready.

        Returns:
            bool: True if initialised, False otherwise.
        """
        status = c_int()
        self._check_return(self.lib.AttoDRY_Interface_isDeviceInitialised(ctypes.byref(status)))
        return bool(status.value)

    def DownloadSampleTempSensorCalibrationCurve(self, save_path: str) -> None:
    """
    Downloads the Sample Temperature Sensor Calibration Curve.

    This method initiates the download of the sample temperature sensor calibration curve 
    from the attoDRY device and saves it to the specified file path.

    Args:
        save_path (str): The full path (including filename) where the calibration curve 
                         will be saved on the local machine.
    """
    self._check_return(
        self.lib.AttoDRY_Interface_downloadSampleTemperatureSensorCalibrationCurve(save_path.encode('utf-8'))
    )

    def DownloadTempSensorCalibrationCurve(self, user_curve_number: int, path: str) -> None:
        """
        Downloads a user-selected Temperature Sensor Calibration Curve.

        This method initiates the download of a temperature sensor calibration curve from the 
        temperature monitor of the attoDRY device, identified by the user curve number, and 
        saves it to the specified file path.

        Args:
            user_curve_number (int): The index of the user calibration curve to download.
            path (str): The full path (including filename) where the calibration curve 
                        will be saved on the local machine.
        """
        self._check_return(
            self.lib.AttoDRY_Interface_downloadTemperatureSensorCalibrationCurve(
                c_uint8(user_curve_number), path.encode('utf-8')
            )
        )


    def ToggleExchangeHeaterControl(self) -> None:
        """
        Toggles control over the exchange/VTI heater.

        This command only toggles the exchange/vti temperature controller. If a 
        sample temperature sensor is connected, this will be controlled, otherwise 
        the temperature of the exchange tube will be used
        """
        self._check_return(self.lib.AttoDRY_Interface_toggleExchangeHeaterControl())

    def IsExchangeHeaterOn(self) -> bool:
        """
        Checks if the exchange heater is currently on.

        Checks to see if the exchange/vti heater is on. 'On' is defined as PID 
        control is active or a constant heater power is set.

        Returns:
            bool: True if on, False if off.
        """
        status = c_int()
        self._check_return(self.lib.AttoDRY_Interface_isExchangeHeaterOn(ctypes.byref(status)))
        return bool(status.value)

    def ToggleCryostatInValve(self):
        """
        Toggles the Cryostat In valve. If it is closed, it will 
        open and if it is open, it will close. 

        Toggles the Cryostat In valve.
        """
        self._check_return(self.lib.AttoDRY_Interface_toggleCryostatInValve())

    def ToggleCryostatOutValve(self):
        """
        Toggles the Cryostat Out valve. If it is closed, it will 
        open and if it is open, it will close.

        Toggles the Cryostat Out valve.
        """
        self._check_return(self.lib.AttoDRY_Interface_toggleCryostatOutValve())

    def ToggleDumpInValve(self):
        """
        Toggles the inner volume valve. If it is closed, it will 
        open and if it is open, it will close.

        Toggles the Dump In valve.
        """
        self._check_return(self.lib.AttoDRY_Interface_toggleDumpInValve())

    def ToggleDumpOutValve(self):
        """
        Toggles the outer volume valve. If it is closed, it will 
        open and if it is open, it will close. 

        Toggles the Dump Out valve.
        """
        self._check_return(self.lib.AttoDRY_Interface_toggleDumpOutValve())

    def GetCryostatInValveStatus(self) -> int:
        """
        Retrieves the status of the Cryostat In valve.
        Gets the current status of the Cryostat In valve.

        Returns:
            int: Valve status (0 or 1).
        """
        status = c_int()
        self._check_return(self.lib.AttoDRY_Interface_getCryostatInValve(ctypes.byref(status)))
        return status.value

    def GetCryostatOutValveStatus(self) -> int:
        """
        Gets the current status of the Cryostat Out valve.

        Returns Cryostat Out valve status (0 = closed, 1 = open).
        """
        status = c_int()
        self._check_return(self.lib.AttoDRY_Interface_getCryostatOutValve(ctypes.byref(status)))
        return status.value

    def GetDumpInValveStatus(self) -> int:
        """
        Gets the current status of the Dump In volume valve

        Returns Dump In valve status (0 = closed, 1 = open).
        """
        status = c_int()
        self._check_return(self.lib.AttoDRY_Interface_getDumpInValve(ctypes.byref(status)))
        return status.value

    def GetDumpOutValveStatus(self) -> int:
        """
        Gets the current status of the outer volume valve.
        
        Returns Dump Out valve status (0 = closed, 1 = open).
        """
        status = c_int()
        self._check_return(self.lib.AttoDRY_Interface_getDumpOutValve(ctypes.byref(status)))
        return status.value

    def GetCryostatInPressure(self) -> float:
        """
        Reads the current Cryostat In pressure.

        Gets the pressure at the Cryostat Inlet

        Returns:
            float: Pressure in mbar.
        """
        pressure = c_float()
        self._check_return(self.lib.AttoDRY_Interface_getCryostatInPressure(ctypes.byref(pressure)))
        return pressure.value

    def GetCryostatOutPressure(self) -> float:
        """
        Gets the Cryostat Outlet pressure
        Reads the current Cryostat Out pressure (in mbar).
        """
        pressure = c_float()
        self._check_return(self.lib.AttoDRY_Interface_getCryostatOutPressure(ctypes.byref(pressure)))
        return pressure.value

    def GetDumpPressure(self) -> float:
        """
        Gets the pressure at the Dump.
        Reads the current Dump pressure (in mbar).
        """
        pressure = c_float()
        self._check_return(self.lib.AttoDRY_Interface_getDumpPressure(ctypes.byref(pressure)))
        return pressure.value

    def GetReservoirHeaterPower(self) -> float:
        """
        Gets the current power, in Watts, being produced by the reservoir heater.

        Returns:
            float: The current power output of the reservoir heater in Watts.
        """
        val = c_float()
        self._check_return(self.lib.AttoDRY_Interface_getReservoirHeaterPower(ctypes.byref(val)))
        return val.value


    def GetReservoirTemperature(self) -> float:
        """
        Gets the current temperature of the Helium Reservoir, in Kelvin
        Reads the reservoir temperature in Kelvin.
        """
        temp = c_float()
        self._check_return(self.lib.AttoDRY_Interface_getReservoirTemperature(ctypes.byref(temp)))
        return temp.value

    def Get4KStageTemperature(self) -> float:
        """
        Reads the 4K stage temperature in Kelvin.
        """
        temp = c_float()
        self._check_return(self.lib.AttoDRY_Interface_get4KStageTemperature(ctypes.byref(temp)))
        return temp.value

    def GetVtiTemperature(self) -> float:
        """
        Reads the VTI (Variable Temperature Insert) temperature in Kelvin.
        """
        temp = c_float()
        self._check_return(self.lib.AttoDRY_Interface_getVtiTemperature(ctypes.byref(temp)))
        return temp.value

    def GetSampleTemperature(self) -> float:
        """
        Reads the sample temperature in Kelvin.
        """
        temp = c_float()
        self._check_return(self.lib.AttoDRY_Interface_getSampleTemperature(ctypes.byref(temp)))
        return temp.value

    def GetUserTemperature(self) -> float:
        """
        Reads the user-defined temperature sensor value (in Kelvin).
        """
        temp = c_float()
        self._check_return(self.lib.AttoDRY_Interface_getUserTemperature(ctypes.byref(temp)))
        return temp.value

    def GetTemperatureSetpoint(self) -> float:
        """
        Gets the current temperature setpoint for the sample heater.

        Returns:
            float: Setpoint temperature in Kelvin.
        """
        temp = c_float()
        self._check_return(self.lib.AttoDRY_Interface_getTemperatureSetpoint(ctypes.byref(temp)))
        return temp.value

    def GetTemperatureSetpointLimit(self) -> float:
        """
        Gets the maximum allowable temperature setpoint.

        Returns:
            float: Temperature setpoint limit in Kelvin.
        """
        temp = c_float()
        self._check_return(self.lib.AttoDRY_Interface_getTemperatureSetpointLimit(ctypes.byref(temp)))
        return temp.value

    def SetTemperatureSetpoint(self, temp: float) -> None:
        """
        Sets the desired sample temperature setpoint.

        Args:
            temp (float): Temperature setpoint in Kelvin.
        """
        self._check_return(self.lib.AttoDRY_Interface_setTemperatureSetpoint(c_float(temp)))

    def GetTemperatureRampRate(self) -> float:
        """
        Gets the current temperature ramp rate.

        Returns:
            float: Ramp rate in K/min.
        """
        rate = c_float()
        self._check_return(self.lib.AttoDRY_Interface_getTemperatureRampRate(ctypes.byref(rate)))
        return rate.value

    def SetTemperatureRampRate(self, rate: float) -> None:
        """
        Sets the temperature ramp rate.

        Args:
            rate (float): Ramp rate in K/min.
        """
        self._check_return(self.lib.AttoDRY_Interface_setTemperatureRampRate(c_float(rate)))

    def GetHeaterOutput(self) -> float:
        """
        Gets the current heater output percentage.

        Returns:
            float: Heater output (0–100%).
        """
        output = c_float()
        self._check_return(self.lib.AttoDRY_Interface_getHeaterOutput(ctypes.byref(output)))
        return output.value

    def GetHeaterRange(self) -> int:
        """
        Gets the current heater range setting.

        Returns:
            int: Heater range (e.g., 0 = Off, 1 = Low, etc.).
        """
        range_val = c_int()
        self._check_return(self.lib.AttoDRY_Interface_getHeaterRange(ctypes.byref(range_val)))
        return range_val.value

    def SetHeaterRange(self, range_val: int) -> None:
        """
        Sets the heater range.

        Args:
            range_val (int): Range setting (e.g., 0 = Off, 1 = Low, etc.).
        """
        self._check_return(self.lib.AttoDRY_Interface_setHeaterRange(c_int(range_val)))

    def IsHeaterOn(self) -> bool:
        """
        Checks if the heater is currently on.

        Returns:
            bool: True if heater is on, False otherwise.
        """
        status = c_int()
        self._check_return(self.lib.AttoDRY_Interface_isHeaterOn(ctypes.byref(status)))
        return bool(status.value)

    def GetMagnetField(self) -> float:
        """
        Gets the current magnetic field strength.

        Returns:
            float: Magnetic field in Tesla.
        """
        field = c_float()
        self._check_return(self.lib.AttoDRY_Interface_getMagnetField(ctypes.byref(field)))
        return field.value

    def GetMagnetSetpoint(self) -> float:
        """
        Gets the magnetic field setpoint.

        Returns:
            float: Field setpoint in Tesla.
        """
        setpoint = c_float()
        self._check_return(self.lib.AttoDRY_Interface_getMagnetSetpoint(ctypes.byref(setpoint)))
        return setpoint.value

    def SetMagnetSetpoint(self, setpoint: float) -> None:
        """
        Sets the magnetic field setpoint.

        Args:
            setpoint (float): Desired field in Tesla.
        """
        self._check_return(self.lib.AttoDRY_Interface_setMagnetSetpoint(c_float(setpoint)))

    def GetMagnetSweepRate(self) -> float:
        """
        Gets the current sweep rate for the magnet.

        Returns:
            float: Sweep rate in T/min.
        """
        rate = c_float()
        self._check_return(self.lib.AttoDRY_Interface_getMagnetSweepRate(ctypes.byref(rate)))
        return rate.value

    def SetMagnetSweepRate(self, rate: float) -> None:
        """
        Sets the magnetic field sweep rate.

        Args:
            rate (float): Sweep rate in T/min.
        """
        self._check_return(self.lib.AttoDRY_Interface_setMagnetSweepRate(c_float(rate)))

    def MagnetSweep(self) -> None:
        """
        Starts sweeping the magnetic field to the setpoint.
        """
        self._check_return(self.lib.AttoDRY_Interface_magnetSweep())

    def MagnetSweepCancel(self) -> None:
        """
        Cancels the current magnetic field sweep.
        """
        self._check_return(self.lib.AttoDRY_Interface_magnetSweepCancel())

    def GetMagnetStatus(self) -> int:
        """
        Gets the status of the magnet.

        Returns:
            int: Status code representing current magnet operation.
        """
        status = c_int()
        self._check_return(self.lib.AttoDRY_Interface_getMagnetStatus(ctypes.byref(status)))
        return status.value

    def GetErrorCount(self) -> int:
        """
        Gets the number of unread errors.

        Returns:
            int: Number of stored errors.
        """
        count = c_int()
        self._check_return(self.lib.AttoDRY_Interface_getErrorCount(ctypes.byref(count)))
        return count.value

    def GetError(self) -> str:
        """
        Retrieves and clears the oldest error message from the buffer.

        Returns:
            str: Error message.
        """
        buffer = ctypes.create_string_buffer(256)
        self._check_return(self.lib.AttoDRY_Interface_getError(buffer, c_int(256)))
        return buffer.value.decode('utf-8')

    def GetWarningCount(self) -> int:
        """
        Gets the number of unread warnings.

        Returns:
            int: Number of stored warnings.
        """
        count = c_int()
        self._check_return(self.lib.AttoDRY_Interface_getWarningCount(ctypes.byref(count)))
        return count.value

    def GetWarning(self) -> str:
        """
        Retrieves and clears the oldest warning message from the buffer.

        Returns:
            str: Warning message.
        """
        buffer = ctypes.create_string_buffer(256)
        self._check_return(self.lib.AttoDRY_Interface_getWarning(buffer, c_int(256)))
        return buffer.value.decode('utf-8')

    def GetSystemStatus(self) -> int:
        """
        Gets the system status code.

        Returns:
            int: Bitmask of system status flags.
        """
        status = c_int()
        self._check_return(self.lib.AttoDRY_Interface_getSystemStatus(ctypes.byref(status)))
        return status.value

    def is_persistent_mode_set(self) -> bool:
        """
        Returns 1 if the magnet is in persistent mode.
        """
        status = c_int()
        self._dll.AttoDRY_Interface_isPersistentModeSet(ctypes.byref(status))
        return bool(status.value)

    def is_pumping(self) -> bool:
        """
        Returns 1 if the system is currently pumping.
        """
        status = c_int()
        self._dll.AttoDRY_Interface_isPumping(ctypes.byref(status))
        return bool(status.value)

    def is_sample_exchange_in_progress(self) -> bool:
        """
        Returns 1 if a sample exchange process is currently active.
        """
        status = c_int()
        self._dll.AttoDRY_Interface_isSampleExchangeInProgress(ctypes.byref(status))
        return bool(status.value)

    def is_sample_heater_on(self) -> bool:
        """
        Returns 1 if the sample heater is active.
        """
        status = c_int()
        self._dll.AttoDRY_Interface_isSampleHeaterOn(ctypes.byref(status))
        return bool(status.value)

    def is_sample_ready_to_exchange(self) -> bool:
        """
        Returns 1 if the sample is ready to be exchanged.
        """
        status = c_int()
        self._dll.AttoDRY_Interface_isSampleReadyToExchange(ctypes.byref(status))
        return bool(status.value)

    def is_system_running(self) -> bool:
        """
        Returns 1 if the system is currently running.
        """
        status = c_int()
        self._dll.AttoDRY_Interface_isSystemRunning(ctypes.byref(status))
        return bool(status.value)

    def is_zeroing_field(self) -> bool:
        """
        Returns 1 if the system is currently sweeping the field to 0.
        """
        status = c_int()
        self._dll.AttoDRY_Interface_isZeroingField(ctypes.byref(status))
        return bool(status.value)

    def lower_error(self):
        """
        Lowers the current error condition, if any.
        """
        self._dll.AttoDRY_Interface_lowerError()

    def query_sample_heater_maximum_power(self):
        """
        Query the sample heater's maximum power (in W).
        """
        self._dll.AttoDRY_Interface_querySampleHeaterMaximumPower()

    def query_sample_heater_resistance(self):
        """
        Query the resistance of the sample heater (in Ohms).
        """
        self._dll.AttoDRY_Interface_querySampleHeaterResistance()

    def query_sample_heater_wire_resistance(self):
        """
        Query the resistance of the sample heater wiring (in Ohms).
        """
        self._dll.AttoDRY_Interface_querySampleHeaterWireResistance()

    def set_derivative_gain(self, value: float):
        """
        Set the derivative gain for the temperature controller.
        """
        self._dll.AttoDRY_Interface_setDerivativeGain(c_float(value))

    def set_integral_gain(self, value: float):
        """
        Set the integral gain for the temperature controller.
        """
        self._dll.AttoDRY_Interface_setIntegralGain(c_float(value))

    def set_proportional_gain(self, value: float):
        """
        Set the proportional gain for the temperature controller.
        """
        self._dll.AttoDRY_Interface_setProportionalGain(c_float(value))

    def set_sample_heater_maximum_power(self, power_watts: float):
        """
        Set the maximum power for the sample heater (in W).
        """
        self._dll.AttoDRY_Interface_setSampleHeaterMaximumPower(c_float(power_watts))

    def set_sample_heater_wire_resistance(self, resistance_ohms: float):
        """
        Set the sample heater wire resistance (in Ohms).
        """
        self._dll.AttoDRY_Interface_setSampleHeaterWireResistance(c_float(resistance_ohms))

    def set_sample_heater_power(self, power_watts: float):
        """
        Set the power for the sample heater (in W).
        """
        self._dll.AttoDRY_Interface_setSampleHeaterPower(c_float(power_watts))

    def set_sample_heater_resistance(self, resistance_ohms: float):
        """
        Set the resistance for the sample heater (in Ohms).
        """
        self._dll.AttoDRY_Interface_setSampleHeaterResistance(c_float(resistance_ohms))

    def set_user_magnetic_field(self, field_tesla: float):
        """
        Set the magnetic field (in T) in both X and Z directions.
        """
        self._dll.AttoDRY_Interface_setUserMagneticField(c_float(field_tesla))

    def set_user_temperature(self, temperature_k: float):
        """
        Set the temperature setpoint (in K).
        """
        self._dll.AttoDRY_Interface_setUserTemperature(c_float(temperature_k))

    def start_logging(self, path: str, time_selection: int, append: int):
        """
        Start logging to the given file path.
        """
        path_bytes = path.encode('utf-8')
        self._dll.AttoDRY_Interface_startLogging(c_char_p(path_bytes), c_int(time_selection), c_int(append))

    def start_sample_exchange(self):
        """
        Start the sample exchange process.
        """
        self._dll.AttoDRY_Interface_startSampleExchange()

    def stop_logging(self):
        """
        Stop the current logging session.
        """
        self._dll.AttoDRY_Interface_stopLogging()

    def sweep_field_to_zero(self):
        """
        Sweep the magnetic field to 0 T.
        """
        self._dll.AttoDRY_Interface_sweepFieldToZero()

    def toggle_full_temperature_control(self):
        """
        Toggle full system temperature control.
        """
        self._dll.AttoDRY_Interface_toggleFullTemperatureControl()

    def toggle_magnetic_field_control(self):
        """
        Toggle magnetic field control.
        """
        self._dll.AttoDRY_Interface_toggleMagneticFieldControl()

    def toggle_persistent_mode(self):
        """
        Toggle persistent mode for the magnet.
        """
        self._dll.AttoDRY_Interface_togglePersistentMode()

    def toggle_pump(self):
        """
        Toggle the system pump on or off.
        """
        self._dll.AttoDRY_Interface_togglePump()

    def toggle_sample_temperature_control(self):
        """
        Toggle temperature control for the sample.
        """
        self._dll.AttoDRY_Interface_toggleSampleTemperatureControl()

    def toggle_startup_shutdown(self):
        """
        Toggle system startup or shutdown sequence.
        """
        self._dll.AttoDRY_Interface_toggleStartUpShutdown()

    def upload_sample_temperature_calibration_curve(self, path: str):
        """
        Upload calibration curve for sample temperature sensor.
        """
        self._dll.AttoDRY_Interface_uploadSampleTemperatureCalibrationCurve(c_char_p(path.encode('utf-8')))

    def upload_temperature_calibration_curve(self, curve_number: int, path: str):
        """
        Upload a temperature calibration curve to a given channel.
        """
        self._dll.AttoDRY_Interface_uploadTemperatureCalibrationCurve(c_uint8(curve_number), c_char_p(path.encode('utf-8')))

    def set_vti_heater_power(self, power_watts: float):
        """
        Set the heater power for the VTI (in W).
        """
        self._dll.AttoDRY_Interface_setVTIHeaterPower(c_float(power_watts))

    def get_magnetic_field(self, axis='X') -> float:
        """
        Get the current magnetic field (in T) along the given axis ('X' or 'Z').
        """
        value = c_float()
        if axis.upper() == 'X':
            self._dll.AttoDRY_Interface_getMagneticFieldX(ctypes.byref(value))
        elif axis.upper() == 'Z':
            self._dll.AttoDRY_Interface_getMagneticFieldZ(ctypes.byref(value))
        return value.value

    def get_magnetic_field_setpoint(self, axis='X') -> float:
        """
        Get the magnetic field setpoint (in T) along the given axis ('X' or 'Z').
        """
        value = c_float()
        if axis.upper() == 'X':
            self._dll.AttoDRY_Interface_getMagneticFieldSetPointX(ctypes.byref(value))
        elif axis.upper() == 'Z':
            self._dll.AttoDRY_Interface_getMagneticFieldSetPointZ(ctypes.byref(value))
        return value.value

    def set_user_magnetic_field_axis(self, axis: str, field_tesla: float):
        """
        Set the magnetic field (in T) for the specified axis ('X' or 'Z').
        """
        if axis.upper() == 'X':
            self._dll.AttoDRY_Interface_setUserMagneticFieldX(c_float(field_tesla))
        elif axis.upper() == 'Z':
            self._dll.AttoDRY_Interface_setUserMagneticFieldZ(c_float(field_tesla))

    def get_pressure(self, channel: int) -> float:
        """
        Get the pressure (in mbar) from the specified channel (1 or 2).
        """
        value = c_float()
        if channel == 1:
            self._dll.AttoDRY_Interface_getPressure1(ctypes.byref(value))
        elif channel == 2:
            self._dll.AttoDRY_Interface_getPressure2(ctypes.byref(value))
        return value.value

    def get_valve_status(self, valve: str) -> int:
        """
        Get the status (0/1) of a specified valve ('He', 'Pump800', 'SampleSpace', 'Valve2').
        """
        status = c_int()
        if valve == 'He':
            self._dll.AttoDRY_Interface_getHeValve(ctypes.byref(status))
        elif valve == 'Pump800':
            self._dll.AttoDRY_Interface_getPump800Valve(ctypes.byref(status))
        elif valve == 'SampleSpace':
            self._dll.AttoDRY_Interface_getSampleSpaceValve(ctypes.byref(status))
        elif valve == 'Valve2':
            self._dll.AttoDRY_Interface_getValve2(ctypes.byref(status))
        return status.value

    def toggle_valve(self, valve: str):
        """
        Toggle the state of a specified valve ('SampleSpace', 'Pump800', 'BreakVac', 'Helium800').
        """
        if valve == 'SampleSpace':
            self._dll.AttoDRY_Interface_toggleValveSampleSpace()
        elif valve == 'Pump800':
            self._dll.AttoDRY_Interface_togglePump800Valve()
        elif valve == 'BreakVac':
            self._dll.AttoDRY_Interface_toggleValveBreakVac()
        elif valve == 'Helium800':
            self._dll.AttoDRY_Interface_toggleHelium800Valve()

    def get_reservoir_temperature(self) -> float:
        """Get the temperature of the reservoir (in K)."""
        value = c_float()
        self._dll.AttoDRY_Interface_getTemperature4(ctypes.byref(value))
        return value.value

    def get_turbopump_frequency(self) -> int:
        """
        Get the frequency (in Hz) of the turbopump.
        """
        freq = ctypes.c_uint16()
        self._dll.AttoDRY_Interface_GetTurbopumpFrequ800(ctypes.byref(freq))
        return freq.value

 def get_dll_status(self) -> str:
        """
        Calls LVDLLStatus to get the status string of the DLL.

        Returns:
            str: The error or status message from the DLL.
        """
        err_str_len = 512
        err_str = create_string_buffer(err_str_len)
        module_ptr = c_void_p()  # Assuming no specific module context is needed
        result = self._dll.LVDLLStatus(err_str, err_str_len, ctypes.byref(module_ptr))
        if result != 0:
            raise RuntimeError(f"LVDLLStatus returned error code {result}")
        return err_str.value.decode('utf-8')