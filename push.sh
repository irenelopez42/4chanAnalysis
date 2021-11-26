#!/bin/bash
#Commit and push all files in the 4chanAnalysis folder
echo add files
git add -a
echo commit
git commit -m "4plebs results by machine `hostname`"
echo pull remote changes
git pull
echo push
git push