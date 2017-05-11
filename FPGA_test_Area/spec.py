sdstatus = [128, 0, 0, 0, 8, 0, 0, 0, 4, 1, 144, 0, 16, 66, 63, 90, 0, 64, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sdstatus_py = []
for byte in sdstatus:
	sdstatus_py.append(hex(byte))
print sdstatus_py