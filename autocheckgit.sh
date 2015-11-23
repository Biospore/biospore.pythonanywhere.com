git fetch origin
diff=$(git log HEAD..origin/master --oneline)
if [ "${diff}" != "" ] ; then
    git pull origin master
fi
