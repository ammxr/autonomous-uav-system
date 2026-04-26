import pygame
import serial
import time

try:
    ser = serial.Serial("COM3", 115200, timeout=0.1) # COM Port, matching with device manager 
except:
    print("Could not open COM port. Check Device Manager!")
    exit()

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No PS5 Controller found")
    exit()

js = pygame.joystick.Joystick(0)
js.init()
print(f"Connected to: {js.get_name()}")

try:
    while True:
        pygame.event.pump()

        # Left Stick: Axis 0 (H), Axis 1 (V)
        # Right Stick: Axis 2 (H), Axis 3 (V)
        throttle = js.get_axis(1)   
        roll     = js.get_axis(2)   
        pitch    = js.get_axis(3)   
        yaw      = js.get_axis(0)   

        # Convert -1.0..1.0 to 1000..2000
        def scale_pwm(val):
            if abs(val) < 0.05: val = 0 # stick deadzone
            return int(1500 + (val * 500)) # pwm neutral at 1500 

        t_pwm = scale_pwm(throttle)
        r_pwm = scale_pwm(roll)
        p_pwm = scale_pwm(pitch)
        y_pwm = scale_pwm(yaw)

        # Sent as a formatted string: "T1500,R1500,P1500,Y1500\n"
        msg = f"T{t_pwm}R{r_pwm}P{p_pwm}Y{y_pwm}\n"
        ser.write(msg.encode())

        print(f"Sending: {msg.strip()}", end='\r')
        time.sleep(0.02) # 50Hz PWM signals

except KeyboardInterrupt:
    ser.close()
    print("\nScript Stopped.")