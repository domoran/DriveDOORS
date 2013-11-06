REM Locate the DriveDOORS Root Directory
pushd
FOR /F "delims=; tokens=*" %%I in ("%0") DO CD /D "%%~dpI"
:searchRoot 
if exist README.md (set DRIVEDOORSROOT=%CD%) else (cd .. & goto :searchRoot)
popd


SET RUNNER=%DRIVEDOORSROOT%\runner\runServer.bat
call "%RUNNER%" server1 -a "%DRIVEDOORSROOT%\lib\dxl"
