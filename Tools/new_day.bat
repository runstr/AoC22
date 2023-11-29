@echo off

set arg1=%1
set arg2=%2
cd ..\y%arg2%
if exist Day%arg1% ECHO "file already exist" & goto End
mkdir Day%arg1%
copy ..\DefaultDay\* Day%arg1%\

cd Day%arg1%
break>input.txt
break>example.txt
echo __all__ = ["day%arg1%_1", "day%arg1%_2"]>__init__.py
ren day1_1.py day%arg1%_1.py & ren day1_2.py day%arg1%_2.py

cd ..
type day_imports\__init__.py > temp.txt
echo from y%arg2%.Day%arg1% import * > day_imports\__init__.py
type temp.txt >> day_imports\__init__.py
del temp.txt
echo __all__ += ["day%arg1%_1", "day%arg1%_2"]>>day_imports\__init__.py
cd ..\Tools

:End
