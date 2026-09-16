import time
import timer
import cpu
import memory_bus
import gpu

memory_bus.initialize_memory()
memory_bus.load_program('./test_opcode.ch8')
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
    while (ins_this_step < timer.timer_instructions_per_step):
        run_result = cpu.run()
        if not run_result: break
        ins_this_step += timer.timer_instruction_duration
        ins_counter += 1
    # Handle input
    # Handle audio
    # Tick timers
    gpu.screen_heartbeart()
    ins_this_step = 0.0
    time.sleep(timer.timer_run_speed)
