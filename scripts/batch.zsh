#!/usr/bin/env zsh

# remember mp3 paths in input folder for cleanup after glitching
input_mp3s=()

for file in ./input/**/*.wav; do
	# https://trac.ffmpeg.org/wiki/Encode/MP3
	# ffmpeg -i $file -codec:a libmp3lame -b:a 320k ${file%.*}.mp3
	mp3_file="${file%.*}.mp3"
	ffmpeg -i "$file" -codec:a libmp3lame -q:a 0 "$mp3_file"
	input_mp3s+=("$mp3_file")
done

mp3glitch input output -p 7 -M 6 -w 19

for file in ./output/**/*.mp3; do
	# convert glitched mp3 back to wav
	ffmpeg -i "$file" "${file%.*}.wav"
	# remove mp3s in output folder
	rm "$file"
done

# clean up mp3s in input folder
for file in "${input_mp3s[@]}"; do
	rm "$file"
done
