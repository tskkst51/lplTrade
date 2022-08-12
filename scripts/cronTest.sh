#!/bin/bash

env > /tmp/crontTestENV.$$
echo lplt value: $LPLT >> /tmp/crontTestENV.$$
echo user value: $USER >> /tmp/crontTestENV.$$

. ${HOME}/.bashrc
env >> /tmp/crontTestENV.$$

exit 0
