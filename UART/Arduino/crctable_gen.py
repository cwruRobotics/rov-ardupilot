crc_lookup = [0] * 256

poly = 0x107 # x^8 + x^2 + x + 1

# Generate the CRC value for each value in a byte range
for i in range(0,256):
    # shift the current index up 8 values to get the remainder as 0 in the 8 LSBs
    crc = i << 8
        
    # divide while the dividend (the index) is greater than 0 
    while crc & 0xFF00 > 0:
        divisor = 0
        # generate the divisor by shifting the polynomial to line up with the MSB of the dividend
        for msb_index in range(7, -1, -1):
            if crc & (1 << msb_index + 8) > 0:
                divisor = poly << msb_index
        
        # perform XOR to find the crc of this index
        crc = crc ^ divisor
    
    # put the crc (the remainder) into the lookup table
    crc_lookup[i] = crc & 0x00FF

# generate the output in a nice format to be pasted into code
output = "[\n    "
index = 0

# iterate over the loopup table
for val in crc_lookup:

    # convert the current value to hex
    val_output = "{}".format(hex(val))

    # if converted value does not have 4 characters, add a 0 after the 0x to make it have 4 characters
    if len(val_output) < 4:
        val_output = "{}{}{}{}".format(val_output[0], val_output[1], "0", val_output[2])

    # append it to the output
    output = "{}{}, ".format(output, val_output)

    # every 8 values, go to a new line
    if ((index + 1) % 8) == 0:
        output = "{}\n    ".format(output)
    index = index + 1

print(output)
print("]")

# make sure the sorted output has 1 of each value in the byte range
crc_lookup.sort()
print(crc_lookup == range(0,256))