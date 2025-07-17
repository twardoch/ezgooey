# this_file: scripts/install.ps1
# Easy installation script for ezgooey (Windows PowerShell)

param(
    [string]$PythonCmd = "python"
)

Write-Host "🚀 Installing ezgooey..." -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = & $PythonCmd --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python 3 is required but not found. Please install Python 3.8 or later." -ForegroundColor Red
    exit 1
}

# Parse Python version
$versionMatch = [regex]::Match($pythonVersion, "Python (\d+)\.(\d+)")
if ($versionMatch.Success) {
    $majorVersion = [int]$versionMatch.Groups[1].Value
    $minorVersion = [int]$versionMatch.Groups[2].Value
    
    if ($majorVersion -lt 3 -or ($majorVersion -eq 3 -and $minorVersion -lt 8)) {
        Write-Host "❌ Python 3.8 or later is required. Found: $pythonVersion" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "❌ Could not parse Python version: $pythonVersion" -ForegroundColor Red
    exit 1
}

Write-Host "✅ $pythonVersion found" -ForegroundColor Green

# Install ezgooey
Write-Host "📦 Installing ezgooey package..." -ForegroundColor Yellow
& $PythonCmd -m pip install --user ezgooey

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Installation failed" -ForegroundColor Red
    exit 1
}

# Verify installation
Write-Host "🔍 Verifying installation..." -ForegroundColor Yellow
$verifyScript = @"
import ezgooey
print(f'✅ ezgooey {ezgooey.__version__} installed successfully')

# Test basic functionality
from ezgooey.ez import ezgooey, ArgumentParser
import ezgooey.logging as logging

print('✅ All modules imported successfully')
"@

& $PythonCmd -c $verifyScript

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Installation verification failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 ezgooey installation completed!" -ForegroundColor Green
Write-Host ""
Write-Host "📚 Quick start:" -ForegroundColor Cyan
Write-Host "  1. Create a Python script with argparse" -ForegroundColor White
Write-Host "  2. Add @ezgooey decorator to your argument parser function" -ForegroundColor White
Write-Host "  3. Run without arguments for GUI, with arguments for CLI" -ForegroundColor White
Write-Host ""
Write-Host "📖 Documentation: https://github.com/twardoch/ezgooey" -ForegroundColor Cyan
Write-Host "🐛 Issues: https://github.com/twardoch/ezgooey/issues" -ForegroundColor Cyan
Write-Host ""
Write-Host "Example usage:" -ForegroundColor Yellow
Write-Host "  python -c `"from ezgooey.ez import ezgooey, ArgumentParser; print('Ready to use!')`"" -ForegroundColor White