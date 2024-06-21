import sys,time,pygame

sys.path.append("..//ines_mapper//")
sys.path.append("../2a03_dissassembler//")

import ines_mapper
import twoA03
from debug import *
import cpu as CPU

# constants

KB = 1024
TWO_KB = 2048


def main():
    size = (256,240)
    #screen = pygame.display.set_mode(size)

    # 1.79 MHz (1.79mil / sec)
    cpu = CPU.CPU()

    while True:
        if not cpu.cycle():
            dbglog("[NEMO] Goodbye.")
            exit()

        pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [rom]")
        exit()

    

    main()
