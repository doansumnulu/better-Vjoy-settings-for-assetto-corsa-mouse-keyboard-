if starting:
    system.setThreadTiming(TimingTypes.HighresSystemTimer)
    system.threadExecutionInterval = 1
    
    def set_button(button, key):
        v.setButton(button, keyboard.getKeyDown(key))
    
    def calculate_rate(max, time):
        if time > 0:
            return max / (time / system.threadExecutionInterval)
        else:
            return max
    
    int32_max = (2 ** 14) - 1
    int32_min = ((2 ** 14) * -1) + 1
    
    v = vJoy[0]
    v.x, v.y, v.z, v.rx, v.ry, v.rz, v.slider, v.dial = (int32_min,) * 8
    
    throttle_inversion = 1
    braking_inversion = 1
    clutch_inversion = 1
    handbraking_inversion = 1
    
    mouse_sensitivity = 0.8
    sensitivity_center_reduction = 1.0
    
    ignition_cut_enabled = True
    ignition_cut_time = 100
    ignition_cut_elapsed_time = 0
    
    steering = 0.0
    steering_max = float(int32_max)
    steering_min = float(int32_min)
    steering_center_reduction = 1.0
    
    throttle_blip_enabled = True
    
    throttle_increase_time = 21
    throttle_increase_time_after_ignition_cut = 0
    throttle_increase_time_blip = 12
    throttle_decrease_time = 13
    
    throttle_max = int32_max * throttle_inversion
    throttle_min = int32_min * throttle_inversion
    throttle = throttle_min
    
    throttle_increase_rate = calculate_rate(throttle_max, throttle_increase_time)
    throttle_increase_rate_after_ignition_cut = calculate_rate(throttle_max, throttle_increase_time_after_ignition_cut) 
    throttle_increase_rate_blip = calculate_rate(throttle_max, throttle_increase_time_blip)
    throttle_decrease_rate = calculate_rate(throttle_max, throttle_decrease_time) * -1
    
    braking_increase_time = 24
    braking_decrease_time = 10
    
    braking_max = int32_max * braking_inversion
    braking_min = int32_min * braking_inversion
    braking = braking_min
    
    braking_increase_rate = calculate_rate(braking_max, braking_increase_time)
    braking_decrease_rate = calculate_rate(braking_max, braking_decrease_time) * -1
    
    clutch_increase_time = 8
    clutch_decrease_time = 15
    
    clutch_max = int32_max * clutch_inversion
    clutch_min = int32_min * clutch_inversion
    clutch = clutch_min
    
    clutch_increase_rate = calculate_rate(clutch_max, clutch_increase_time)
    clutch_decrease_rate = calculate_rate(clutch_max, clutch_decrease_time) * -1
    
    handbraking_increase_time = 0.5
    handbraking_decrease_time = 0.1
    
    handbraking_max = int32_max * handbraking_inversion
    handbraking_min = int32_min * handbraking_inversion
    handbraking = handbraking_min
    
    handbraking_increase_rate = calculate_rate(handbraking_max, handbraking_increase_time)
    handbraking_decrease_rate = calculate_rate(handbraking_max, handbraking_decrease_time) * -1

# assign button
set_button(0, Key.LeftControl)
set_button(1, Key.LeftShift)
set_button(2, Key.C)
set_button(3, Key.W)
set_button(4, Key.E)
set_button(5, Key.R)
set_button(6, Key.T)
set_button(7, Key.Y)

# Steering logic
if steering != 0:
    steering_center_reduction = sensitivity_center_reduction ** (1 - (steering / steering_max))
    
steering += (float(mouse.deltaX) * mouse_sensitivity) / steering_center_reduction
steering = max(min(steering, steering_max), steering_min)
v.x = int(round(steering))

# Clutch logic
clutch += clutch_increase_rate if keyboard.getKeyDown(Key.D) else clutch_decrease_rate
clutch = max(min(clutch, clutch_max * clutch_inversion), clutch_min * clutch_inversion)
v.z = clutch

# Throttle logic
throttle += throttle_increase_rate if keyboard.getKeyDown(Key.W) else throttle_decrease_rate
throttle = max(min(throttle, throttle_max * throttle_inversion), throttle_min * throttle_inversion)
v.y = throttle

# Braking logic
braking += braking_increase_rate if keyboard.getKeyDown(Key.S) else braking_decrease_rate
braking = max(min(braking, braking_max * braking_inversion), braking_min * braking_inversion)
v.rz = braking

# HandBraking logic
handbraking += handbraking_increase_rate if keyboard.getKeyDown(Key.Space) else handbraking_decrease_rate
handbraking = max(min(handbraking, handbraking_max * handbraking_inversion), handbraking_min * handbraking_inversion)
v.ry = handbraking

# Buttons post-throttle logic
# set_button(look_left_button, look_left_key)
# set_button(look_right_button, look_right_key)
# set_button(look_back_button, look_back_key)
# set_button(change_view_button, change_view_key)
# set_button(indicator_left_button, indicator_left_key)
# set_button(indicator_right_button, indicator_right_key)

# PIE diagnostics logic
diagnostics.watch(v.x)
diagnostics.watch(v.y)
diagnostics.watch(v.rz)
diagnostics.watch(v.slider)
diagnostics.watch(steering_center_reduction)
diagnostics.watch(throttle_blip_enabled)
diagnostics.watch(ignition_cut_enabled)

from ctypes import *
user32 = windll.user32

if starting:
    mouselock = False

toggle_mouselock = mouse.getPressed(4)
if toggle_mouselock:
    mouselock = not mouselock

if mouselock:
    user32.SetCursorPos(0, 0)
