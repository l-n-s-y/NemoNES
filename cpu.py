import sys

sys.path.append("..\\2a03_dissassembler")
import twoA03
import mapper
from debug import *

OPCODE_FILE = "raw_opcodes.txt"

KB = 1024
TWO_KB = 2048


#### DEBUG ####
ROM_DUMP = "..\ines_mapper\smb.nes.prg"
###############


class CPU:
    def __init__(self):
        self.ram_start = 0x0000
        self.ram_size = TWO_KB
        self.ram_end = self.ram_start+self.ram_size-1

        self.ram_mirror_start = 0x0800
        self.ram_mirror_size = TWO_KB*3
        self.ram_mirror_end = self.ram_mirror_start+self.ram_mirror_size-1

        self.ppu_registers_start = 0x2000
        self.ppu_registers = 8
        self.ppu_registers_end = self.ppu_registers_start+self.ppu_registers-1
        self.ppu_mirror_size = KB*8

        self.apu_io_start = 0x4000
        self.apu_io_size = 0x401F
        self.apu_io_end = self.apu_io_start+self.apu_io_size-1

        # Usually reserved for cartridge RAM and ROM
        self.cart_ram_start = 0x6000
        self.cart_ram_size = 0x2000
        self.cart_ram_end = self.cart_ram_start+self.cart_ram_size-1

        self.cart_rom_start = 0x8000
        self.cart_rom_size = 0x8000
        self.cart_rom_end = self.cart_rom_start+self.cart_rom_size-1
        #self.unmapped_start = 0x4020
        #self.unmapped_size = 0xBFE0

        # interrupt vectors
        self.nmi_vector = 0xFFFA # points to the NMI handler
        self.nmi_vector_size = 2
        
        self.reset_vector = 0xFFFC # points to chipset initialisation code
        self.reset_vector_size = 2

        self.IRQ_vector = 0xFFFE # aka BRK vector, points to mapper's interrupt handler

        self.cycles = 0
    
        self.X = 0
        self.Y = 0
        self.A = 0

        self.PC = 0xFFFC
        #self.PC = 0

        self.flags = {
            "C":0, # Carry 
            "Z":0, # Zero
            "I":1, # Interrupt disable
            "D":0, # Decimal
            "V":0, # Overflow
            "N":0, # Negative
        }


        self.ram_initialised = False
        self.init_ram()

        self.rom_initialised = False

        # DEBUG #
        #self.load_cart(ROM_DUMP)
        self.load_cart(twoA03.disassemble(ROM_DUMP))
        #########


        self.opcodes = twoA03.parse_opcodes_from_file(OPCODE_FILE)

    def cycle(self):

        """
        # update RAM mirrors
        # TODO: Add cache checks to avoid unecessary copies
        for i in range(0,self.ram_mirror_size*10,int((self.ram_mirror_size/3)*10)):
            i //= 10

            # skip mirroring if no change in RAM
            if self.ram[:self.ram_size] == self.ram[i:i+self.ram_size]: break

            # mirror
            self.ram[i:i+self.ram_size] = self.ram[:self.ram_size]

            print(self.ram[i:i+self.ram_size])


        """
        if not self.rom_initialised:
            dbgerr(f"[CPU] ROM not initialised. Load a cart dump.")
            return False


        op = self.read(self.PC)
        if op == -1:
            dbgerr(f"[CPU] Invalid opcode (cycles:{self.PC}).\nAborting...")
            return False
        self.PC += 1

        self.cycles += 1

        return True
    
    
    def read(self,addr):
        if not self.ram_initialised:
            dbgerr("[READ] RAM not initialised.")
            return -1

        if addr < 0x0 or addr >= 0xFFFF: 
            dbgerr(f"[READ] Out-of-bounds @ [{addr}].")
            return -1

        return self.ram[addr]


    def read_range(self,addr,size):
        if not self.ram_initialised:
            dbgerr("[READRANGE] RAM not initialised.")
            return -1

        if addr < 0x0 or addr >= 0xFFFF:
            dbgerr(f"[READRANGE] Out-of-bounds @ [{addr}].")
            return -1

        return self.ram[addr:addr+size]
        

    def write(self,addr,value):
        if not self.ram_initialised: 
            dbgerr("[WRITE] RAM not initialised.")
            return False

        if addr < 0x0 or addr >= 0xFFFF: 
            dbgerr(f"[WRITE] Out-of-bounds @ [{addr}].")
            return False

        # prevent writing to RAM mirrors
        #if addr >= self.ram_mirror_start and addr < self.ram_mirror_start+self.ram_mirror_size:
        if addr >= self.ram_mirror_start and addr <= self.ram_mirror_end:
            dbgerr(f"[WRITE] Access violation @ [{addr}]. (RAM mirror space).")
            return False

        # write to CPU RAM
        #if addr >= self.ram_start and addr < self.ram_start+self.ram_size:
        if addr >= self.ram_start and addr <= self.ram_end:
            self.ram[addr] = value
            for i in range(1,4): # mirror RAM
                self.ram[addr+(i*TWO_KB)] = value
    
            return True

        # write to PPU registers
        #if addr >= self.ppu_registers_start and addr < self.ppu_registers_start+self.ppu_registers:
        #    self.ram[addr] = value

    def load_cart(self,rom_dump):
        self.rom = rom_dump
        raw_rom = mapper.map_rom_from_opcode_dump(rom_dump)
        dbglog("[LOAD] Mapping cart ROM...")
        for i in range(len(raw_rom)):
            print(hex(0x8000+i),hex(len(raw_rom)+0x8000))
            self.write(0x8000+i,raw_rom[i]);
            self.read(0x8000+i)
        self.rom_initialised = True

    def init_ram(self):
        self.ram = bytearray([0 for _ in range(0xffff)])
        self.ram_initialised = True
