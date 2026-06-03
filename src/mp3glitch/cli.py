import argparse
from pathlib import Path
import mp3glitch.fn as fn

# both positional and optional arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "input",
    help="mp3 file/directory of mp3 files to be glitched (input/output must both be either file or directory)",
)
parser.add_argument(
    "output",
    help="output mp3 file name/output directory (input/output must both be either file or directory)",
)
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


def app():
    config = fn.make_config(args)
    input_path = Path(args.input)
    output_path = Path(args.output)

    # process single in/out file if input is a file and output is not a directory
    # TODO: try using pathlib PurePath to check if input path *could be* a file
    # NOTE: since output file wouldn't exist, can't check if output is a file!
    if input_path.is_file() and not output_path.is_dir():
        frames = fn.read_file(args.input)
        output_hex = fn.apply_glitches(frames, config)
        fn.write_file(output_hex, args.output)

        return 0

    # iterate over directory/-ies
    # glitch/write all files to output dir (flat hierarchy)
    if input_path.is_dir() and output_path.is_dir():
        mp3_files = input_path.glob("**/*.mp3")
        for file in mp3_files:
            frames = fn.read_file(file)
            output_hex = fn.apply_glitches(frames, config)
            fn.write_file(output_hex, str(output_path / file.name))

        return 0

    # if one of input/output is a directory, but the other isn't, error
    if input_path.is_dir() != output_path.is_dir():
        print("Error: input and output types (file or directory) must match")

        # TODO: better to use error types than exit codes?
        return 1

    return 1
