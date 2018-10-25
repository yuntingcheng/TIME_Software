#!/bin/bash
ssh -T pilot2@timemce.rit.edu /usr/mce/bin/mce_cmd "-x wb rc$1 data_mode $2"
ssh -T time@time-mce-0.caltech.edu /usr/mce/bin/mce_cmd "-x wb rc$1 data_mode $2"
