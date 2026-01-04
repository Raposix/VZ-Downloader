# Pasta fixa para o repositório
$folder = "C:\VZ-Downloader"

# Se a pasta não existir, baixa e descompacta o repositório
if (-Not (Test-Path $folder)) {
    Write-Host "Baixando VZ-Downloader..."
    $zip = "$env:TEMP\VZ-Downloader.zip"
    Invoke-WebRequest -Uri "https://github.com/Raposix/VZ-Downloader/archive/refs/heads/main.zip" -OutFile $zip
    Expand-Archive -Path $zip -DestinationPath "C:\"
    Rename-Item "C:\VZ-Downloader-main" "C:\VZ-Downloader"
    Remove-Item $zip
}

# Vai para a pasta do repositório
Set-Location $folder

# Roda o installer
Write-Host "Rodando installer.py..."
py -3 installer.py

# Roda o app
Write-Host "Rodando app.py..."
py -3 app.py
