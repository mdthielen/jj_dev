mayalocation=/Applications/Autodesk/maya2014/Maya.app/Contents/bin
pythonhome=$mayalocation/../Frameworks/Python.framework/Versions/Current
export PYTHONHOME=$pythonhome
export DYLD_LIBRARY_PATH=$mayalocation/../MacOS:$DYLD_LIBRARY_PATH
export DYLD_FRAMEWORK_PATH=$mayalocation/../Frameworks:$DYLD_FRAMEWORK_PATH
export MAYA_LOCATION=$mayalocation/..

echo "Enter episode and sequence as ### ###: "
read -e INFO

cd /Volumes/public/StoryBots/sbtv/03_shared_assets/01_cg/maya_tools/maya_scripts/python
pwd

python animPrep.py $INFO
#set -m
#suspend -f