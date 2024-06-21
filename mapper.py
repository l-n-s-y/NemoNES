# Returns a bytearray interpretation of a 
# ROM instruction list dumped from twoA03
def map_rom_from_opcode_dump(dump:list) -> bytearray:
    raw_rom = bytearray()
    for instruction in dump:
        raw_bytes = int(instruction.op.opcode + "".join(instruction.args),16)
        raw_rom.append(raw_bytes)

    return raw_rom
