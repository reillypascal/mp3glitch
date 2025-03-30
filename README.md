# MP3 Glitch
Automates the process of glitching MP3s described in [this article](https://reillyspitzfaden.com/posts/2025/02/databending-part-2/). Note that this only works for constant bitrate (CBR) MP3s at the moment!

## Usage
- Provide the name of an mp3 file in the same folder as the script to serve as an input, followed by the desired output file name
```sh
python3 mp3glitch.py <input_file_name> <output_file_name>
```
- Options
    - `-h, --help`       show this help message and exit
    - `-p, --prob`       percent probability of glitching (float)
    - `-m, --hexmin`     decimal representation of minimum hex value to insert (int)
    - `-M, --hexmax`     decimal representation of maximum hex value to insert (int)
    - `-f, --framemin`   minimum position in frame to glitch (float, 0-1)
    - `-F, --framemax`   maximum position in frame to glitch (float, 0-1)
    - `-s, --spacingmin` minimum spacing between glitched frames (int)
    - `-S, --spacingmax` maximum spacing between glitched frames (int)
    - `-w, --width`      number of hex digits to insert in each glitch (int)
    - `-l, --limit`      max number of glitches per frame (0 = no limit) (int)