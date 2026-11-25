# Run this script to enable 'python' and 'pip' in your current terminal session:
# Usage: . .\enable_python.ps1

function python { & uv run python $args }
function pip { & uv pip $args }

Write-Host "Python and Pip shortcuts enabled for this session!" -ForegroundColor Green
Write-Host "You can now run: python <file.py> and pip <command>" -ForegroundColor Cyan
