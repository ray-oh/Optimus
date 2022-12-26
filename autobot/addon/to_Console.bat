rem cd\
query user %USERNAME%
for /f "skip=1 tokens=3" %%s in ('query user %USERNAME%') do (
  echo %%s  
)
rem %windir%\System32\tscon.exe %%s /dest:console