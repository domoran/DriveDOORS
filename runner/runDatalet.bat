FOR /F "delims=*" %%i in ("%0") do SET DRIVEDOORSROOT=%%~dpi..
SET NETCAT=%DRIVEDOORSROOT%\runner\netcat\nc

echo print ^"Hallo^" //END_OF_PROGRAM | "%NETCAT%" -w1 localhost 2030
pause 