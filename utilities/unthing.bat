:: cd /D "%~dp0"
:: "%~dp0": directory of current batch file.
:: /D: also change drive.
:: commented so it can be used on a file in current working directory
py -3 "%~dp0\unthing" %*