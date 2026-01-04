# Pasta temporária
$temp = "$env:TEMP\VZ-Downloader"
if (-Not (Test-Path $temp)) { New-Item -ItemType Directory -Path $temp }

# URLs dos arquivos Python
$installerUrl = "https://raw.githubusercontent.com/Raposix/VZ-Downloader/main/installer.py"
$appUrl       = "https://raw.githubusercontent.com/Raposix/VZ-Downloader/main/app.py"

# Baixa os arquivos
Invoke-WebRequest -Uri $installerUrl -OutFile "$temp\installer.py"
Invoke-WebRequest -Uri $appUrl -OutFile "$temp\app.py"

# Roda os scripts na ordem
python "$temp\installer.py"
python "$temp\app.py"
