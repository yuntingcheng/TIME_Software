#!/bin/bash
RC = $1
ssh -T time@time-mce-0.caltech.edu /usr/mce/bin/mce_cmd "-x stop rc$RC ret_dat"
