import binascii
import random


def make_config(args):
    config = {
        "glitch_prob": 5,
        "hex_min": 0,
        "hex_max": 16,
        "frame_min": 0,
        "frame_max": 1,
        "frame_spacing_min": 1,
        "frame_spacing_max": 1,
        "glitch_width": 8,
        "max_glitches_per_frame": 0,
    }

    # TODO:
    # for key in config:
    #   if key in <config file heading>:

    # argument variables
    if args.prob:
        config["glitch_prob"] = args.prob
    if args.hexmin:
        config["hex_min"] = args.hexmin
    if args.hexmax:
        config["hex_max"] = args.hexmax
    if args.framemin:
        config["frame_min"] = args.framemin
    if args.framemax:
        config["frame_max"] = args.framemax
    if args.spacingmin:
        config["frame_spacing_min"] = args.spacingmin
    if args.spacingmax:
        config["frame_spacing_max"] = args.spacingmax
    if args.width:
        config["glitch_width"] = args.width
    if args.limit:
        config["max_glitches_per_frame"] = args.limit

    return config


def read_file(input_path):
    # args.input is first cli positional argument
    # 'rb' = 'read' + 'binary'; import file here; read as hex
    with open(input_path, "rb") as input_file:
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

    return frames


# NOTE:
#   single-number glitch max is 4294967295 (0xffffffff)
#   more generally, pow(16, glitch_width) - 1
def apply_glitches(frames, config):
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
                if idx_digit % config["glitch_width"] == 0:
                    testval = random.uniform(0, 100)
                    if testval < config["glitch_prob"]:
                        num_glitches_this_frame += 1
                # perform glitch if testval, not to many glitches for this frame
                # within min/max freq, frame counter is 0
                if (
                    testval < config["glitch_prob"]
                    and (
                        True,
                        num_glitches_this_frame <= config["max_glitches_per_frame"],
                    )[config["max_glitches_per_frame"] > 0]
                    and idx_digit >= (len(frame) * config["frame_min"])
                    and idx_digit <= (len(frame) * config["frame_max"])
                    and idx_digit >= 8  # leave header alone - first 8 digits
                    and frame_counter == 0
                ):
                    digit = random.choice(
                        hex_digits[config["hex_min"] : config["hex_max"] + 1]
                    )
            # append digit regardless of glitching
            output_hex.append(digit)
        # choose new frame spacing when counter is 0 (max is +1 because randrange
        # is non-inclusive); increment, wrap (run once per frame)
        if frame_counter == 0:
            frame_spacing = random.randrange(
                config["frame_spacing_min"], config["frame_spacing_max"] + 1
            )
        frame_counter += 1
        frame_counter %= frame_spacing

    return output_hex


def write_file(output_hex, output_path):
    rejoined_frames = "".join(output_hex)
    # if frames are an odd length, add "0"
    if len(rejoined_frames) % 2 != 0:
        rejoined_frames = rejoined_frames + "0"
    # 'wb' = 'write' + 'binary'; binascii.unhexlify converts ascii hex -> binary
    # args.output is second cli positional argument
    with open(output_path, "wb") as output_file:
        output_file.write(binascii.unhexlify(rejoined_frames))
