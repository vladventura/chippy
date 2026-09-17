import time
import keypad_input
import timer
import cpu
import memory_bus
import gpu
import pygame

memory_bus.initialize_memory()
# memory_bus.load_program('./test_opcode.ch8')
memory_bus.load_program('./delay_timer_test.ch8')
cpu.initialize_cpu()
gpu.initialize_gpu()

ins_counter = 0
ins_this_step = 0.0

print(
f"""
Chip-8 emulator by Vladimir Ventura

This is seriously so confusing btw.

Run speed = {timer.timer_run_speed}
Instructions per step = {timer.timer_instructions_per_step}
Instruction duration = {timer.timer_instruction_duration}
"""
)

while True:
    st = time.perf_counter()
    keypad_input.capture_input()
    if not cpu.cpu_await_keypress:
        while (ins_this_step < int(timer.timer_instructions_per_step)):
            run_result = cpu.run()
            if not run_result: break
            if cpu.cpu_await_keypress: break
            ins_this_step += 1
            ins_counter += 1
    # Handle audio
    timer.tick_delay()
    pygame.display.flip()
    ins_this_step = 0.0
    el = time.perf_counter() - st
    if el < timer.timer_run_speed:
        time.sleep(timer.timer_run_speed - el)
