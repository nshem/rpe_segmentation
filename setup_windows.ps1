# Activate the virtual environment
.\venv\Scripts\activate.ps1

# Check if the virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    python -m venv .\venv
    . .\venv\Scripts\Activate
    Write-Output "Python venv should be activated now, please run the script again."
    exit 1
}

# Check if Python version is between 3.10 and 3.12
$pythonVersionOutput = & python --version 2>&1
$pythonVersion = $pythonVersionOutput -replace "Python ", ""
$versionParts = $pythonVersion.Split('.')

$major = [int]$versionParts[0]
$minor = [int]$versionParts[1]

if (($major -eq 3 -and $minor -ge 10) -and ($major -eq 3 -and $minor -lt 12)) {
    Write-Output "Python version $pythonVersion is compatible."
} else {
    Write-Output "Python version $pythonVersion is not compatible. Required: >=3.10 and <3.12"
}

# Install dependencies
pip install -r requirements.txt

# Download the weights if the directory doesn't exist
$weightsPath = Join-Path (Get-Location) "weights"
if (-not (Test-Path -Path $weightsPath)) {
    Write-Output "Downloading the weights"
    New-Item -ItemType Directory -Path $weightsPath | Out-Null
    Invoke-WebRequest -Uri "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth" -OutFile (Join-Path $weightsPath "sam_vit_h_4b8939.pth")
}

# Run the main script
python -m src.main