#!/bin/bash

SITEPATH=/Users/tknitter/w/gitWS/lplW/lib/python3.7/site-packages/
LPLTPATH=/Users/tknitter/w/gitWS/lplTrade/

cp $LPLTPATH/src/*py $SITEPATH/lplTrade || exit 1

cp $LPLTPATH/pyetrade/*py $SITEPATH/pyetrade || exit 1

