timer_instructions_per_second = 700
timer_instruction_duration = 1 / timer_instructions_per_second
timer_run_speed = 1 / 60
timer_instructions_per_step = timer_run_speed / timer_instruction_duration

timer_delay = 0x00
timer_sound = 0x00

def tick_delay():
    global timer_delay
    
    if timer_delay <= 0:
        return
    timer_delay -= 1
