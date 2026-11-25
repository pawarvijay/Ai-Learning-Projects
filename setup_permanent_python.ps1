<#
.SYNOPSIS
    Permanently enables 'python' and 'pip' commands in PowerShell backed by 'uv'.
.DESCRIPTION
    Creates or updates your PowerShell profile so every new PowerShell window
    can run 'python' and 'pip' directly without typing 'uv run'.
#>

[CmdletBinding()]
param()

$profilePath = $PROFILE
$profileDir = Split-Path $profilePath -Parent

# Ensure profile directory exists
if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
}

$blockComment = "# --- UV Python & Pip Permanent Aliases ---"
$shimContent = @"

$blockComment
function python { & uv run python `$args }
function pip { & uv pip `$args }
# --- End UV Aliases ---
"@

# Read existing profile content if present
$existing = if (Test-Path $profilePath) { Get-Content -Path $profilePath -Raw } else { "" }

if ($existing -notmatch [regex]::Escape($blockComment)) {
    Add-Content -Path $profilePath -Value $shimContent -Encoding utf8
    Write-Host "[SUCCESS] Added 'python' and 'pip' aliases to your PowerShell profile:" -ForegroundColor Green
    Write-Host "          $profilePath" -ForegroundColor Cyan
} else {
    Write-Host "[OK] 'python' and 'pip' aliases are already configured in:" -ForegroundColor Yellow
    Write-Host "     $profilePath" -ForegroundColor Cyan
}

Write-Host "`nTo activate in your CURRENT terminal window, run:" -ForegroundColor Green
Write-Host "    . `$PROFILE" -ForegroundColor White
Write-Host "All future terminal windows will have them enabled automatically." -ForegroundColor Green
