import argparse
import mp3glitch.fn as fn

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


def app():
    config = fn.run_config(args)
    frames = fn.read_file(args.input)
    output_hex = fn.apply_glitches(frames, config)
    fn.write_file(output_hex, args.output)
