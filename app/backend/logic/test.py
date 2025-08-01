with open("./test_binaries/test0.bin", "wb") as f:
    f.write(0x00000293.to_bytes(4, "little"))
    f.write(0x0002A303.to_bytes(4, "little"))
    f.write(0x000173B7.to_bytes(4, "little"))
    f.write(0x0083A023.to_bytes(4, "little"))
    f.write(0x00640933.to_bytes(4, "little"))
    f.write(0x40535213.to_bytes(4, "little"))
    f.write(0xFC7008E3.to_bytes(4, "little"))