import binascii
import random

# 'rb' = 'read' + 'binary'; import file here
with open('beat_1_bip_2_F.mp3', 'rb') as input_file:
    hexdata = input_file.read().hex()

# take first 8 characters - that's the header
header = hexdata[:8]
# split at header, removing it
frames = hexdata.split(header)

testval = 0
# strings are immutable, so need a new array
output_hex = []
# start from index 1 - first index is blank
for frame in frames[1:]:
    output_hex.append(header)
    for idx, digit in enumerate(frame):
        # according to probability, glitch an entire octet
        if idx % 8 == 0:
            testval = random.randrange(100)
        # comparison for testval; idx must be greater than 0 to avoid glitching whole file's header
        if testval < 5 and idx > 0:
            digit = random.choice('0123456789abcdef')
        output_hex.append(digit)

# join frames using header as separator - note method is applied to separator, not iterable item!
rejoined_frames = ''.join(output_hex)
# need to use 'wb' to get it to write as *binary*, not text
# binascii.unhexlify converts ascii hex -> binary
with open('binary_mp3.mp3', 'wb') as output_file:
    output_file.write(binascii.unhexlify(rejoined_frames))

# write to text file for diagnostics
# with open('binary_mp3.txt', 'w') as output_file: 
#     output_file.write(rejoined_frames)