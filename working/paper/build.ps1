# build.ps1 - Compile SPECTRA NeurIPS 2026 paper
# Usage: .\build.ps1
# Output: build/main.pdf

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$buildDir = "$root\build"

# Ensure build dir exists
if (-not (Test-Path $buildDir)) {
    New-Item -ItemType Directory -Path $buildDir | Out-Null
}

# Clean previous build artifacts
Get-ChildItem "$buildDir\*" -ErrorAction SilentlyContinue | Remove-Item -Force

# Clean any leftover in-place artifacts from previous runs
Get-ChildItem "$root\main.aux","$root\main.bbl","$root\main.blg","$root\main.log","$root\main.out","$root\main.synctex.gz","$root\main.pdf" -ErrorAction SilentlyContinue | Remove-Item -Force

# Suppress MiKTeX first-run update warning
$env:MIKTEX_WARN_MIKTEX_NO_UPDATE = "1"

# Add NeurIPS formatting dir to TEXINPUTS so .sty is found without copying
$neuripsDir = "$root\Formatting_Instructions_For_NeurIPS_2026"
$env:TEXINPUTS = "$neuripsDir;"

# MiKTeX paths (explicit to avoid TinyTeX shadowing)
$miktexBin = "C:\Users\Hellx\AppData\Local\Programs\MiKTeX\miktex\bin\x64"
$pdflatex = "& `"$miktexBin\pdflatex.exe`" --enable-installer -interaction=nonstopmode -synctex=1 -output-directory=`"$buildDir`" main.tex"
$bibtex   = "& `"$miktexBin\bibtex.exe`" `"$buildDir\main`""

$ErrorActionPreference = "Continue"

Write-Host "=== Pass 1: pdflatex ===" -ForegroundColor Cyan
Invoke-Expression $pdflatex 2>&1 | Where-Object { $_ -notmatch "major issue|MIKTEX_WARN" } | Select-Object -Last 5

Write-Host "=== Pass 2: bibtex ===" -ForegroundColor Cyan
Invoke-Expression $bibtex 2>&1 | Where-Object { $_ -notmatch "major issue|MIKTEX_WARN" } | Select-Object -Last 5

Write-Host "=== Pass 3: pdflatex ===" -ForegroundColor Cyan
Invoke-Expression $pdflatex 2>&1 | Where-Object { $_ -notmatch "major issue|MIKTEX_WARN" } | Select-Object -Last 5

Write-Host "=== Pass 4: pdflatex ===" -ForegroundColor Cyan
Invoke-Expression $pdflatex 2>&1 | Where-Object { $_ -notmatch "major issue|MIKTEX_WARN" } | Select-Object -Last 5

$ErrorActionPreference = "Stop"

if (Test-Path "$buildDir\main.pdf") {
    Write-Host ""
    Write-Host "Build succeeded: build\main.pdf" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Build FAILED -- no PDF produced. Check build\main.log for errors." -ForegroundColor Red
    exit 1
}
