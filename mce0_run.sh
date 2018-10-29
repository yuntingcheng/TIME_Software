#!/bin/bash
ssh -T time@time-mce-0.caltech.edu /usr/mce/mce_script/script/mce_run "temp $1 $2 --sequence=$3"
