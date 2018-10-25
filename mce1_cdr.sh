#!/bin/bash
ssh -T pilot2@timemce.rit.edu /usr/mce/bin/mce_cmd "-x wb cc data_rate $1"
ssh -T time@time-mce-0.caltech.edu /usr/mce/bin/mce_cmd "x wb cc data_rate $1"
