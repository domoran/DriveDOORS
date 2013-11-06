@echo off

REM Locate the DriveDOORS Root Directory
pushd
FOR /F "delims=; tokens=*" %%I in ("%0") DO CD /D "%%~dpI"
:searchRoot 
if exist README.md (set DRIVEDOORSROOT=%CD%) else (cd .. & goto :searchRoot)
popd

SET CONF_FILE=%DRIVEDOORSROOT%\config\doors_settings.cfg

if NOT EXIST %CONF_FILE% (
   echo Configuration file %CONF_FILE% was not found. Quitting!
   exit 
)

REM Check parameter
IF "%1"=="" (
   echo USAGE:   run.bat ^<servername^>
   echo.
   echo This file needs to be started with a name configured in %CONF_FILE%
   echo.
   pause
   goto :eof
)

call :findParameterInConfig global. doors
set DOORS=%VALUE%

call :findParameterInConfig "%1." host
set HOST=%VALUE: =%

call :findParameterInConfig "%1." port
set PORT=%VALUE: =%

call :findParameterInConfig "%1." user
set USER=%VALUE: =%

call :findParameterInConfig "%1." pass
set PASS=%VALUE: =%

ECHO Running DXL Server on %PORT%@%HOST%
ECHO Command: "%DOORS%" -J "#include <%DRIVEDOORSROOT%/lib/dxl/DriveDOORS.inc>" -d %PORT%@%HOST% -W %2 %3 %4 %5 %6 %7 %8 -u %USER% -P %PASS%
start "DOORS" "%DOORS%" -J "#include <%DRIVEDOORSROOT%/lib/dxl/DriveDOORS.inc>" -d %PORT%@%HOST% -W %2 %3 %4 %5 %6 %7 %8 -u %USER% -P %PASS%

SET VALUE=
SET DOORS=
SET HOST=
SET PORT=
SET USER=
SET PASS=

goto :eof


REM Subroutine ************ Find Parameter in config *****************
:findParameterInConfig
SET VALUE=

FOR /F "delims=: tokens=1,*" %%i in ('findstr "%~1%~2" %CONF_FILE%') DO (
 SET VALUE=%%j
)

IF "%VALUE%" == "" (
   echo Could not find %2 settings for %1 in %CONF_FILE%. Validate your configuration
   EXIT 2
)

goto :eof 
