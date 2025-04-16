#!/bin/zsh

# https://gist.github.com/valosekj/dce78453f232362201ac4f8229678bd4
# https://stackoverflow.com/questions/125281/how-do-i-remove-the-file-suffix-and-path-portion-from-a-path-string-in-bash

# https://trac.ffmpeg.org/wiki/Encode/MP3

for file in ./input/**/*(.); do
	#if [ "${file##.}" == "wav" ]; then
		ffmpeg -i $file -codec:a libmp3lame -q:a 0 ${file%.*}.mp3
	#fi
	
	new_path=${file/input/output}
	# new_ext=${new_path%.*}.wav
	# mkdir -p $(dirname "${new_ext}")
	mkdir -p $(dirname "${new_path}")
	
	python3 mp3glitch.py ${file%.*}.mp3 ${new_path%.*}.mp3 -M 10 -w 6	

	ffmpeg -i ${new_path%.*}.mp3 $new_path
	
	rm ${file%.*}.mp3 ${new_path%.*}.mp3
done
