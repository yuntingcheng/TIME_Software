#!/bin/bash
#DR = $1
ssh -T pilot2@timemce.rit.edu /usr/mce/bin/mce_cmd "-x wb cc data_rate $1"
