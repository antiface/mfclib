#!/bin/bash

SCRIPT_DIR=`pwd`
PYTHON_EXEC='/usr/bin/python'
MFCLIB_VERSION=`cat VERSION`
MFCLIB_PACKAGES='core.Query core.mfclibAppHandler'

echo 'Removing MANIFEST file...'
rm MANIFEST

echo 'Removing build folder...'
rm -rf build
echo 'Removing dist folder...'
rm -rf dist

echo 'Creating setup.py...'
echo "#!$PYTHON_EXEC" > setup.py

echo 'Creating test script...'
echo "#!$PYTHON_EXEC" > test.py


echo "from distutils.core import setup" >> setup.py 
echo "setup(" >> setup.py 
echo "  name='mfclib'," >> setup.py
echo "  version='$MFCLIB_VERSION'," >> setup.py
echo "  py_modules=[" >> setup.py
echo "    'mfclib'," >> setup.py

for mod in `find ./lib -name '*.py' | grep -rv __init__.py | sed 's/\//./g' | sed 's/\.\.//g' | sed 's/\.py//g'`;
do
	echo "import $mod" >> test.py
	echo "    '$mod'," >> setup.py
done

echo "  ]" >> setup.py
echo ")" >> setup.py

TEST_EXEC=`$PYTHON_EXEC $SCRIPT_DIR/test.py 2> /dev/null && echo $?`

if [ $? -eq 0 ];then
	echo "--[Test passed]--"
else
	echo "--------------[Test failed]-----------------"
	`$PYTHON_EXEC $SCRIPT_DIR/test.py`
	echo "--------------------------------------------"
	exit
fi

rm $SCRIPT_DIR/test.py

echo 'Removing python cache...'
find . -name __pycache__ -delete
find . -name \*.pyc -delete
python setup.py sdist
python setup.py install
