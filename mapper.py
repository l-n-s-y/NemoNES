# Returns a bytearray interpretation of a 
# ROM instruction list dumped from twoA03
def map_rom_from_opcode_dump(dump:list) -> bytearray:
    print(dump)
    raw_rom = bytearray()
    for instruction in dump:
        raw_rom.append(instruction.op.opcode)
        [raw_rom.append(arg) for arg in instruction.args]

        print(instruction,raw_rom[-(len(instruction.args)+1):])

    return raw_rom
