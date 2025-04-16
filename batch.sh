#!/bin/zsh

# https://gist.github.com/valosekj/dce78453f232362201ac4f8229678bd4
# https://stackoverflow.com/questions/125281/how-do-i-remove-the-file-suffix-and-path-portion-from-a-path-string-in-bash

for file in ./input/**/*(.); do
	new_path=${file/input/output}
	new_ext=${new_path%.*}.wav
	mkdir -p $(dirname "${new_ext}")
	
	python3 mp3glitch.py $file $new_path -M 10 -w 6	

	ffmpeg -i $new_path $new_ext
done
