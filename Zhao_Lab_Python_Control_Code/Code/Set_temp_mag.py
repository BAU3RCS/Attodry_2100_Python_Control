from Attodry_wrapper_class import AttoDRYInterface
import time
"""
The "C function returned error code: -1073807246" error from connect
means there is another program open using the com port the Attocube is on
"""

AD = AttoDRYInterface()


AD.begin()
AD.connect()

initialized = 0

while initialized==0:
    initialized = AD.is_initialised()

print("Connected and Initliazed")

print(f"VTI Temp. {AD.get_vti_temperature()}K")

print(f"This is the User setpoint temp. {AD.get_user_temperature_setpoint()}K")
print(f"This is the sample temp. {AD.get_sample_temperature()}K")

AD.set_user_temperature(4)
AD.toggle_full_temperature_control()

time.sleep(5)

print(f"This is the User setpoint temp. {AD.get_user_temperature_setpoint()}K")
print(f"This is the sample temp. {AD.get_sample_temperature()}K")

#AD.toggle_magnetic_field_control()



# AD.set_user_magnetic_field_axis("X",0.01)
# AD.set_user_magnetic_field_axis("Z",0.01)
# AD.set_user_magnet_setpoint(0.01)


# print()
# print("Magnetic Field User Setpoint")
# print(f"X: {AD.get_user_magnetic_field_setpoint_axis('X')} Tesla")
# print(f"Y: {AD.get_user_magnet_setpoint()} Tesla")
# print(f"Z: {AD.get_user_magnetic_field_setpoint_axis('Z')} Tesla")

# time.sleep(10)

# print()
# print("Magnetic Field User Setpoint")
# print(f"X: {AD.get_user_magnetic_field_setpoint_axis('X')} Tesla")
# print(f"Y: {AD.get_user_magnet_setpoint()} Tesla")
# print(f"Z: {AD.get_user_magnetic_field_setpoint_axis('Z')} Tesla")


AD.Disconnect()
AD.End()

print("Script Done")