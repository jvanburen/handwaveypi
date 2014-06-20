#!/bin/bash
let port=$1
shift
let width=$1
let height=$2
shift 2
for p in {40000..40250}
do
	raspiyuv -w $width -h $height -hf -n -t 0 -o - $* | nc -l $p &
	sleep 0.1
done
