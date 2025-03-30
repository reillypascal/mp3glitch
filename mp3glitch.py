import argparse
import binascii
import random

# both positional and optional arguments
parser = argparse.ArgumentParser()
parser.add_argument("input", help="mp3 file to be glitched")
parser.add_argument("output", help="output mp3 file name")
parser.add_argument("-p", "--prob", help="percent probability of glitching (float)", type=float)
parser.add_argument("-m", "--hexmin", help="minimum hex value to insert (int)", type=int)
parser.add_argument("-M", "--hexmax", help="maximum hex value to insert (int)", type=int)
parser.add_argument("-f", "--framemin", help="minimum position in frame to glitch (float, 0-1)", type=float)
parser.add_argument("-F", "--framemax", help="maximum position in frame to glitch (float, 0-1)", type=float)
parser.add_argument("-w", "--width", help="number of hex digits to insert in each glitch (int)", type=int)
parser.add_argument("-l", "--limit", help="max number of glitches per frame (0 = no limit) (int)", type=int)
# key-value pairs with argument long names and values
args = parser.parse_args()

# args.input is first cli positional argument
# 'rb' = 'read' + 'binary'; import file here; read as hex
with open(args.input, 'rb') as input_file:
    hexdata = input_file.read().hex()

# take first 8 characters - that's the header (in CBR MP3s, at least)
header = hexdata[:8]
# split at header, removing it
frames = hexdata.split(header)

# argument variables
glitch_prob = 5
if args.prob:
    glitch_prob = args.prob

hex_min = 0
if args.hexmin:
    hex_min = args.hexmin

hex_max = 16
if args.hexmax:
    hex_max = args.hexmax

frame_min = 0
if args.framemin:
    frame_min = args.framemin

frame_max = 1
if args.framemax:
    frame_max = args.framemax

glitch_width = 8
if args.width:
    glitch_width = args.width

freq_spacing = 1

freq_spacing_min = 1

freq_spacing_max = 8

frame_spacing = 2

frame_spacing_min = 2

frame_spacing_max = 12

max_glitches_per_frame = 0
if args.limit:
    max_glitches_per_frame = args.limit

# preset variables
hex_digits = '0123456789abcdef'
num_glitches_this_frame = 0
# need testval defined outside test block
testval = 0
# strings are immutable, so need a new array
output_hex = []

frame_counter = 0
freq_counter = 0
glitch_width_counter = 0
# start from index 1 - first index is blank
for idx_frame, frame in enumerate(frames[1:]):
    output_hex.append(header)
    num_glitches_this_frame = 0
    for idx_digit, digit in enumerate(frame):
        # don't glitch first frame (file header)
        if idx_frame > 0:
            # - idx_digit must be between given min/max
            if (
                idx_digit >= (len(frame) * frame_min) and
                idx_digit <= (len(frame) * frame_max)
            ):
                # choose new frame/freq spacings when respective counters are 0
                if frame_counter == 0:
                    frame_spacing = random.randrange(frame_spacing_min, frame_spacing_max)
                if freq_counter == 0:
                    freq_spacing = random.randrange(freq_spacing_min, freq_spacing_max)
                # when frame/freq counters both indicate to start, reset glitch width counter
                if frame_counter == 0 and freq_counter == 0:
                    glitch_width_counter = 0
                # 
                if glitch_width_counter < glitch_width:
                    digit = random.choice(hex_digits[hex_min:hex_max + 1])
                    glitch_width_counter += 1
            # if no longer glitching digits, start counting until next time in frequency spectrum
            if glitch_width_counter >= glitch_width:
                freq_counter += 1
                freq_counter %= freq_spacing
        # append digit regardless of glitching
        output_hex.append(digit)
    frame_counter += 1
    frame_counter %= frame_spacing

# join frames using header as separator - note method is applied to separator, not iterable item!
rejoined_frames = ''.join(output_hex)
# 'wb' = 'write' + 'binary'; binascii.unhexlify converts ascii hex -> binary
# args.output is second cli positional argument
with open(args.output, 'wb') as output_file:
    output_file.write(binascii.unhexlify(rejoined_frames))

# write to text file for diagnostics
# with open('input_mp3.txt', 'w') as output_file_raw:
#     output_file_raw.write(hexdata)
# with open('output_mp3.txt', 'w') as output_file: 
#     output_file.write(rejoined_frames)