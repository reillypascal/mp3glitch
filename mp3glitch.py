import binascii
import random

# 'rb' = 'read' + 'binary'; import file here; read as hex
with open('beat_1_bip_2_F.mp3', 'rb') as input_file:
    hexdata = input_file.read().hex()

# take first 8 characters - that's the header
header = hexdata[:8]
# split at header, removing it
frames = hexdata.split(header)

hex_digits = '0123456789abcdef'
glitch_width = 8
max_glitches_per_frame = 0
num_glitches_this_frame = 0
glitch_prob = 5
hex_min = 0
hex_max = 16
# need testval defined outside test block
testval = 0
# strings are immutable, so need a new array
output_hex = []
# start from index 1 - first index is blank
for frame in frames[1:]:
    output_hex.append(header)
    num_glitches_this_frame = 0
    for idx, digit in enumerate(frame):
        # according to probability, glitch selected length 
        if idx % glitch_width == 0:
            testval = random.uniform(0,100)
            if testval < glitch_prob:
                num_glitches_this_frame += 1
        # comparison for testval; 
        # - glitch_prob must be true
        # - ternary statement: compare number of glitches per frame w/ max allowed *unless* max is zero, then always true
        # - idx must be greater than 0 to avoid glitching whole file's header
        if testval < glitch_prob and (True, num_glitches_this_frame <= max_glitches_per_frame)[max_glitches_per_frame > 0] and idx > 0:
            digit = random.choice(hex_digits[hex_min:hex_max])
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