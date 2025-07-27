#!/bin/bash
set -e

sudo pytest test_network.py test_exec.py test_bpf.py -v #> test_log.txt
