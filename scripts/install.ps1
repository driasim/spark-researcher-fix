param(
    [string]$PackageSpec = "git+https://github.com/vibeforge1111/spark-researcher.git",
    [string]$AppName = "spark-researcher",
    [string]$PythonCommand = "",
    [switch]$SkipEnsurePath
)

$ErrorActionPreference = "Stop"

function Resolve-PythonCommand {
    param([string]$Requested)
    if ($Requested) {
        return $Requested
    }
    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) {
        return "py"
    }
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        return "python"
    }
    throw "Python 3.10+ is required."
}

$python = Resolve-PythonCommand -Requested $PythonCommand

& $python -m pip install --user --upgrade pip pipx
if (-not $SkipEnsurePath) {
    & $python -m pipx ensurepath | Out-Host
}

try {
    & $python -m pipx uninstall $AppName | Out-Host
} catch {
}

& $python -m pipx install --python $python $PackageSpec | Out-Host

Write-Host ""
Write-Host "Installed $AppName."
if (-not $SkipEnsurePath) {
    Write-Host "If the command is not available yet, restart the terminal so PATH updates from pipx ensurepath take effect."
}
Write-Host "To generate a runnable demo without cloning the repo:"
Write-Host "  $AppName init --path spark-demo --preset toy --project-name spark-demo"
