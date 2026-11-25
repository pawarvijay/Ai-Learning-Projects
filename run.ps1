<#
.SYNOPSIS
    Windows PowerShell equivalent of run.sh for rx-planner.
.DESCRIPTION
    Manages local PostgreSQL, FastAPI backend engine, and Vite/React UI on Windows.
    Usage:
        .\run.ps1          # Start everything (DB, Engine in background, UI in foreground)
        .\run.ps1 db       # Set up / reset database only
        .\run.ps1 engine   # Run engine only
        .\run.ps1 ui       # Run UI only
        .\run.ps1 stop     # Stop engine (port 6002) and UI (port 5175)
#>

[CmdletBinding()]
param(
    [ValidateSet("all", "db", "engine", "ui", "stop")]
    [string]$Command = "all"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

$ENGINE_PORT = 6002
$UI_PORT = 5175
$DB_NAME = "rx_planner"
$DB_USER = "rxplanner"
$DB_PASS = "rxplanner_local_dev"

function Log-Info([string]$msg) {
    Write-Host "▸ $msg" -ForegroundColor Cyan
}

function Log-Error([string]$msg) {
    Write-Host "✗ $msg" -ForegroundColor Red
}

function Stop-PortProcess([int]$port) {
    $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($conns) {
        $pids = $conns | Select-Object -ExpandProperty OwningProcess -Unique
        foreach ($p in $pids) {
            try {
                Stop-Process -Id $p -Force -ErrorAction SilentlyContinue
            } catch {}
        }
    }
}

function Start-Postgres {
    # Check if PostgreSQL service is running or port 5432 is responding
    $listening = Test-NetConnection -ComputerName 127.0.0.1 -Port 5432 -InformationLevel Quiet -WarningAction SilentlyContinue
    if (-not $listening) {
        Log-Info "Attempting to start postgresql Windows service..."
        $svc = Get-Service -Name "postgresql*" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($svc) {
            Start-Service $svc.Name
            Start-Sleep -Seconds 2
        } else {
            Log-Error "PostgreSQL service not found. Please ensure Postgres service is running on 127.0.0.1:5432."
            exit 1
        }
    }
    Log-Info "PostgreSQL ready on port 5432."
}

function Setup-Db {
    Start-Postgres

    # Create role if not exists
    $roleExists = psql -U postgres -d postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" 2>$null
    if ($roleExists -notmatch "1") {
        Log-Info "creating role $DB_USER"
        psql -U postgres -d postgres -qc "CREATE ROLE $DB_USER LOGIN PASSWORD '$DB_PASS'"
    }

    # Create database if not exists
    $dbExists = psql -U postgres -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" 2>$null
    if ($dbExists -notmatch "1") {
        Log-Info "creating database $DB_NAME"
        createdb -U postgres -O "$DB_USER" "$DB_NAME"
    }

    Log-Info "applying schema"
    psql -U postgres -q -d "$DB_NAME" -v ON_ERROR_STOP=1 -f "rx-planner-engine\sql\schema.sql"

    Log-Info "seeding"
    psql -U postgres -q -d "$DB_NAME" -v ON_ERROR_STOP=1 -f "rx-planner-engine\sql\seed.sql"

    $grants = @"
GRANT USAGE ON SCHEMA rx_planner TO $DB_USER;
GRANT ALL ON ALL TABLES IN SCHEMA rx_planner TO $DB_USER;
GRANT ALL ON ALL SEQUENCES IN SCHEMA rx_planner TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA rx_planner GRANT ALL ON TABLES TO $DB_USER;
"@
    psql -U postgres -q -d "$DB_NAME" -c $grants

    $medCount = (psql -U postgres -tAc "SELECT count(*) FROM rx_planner.medicines" -d $DB_NAME).Trim()
    $listingCount = (psql -U postgres -tAc "SELECT count(*) FROM rx_planner.platform_listings" -d $DB_NAME).Trim()
    Log-Info "database ready ($medCount medicines, $listingCount listings)"
}

function Ensure-Venv {
    $venvDir = "rx-planner-engine\.venv"
    if (-not (Test-Path $venvDir)) {
        Log-Info "creating engine venv"
        python -m venv $venvDir
        $venvPip = Join-Path $venvDir "Scripts\pip.exe"
        & $venvPip install -q --upgrade pip
        & $venvPip install -q -r "rx-planner-engine\requirements.txt"
    }
}

function Start-Engine {
    Ensure-Venv
    Stop-PortProcess $ENGINE_PORT
    Log-Info "engine  → http://127.0.0.1:$ENGINE_PORT  (docs at /docs)"
    $venvPython = (Join-Path (Get-Location) "rx-planner-engine\.venv\Scripts\python.exe")
    Push-Location "rx-planner-engine"
    try {
        & $venvPython -m uvicorn app.main:app --host 127.0.0.1 --port $ENGINE_PORT --reload
    } finally {
        Pop-Location
    }
}

function Start-Ui {
    if (-not (Test-Path "rx-planner-ui\node_modules")) {
        Log-Info "installing UI dependencies"
        Push-Location "rx-planner-ui"
        npm install
        Pop-Location
    }
    Log-Info "ui      → http://localhost:$UI_PORT"
    Push-Location "rx-planner-ui"
    try {
        npm run dev
    } finally {
        Pop-Location
    }
}

function Stop-All {
    Stop-PortProcess $ENGINE_PORT
    Stop-PortProcess $UI_PORT
    Log-Info "stopped engine and ui"
}

# --- Command Router ---
switch ($Command) {
    "db" {
        Setup-Db
    }
    "engine" {
        Setup-Db
        Start-Engine
    }
    "ui" {
        Start-Ui
    }
    "stop" {
        Stop-All
    }
    "all" {
        Setup-Db
        Ensure-Venv
        Stop-PortProcess $ENGINE_PORT
        
        Log-Info "Starting engine background process on port $ENGINE_PORT..."
        $venvPython = (Join-Path (Get-Location) "rx-planner-engine\.venv\Scripts\python.exe")
        $engineJob = Start-Process -FilePath $venvPython -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port $ENGINE_PORT --reload" -WorkingDirectory (Join-Path (Get-Location) "rx-planner-engine") -PassThru

        # Wait for engine health endpoint
        for ($i = 0; $i -lt 40; $i++) {
            Start-Sleep -Milliseconds 500
            try {
                $res = Invoke-WebRequest -Uri "http://127.0.0.1:$ENGINE_PORT/health" -UseBasicParsing -TimeoutSec 1 -ErrorAction SilentlyContinue
                if ($res.StatusCode -eq 200) { break }
            } catch {}
        }

        Log-Info "engine  → http://127.0.0.1:$ENGINE_PORT  (docs at /docs)"
        try {
            Start-Ui
        } finally {
            if ($engineJob -and -not $engineJob.HasExited) {
                Stop-Process -Id $engineJob.Id -Force -ErrorAction SilentlyContinue
            }
            Stop-PortProcess $ENGINE_PORT
        }
    }
}
