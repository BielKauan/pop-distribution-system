
param(
    [Parameter(Mandatory = $true)]
    [string]$ApiUrl
)

$ErrorActionPreference = "Stop"

# Caminho do Desktop público
$destination = Join-Path $env:PUBLIC "Desktop\POPs"

# Diretório temporário exclusivo para esta atualização
$tempRoot = Join-Path $env:TEMP (
    "POP-Distribution-" + [guid]::NewGuid().ToString("N")
)

$zipPath = Join-Path $tempRoot "POPs.zip"
$extractPath = Join-Path $tempRoot "extracted"
$downloadedPops = Join-Path $extractPath "POPs"

$backupPath = "$destination.backup"

try {
    New-Item -ItemType Directory -Path $tempRoot -Force |
        Out-Null

    # 1. Baixar os documentos do servidor
    Write-Host "Baixando os POPs..."

    Invoke-WebRequest `
        -Uri $ApiUrl `
        -OutFile $zipPath

    # 2. Extrair os documentos
    Write-Host "Extraindo os documentos..."

    Expand-Archive `
        -LiteralPath $zipPath `
        -DestinationPath $extractPath `
        -Force

    # 3. Validar o conteúdo recebido
    if (-not (Test-Path $downloadedPops -PathType Container)) {
        throw "O pacote recebido não contém a pasta POPs."
    }

    $receivedFiles = Get-ChildItem $downloadedPops -Recurse -File

    if (-not $receivedFiles) {
        throw "A pasta POPs recebida está vazia."
    }

    # 4. Preservar a versão anterior
    if (Test-Path $destination) {

        if (Test-Path $backupPath) {
            Remove-Item $backupPath -Recurse -Force
        }

        Move-Item -LiteralPath $destination -Destination $backupPath
    }

    try {
        # 5. Instalar a nova versão
        Move-Item -LiteralPath $downloadedPops -Destination $destination
    }
    catch {
        # Restaurar a versão anterior se a instalação falhar
        if (Test-Path $backupPath) {
            Move-Item -LiteralPath $backupPath -Destination $destination
        }

        throw
    }

    # 6. Remover o backup após a atualização bem-sucedida
    if (Test-Path $backupPath) {
        Remove-Item $backupPath -Recurse -Force
    }

    Write-Host "Atualização dos POPs concluída!" -ForegroundColor Green
}
finally {
    # Limpar arquivos temporários
    if (Test-Path $tempRoot) {
        Remove-Item $tempRoot -Recurse -Force
    }
}
