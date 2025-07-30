# Change this to the full path of your Python interpreter and script
$pythonPath = "C:\Users\WengYinHo\AppData\Local\Programs\Python\Python312\python.exe"
$scriptPath = "C:\Users\WengYinHo\Downloads\Remote\Main3.py"

# Run the Python script
Start-Process -FilePath $pythonPath -ArgumentList "`"$scriptPath`"" -NoNewWindow -Wait
