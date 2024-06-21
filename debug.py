def dbgerr(msg):
    print(f"[ERROR]{msg}")

def dbgwarn(msg):
    print(f"[WARNING]{msg}")

def dbglog(msg):
    print(f"[DEBUG]{msg}")

def hexd(n,pad=False,pad_count=2):
    out = hex(n).replace("0x","").upper()
    if pad: return out if n > 0x1*(16**(pad_count)) else ("0"*(pad_count-len(out)))+out
    return out

