#!/bin/bash
RC = $1
FRAME = $2
ssh -T time@time-mce-0.caltech.edu /usr/mce/bin/mce_cmd "-x wb rc$RC data_mode $FRAME"
