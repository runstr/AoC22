@echo off

set arg1=%1

if exist Day%arg1% ECHO "file already exist" & goto End
mkdir Day%arg1%
if %arg1% gtr 10 ( copy Day13\* Day%arg1%\) ELSE (copy Day1\* Day%arg1%\)

cd Day%arg1%
break>input.txt
break>test_input.txt
echo __all__ = ["day%arg1%_1", "day%arg1%_2"]>__init__.py
if %arg1% gtr 10 ( ren day13_1.py day%arg1%_1.py & ren day13_2.py day%arg1%_2.py) ELSE (ren day1_1.py day%arg1%_1.py & ren day1_2.py day%arg1%_2.py)

cd ..
type day_imports\__init__.py > temp.txt
echo from Day%arg1% import * > imports\__init__.py
type temp.txt >> imports\__init__.py
del temp.txt
echo __all__ += ["day%arg1%_1", "day%arg1%_2"]>>imports\__init__.py

:End
