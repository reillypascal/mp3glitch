# mp3glitch

Python tool for glitching MP3s while leaving them playable. Includes many options to shape glitching amount, character, and timbre.

The mechanics behind this are described in [this article](https://reillyspitzfaden.com/posts/2025/02/databending-part-2/), and I discuss using Python to do the glitching in [this article](https://reillyspitzfaden.com/posts/2025/04/databending-part-3/).

Should work for both constant bit rate (CBR) and variable bit rate (VBR) MP3s.

## Usage

- Provide the path of an input MP3 file, followed by the desired output file name, OR provide an input and output directory. NOTE: input/output must both be either files or directories.

```bash
mp3glitch <input_file_or_directory> <output_file_or_directory>
```

- Options
    - `-h`, `--help` show this help message and exit
    - `-p`, `--prob` percent probability of glitching (float)
    - `-m`, `--hexmin` decimal representation of minimum hex value to insert (int)
    - `-M`, `--hexmax` decimal representation of maximum hex value to insert (int)
    - `-f`, `--framemin` minimum position in frame to glitch (float, 0-1)
    - `-F`, `--framemax` maximum position in frame to glitch (float, 0-1)
    - `-s`, `--spacingmin` minimum spacing between glitched frames (int)
    - `-S`, `--spacingmax` maximum spacing between glitched frames (int)
    - `-w`, `--width` number of hex digits to insert in each glitch (int)
    - `-l`, `--limit` max number of glitches per frame (0 = no limit) (int)

NOTE: while the resulting MP3 is still playable, it will likely have e.g., denormal values, and with greater glitch probability or `hexmax` values, this can still cause difficulty with playback. When composing with this tool, I usually use FFmpeg to convert a WAV sample to MP3, glitch it, and then convert back to WAV in order to have the noisy artifacts without the playback difficulty.

The `scripts/` directory contains example Bash (Bash 4+ only) and Zsh scripts to perform this on batches of files, deleting the unused MP3 files along the way. MAKE SURE you understand what the scripts do before using them! They use the `rm` action on the MP3 files, which is permanent.
