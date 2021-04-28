#! /bin/sh

copyboard=""

if [[ `uname` == 'Darwin' ]]; then
	copyboard="pbcopy"
    echo "Mac OS"
fi


if [[ `uname` == 'Linux' ]]; then
	copyboard="xclip"
    echo "Linux"
fi

while :
do
	nc -l 8377 | $copyboard -selection c
done
