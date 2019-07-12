#/bin/bash
dir=$1
cd $dir
go build
mv $dir ../../bin