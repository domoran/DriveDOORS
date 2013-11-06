REM Locate the DriveDOORS Root Directory
pushd
FOR /F "delims=; tokens=*" %%I in ("%0") DO CD /D "%%~dpI"
:searchRoot 
if exist README.md (set DRIVEDOORSROOT=%CD%) else (cd .. & goto :searchRoot)
popd


SET RUNNER=%DRIVEDOORSROOT%\runner\runDoors.bat
SET SERVERARGS=-a "%DRIVEDOORSROOT%\lib\dxl" -C "int SERVERPORT=2030" -W -b "%DRIVEDOORSROOT%\runner\DxlServer.dxl"
call "%RUNNER%" server1 %SERVERARGS% 
