@if (@X)==(@Y) @end /* harmless hybrid line that begins a JScript comment

::: Batch part ::::
@echo off
cscript //nologo //e:JScript "%~f0" "%*"
exit /b

*** JScript part ***/
if (WScript.Arguments.Named.Exists("n")) {
  WScript.StdOut.Writeline(WScript.Arguments.Unnamed(0)); 
  WScript.StdOut.WriteLine(eval(WScript.Arguments.Unnamed(0)));
} else {
  WScript.StdOut.Writeline(WScript.Arguments.Unnamed(0)); 
  WScript.StdOut.Write(eval(WScript.Arguments.Unnamed(0)));
}