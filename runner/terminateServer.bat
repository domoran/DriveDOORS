REM Locate the DriveDOORS Root Directory
pushd
FOR /F "delims=; tokens=*" %%I in ("%0") DO CD /D "%%~dpI"
:searchRoot 
if exist README.md (set DRIVEDOORSROOT=%CD%) else (cd .. & goto :searchRoot)
popd

SET NETCAT=%DRIVEDOORSROOT%\runner\netcat\nc

echo //TERMINATE_SERVER | "%NETCAT%" -w1 localhost 2030
pause
