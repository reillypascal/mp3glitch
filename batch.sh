#!/bin/zsh

# https://gist.github.com/valosekj/dce78453f232362201ac4f8229678bd4
# https://stackoverflow.com/questions/125281/how-do-i-remove-the-file-suffix-and-path-portion-from-a-path-string-in-bash

# https://trac.ffmpeg.org/wiki/Encode/MP3

for file in ./input/**/*(.); do
	# if wav, encode as mp3 vbr0
	if [[ "${file##*.}" == "wav" ]]; then
		ffmpeg -i $file -codec:a libmp3lame -q:a 0 ${file%.*}.mp3
		# ffmpeg -i $file -codec:a libmp3lame -b:a 320k ${file%.*}.mp3
	fi
	# swap "input" w/ "output" in file path; make subdir in "output" folder
	new_path=${file/input/output}
	mkdir -p $(dirname "${new_path}")
	
	python3 mp3glitch.py ${file%.*}.mp3 ${new_path%.*}.mp3 -p 8 -M 4 -w 16 # -f 0
	# convert glitched mp3 back to wav
	ffmpeg -i ${new_path%.*}.mp3 $new_path
	# remove both clean and glitched mp3s
	rm ${file%.*}.mp3 ${new_path%.*}.mp3
	# rm ${file%.*}.mp3

done
