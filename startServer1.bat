FOR /F "delims=; tokens=*" %%i in ("%0") do SET DRIVEDOORSROOT=%%~dpi

SET RUNNER=%DRIVEDOORSROOT%runner\runServer.bat
call "%RUNNER%" server1
pause