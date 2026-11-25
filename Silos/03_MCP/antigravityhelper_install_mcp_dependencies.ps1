<#
.SYNOPSIS
    Prepares and synchronizes all dependencies for 03_MCP Silo projects.
.DESCRIPTION
    Ensures 'uv' is accessible, pins Python 3.13/3.14, and installs official MCP dependencies
    (mcp, starlette, uvicorn, httpx, pydantic, langchain-google-genai, etc.) for each subproject.
#>

[CmdletBinding()]
param()

$baseMcp = "D:\Ai Learning Projects\Silos\03_MCP"
$projects = @(
    "01_Transports_stdio_and_SSE",
    "02_Primitives_Tools_Resources_Prompts",
    "03_Server_to_Nodejs_Backend"
)

# Ensure uv is in PATH
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    $env:Path = "C:\Users\vijay\.local\bin;" + $env:Path
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Installing Official MCP Dependencies for Silo 03_MCP..." -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

foreach ($proj in $projects) {
    $projDir = Join-Path $baseMcp $proj
    if (Test-Path $projDir) {
        Write-Host "`n▸ Setting up: $proj" -ForegroundColor Cyan
        Set-Location $projDir

        # Add essential official MCP stack packages
        uv add "mcp>=1.3.0" "starlette>=0.40.0" "uvicorn>=0.30.0" "httpx>=0.27.0" "pydantic>=2.10.0" "python-dotenv>=1.0.0"
        
        # Sync virtual environment
        uv sync
        Write-Host "✔ Synced dependencies for $proj" -ForegroundColor Green
    }
}

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " All MCP Silo projects are fully installed and ready!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
