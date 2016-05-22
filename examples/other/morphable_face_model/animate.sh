mplayer -ao null out.ogv -vo jpeg:outdir=output
for i in out/*.jpg; do convert $i -crop 360x115+140+160 anim/$(basename $i); done;
convert anim/* out.gif 

