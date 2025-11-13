# NOTES:
# single-number glitch max is 4294967295 (0xffffffff)
# more generally, pow(16, glitch_width) - 1

import argparse
import binascii
import random

# both positional and optional arguments
parser = argparse.ArgumentParser()
parser.add_argument("input", help="mp3 file to be glitched")
parser.add_argument("output", help="output mp3 file name")
parser.add_argument(
    "-p", "--prob", help="percent probability of glitching (float)", type=float
)
parser.add_argument(
    "-m",
    "--hexmin",
    help="decimal representation of minimum hex value to insert (int)",
    type=int,
)
parser.add_argument(
    "-M",
    "--hexmax",
    help="decimal representation of maximum hex value to insert (int)",
    type=int,
)
parser.add_argument(
    "-f",
    "--framemin",
    help="minimum position in frame to glitch (float, 0-1)",
    type=float,
)
parser.add_argument(
    "-F",
    "--framemax",
    help="maximum position in frame to glitch (float, 0-1)",
    type=float,
)
parser.add_argument(
    "-s", "--spacingmin", help="minimum spacing between glitched frames", type=int
)
parser.add_argument(
    "-S", "--spacingmax", help="maximum spacing between glitched frames", type=int
)
parser.add_argument(
    "-w",
    "--width",
    help="number of hex digits to insert in each glitch (int)",
    type=int,
)
parser.add_argument(
    "-l",
    "--limit",
    help="max number of glitches per frame (0 = no limit) (int)",
    type=int,
)
# key-value pairs with argument long names and values
args = parser.parse_args()

# args.input is first cli positional argument
# 'rb' = 'read' + 'binary'; import file here; read as hex
with open(args.input, "rb") as input_file:
    hexdata = input_file.read().hex()

header_start_indices = []
header_start_index = 0
while hexdata.find("fff", header_start_index) >= 0:
    header_start_index = hexdata.find("fff", header_start_index)
    if header_start_index >= 0:
        header_start_indices.append(header_start_index)
    header_start_index += 8

frames = [
    hexdata[header_start_indices[i] : header_start_indices[i + 1]]
    for i in range(len(header_start_indices) - 1)
]


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

frame_spacing_min = 1
if args.spacingmin:
    frame_spacing_min = args.spacingmin

frame_spacing_max = 1
if args.spacingmax:
    frame_spacing_max = args.spacingmax

glitch_width = 8
if args.width:
    glitch_width = args.width

max_glitches_per_frame = 0
if args.limit:
    max_glitches_per_frame = args.limit

hex_digits = "0123456789abcdef"
# strings are immutable, so need a new array
output_hex = []

# variables defined outside test block
num_glitches_this_frame = 0
testval = 0
frame_counter = 0
frame_spacing = 1

for idx_frame, frame in enumerate(frames):
    num_glitches_this_frame = 0
    for idx_digit, digit in enumerate(frame):
        # don't glitch first frame (file header)
        if idx_frame > 0:
            # new chance to glitch every (glitch_width) digits
            # count num per frame
            if idx_digit % glitch_width == 0:
                testval = random.uniform(0, 100)
                if testval < glitch_prob:
                    num_glitches_this_frame += 1
            # perform glitch if testval, not to many glitches for this frame
            # within min/max freq, frame counter is 0
            if (
                testval < glitch_prob
                and (True, num_glitches_this_frame <= max_glitches_per_frame)[
                    max_glitches_per_frame > 0
                ]
                and idx_digit >= (len(frame) * frame_min)
                and idx_digit <= (len(frame) * frame_max)
                and idx_digit >= 8  # leave header alone - first 8 digits
                and frame_counter == 0
            ):
                digit = random.choice(hex_digits[hex_min : hex_max + 1])
        # append digit regardless of glitching
        output_hex.append(digit)
    # choose new frame spacing when counter is 0 (max is +1 because randrange
    # is non-inclusive); increment, wrap (run once per frame)
    if frame_counter == 0:
        frame_spacing = random.randrange(frame_spacing_min, frame_spacing_max + 1)
    frame_counter += 1
    frame_counter %= frame_spacing

rejoined_frames = "".join(output_hex)
# if frames are an odd length, add "0"
if len(rejoined_frames) % 2 != 0:
    rejoined_frames = rejoined_frames + "0"
# 'wb' = 'write' + 'binary'; binascii.unhexlify converts ascii hex -> binary
# args.output is second cli positional argument
with open(args.output, "wb") as output_file:
    output_file.write(binascii.unhexlify(rejoined_frames))

# write to text file for diagnostics
# with open('input_mp3.txt', 'w') as output_file_raw:
#     output_file_raw.write(rejoined_frames)
# with open('output_mp3.txt', 'w') as output_file:
#     output_file.write(rejoined_frames)
