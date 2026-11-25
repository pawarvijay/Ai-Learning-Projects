<#
.SYNOPSIS
    Iterates through every leaf pattern and silo project folder in "D:\Ai Learning Projects"
    and initializes each one as an independent, standalone UV Python project
    with its own pyproject.toml, .venv, main.py, and scripts block.
#>

$base = "D:\Ai Learning Projects"

$patternDirs = @(
    # # 1. Prompt Chaining Workflow
    # "$base\1. Prompt Chaining Workflow\Linear-Sequential",
    # "$base\1. Prompt Chaining Workflow\Routing-Classifier",
    # "$base\1. Prompt Chaining Workflow\Parallel-Voting",
    
    # # 2. ReAct Tool Loop (Agent)
    # "$base\2. ReAct Tool Loop (Agent)\Single-Agent-ReAct",
    # "$base\2. ReAct Tool Loop (Agent)\Human-in-the-Loop-Gate",
    # "$base\2. ReAct Tool Loop (Agent)\Dynamic-Memory-ReAct",
    
    # # 3. Evaluator-Optimizer (Reflection)
    # "$base\3. Evaluator-Optimizer (Reflection)\Self-Correction-Loop",
    # "$base\3. Evaluator-Optimizer (Reflection)\Unit-Test-Driven-Loop",
    # "$base\3. Evaluator-Optimizer (Reflection)\Multi-Perspective-Review",
    
    # # 4. Orchestrator-Workers (Multi-Agent)
    # "$base\4. Orchestrator-Workers (Multi-Agent)\Plan-and-Execute",
    # "$base\4. Orchestrator-Workers (Multi-Agent)\Supervisor-Router",
    # "$base\4. Orchestrator-Workers (Multi-Agent)\Swarm-Handoff",
    # "$base\4. Orchestrator-Workers (Multi-Agent)\Map-Reduce-FanOut-FanIn",
    
    # # 5. Combination Variations (Enterprise Real-World)
    # "$base\5. Combination Variations (Enterprise Real-World)\Chain-Wrapped-ReAct",
    # "$base\5. Combination Variations (Enterprise Real-World)\Parallel-ReAct-Swarm",
    # "$base\5. Combination Variations (Enterprise Real-World)\ReAct-with-Reflection",
    # "$base\5. Combination Variations (Enterprise Real-World)\Full-Enterprise-Pipeline",

    # Silos: 01_LangChain
    "$base\Silos\01_LangChain\01_Prompts_and_Templates",
    "$base\Silos\01_LangChain\02_LCEL_Pipelines",
    "$base\Silos\01_LangChain\03_Structured_Output_Parsers",
    "$base\Silos\01_LangChain\04_Memory_and_History",

    # Silos: 02_RAG
    "$base\Silos\02_RAG\01_Chunking_and_Splitting",
    "$base\Silos\02_RAG\02_Embeddings_and_VectorDB",
    "$base\Silos\02_RAG\03_Retrieval_and_Reranking",
    "$base\Silos\02_RAG\04_Hybrid_Search",

    # Silos: 03_MCP
    "$base\Silos\03_MCP\01_Transports_stdio_and_SSE",
    "$base\Silos\03_MCP\02_Primitives_Tools_Resources_Prompts",
    "$base\Silos\03_MCP\03_Server_to_Nodejs_Backend",

    # Silos: 04_Agents (Duplicate Mappings)
    "$base\Silos\04_Agents\01_Single_Agent_ReAct_Duplicate",
    "$base\Silos\04_Agents\02_Plan_and_Execute_Duplicate",
    "$base\Silos\04_Agents\03_Reflection_and_Self_Correction_Duplicate",
    "$base\Silos\04_Agents\04_Multi_Agent_Supervisor_and_Swarm_Duplicate",

    # Silos: 05_LangGraph (Duplicate Mappings)
    "$base\Silos\05_LangGraph\01_Linear_and_Parallel_Workflows_Duplicate",
    "$base\Silos\05_LangGraph\02_Cyclic_State_Machines_Duplicate",
    "$base\Silos\05_LangGraph\03_Human_in_the_Loop_Gate_Duplicate",
    "$base\Silos\05_LangGraph\04_Persistence_Checkpointers_Duplicate",

    # Silos: 06_Enterprise_System (Duplicate Mappings)
    "$base\Silos\06_Enterprise_System\01_Full_Enterprise_Pipeline_Duplicate"
)

$commonEnv = "D:\deleteme\McpTest\.env"
$total = $patternDirs.Count

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Initializing $total Standalone UV Projects (Patterns + All Silos)..." -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

$count = 0
foreach ($dir in $patternDirs) {
    $count++
    $folderName = Split-Path $dir -Leaf
    $parentCategory = Split-Path (Split-Path $dir) -Leaf
    
    # Create valid python package name (lowercase, no spaces, hyphens)
    $cleanCategory = ($parentCategory -replace '^[0-9]+\.\s*', '') -replace '[^a-zA-Z0-9]', '-'
    $cleanFolder = $folderName -replace '[^a-zA-Z0-9]', '-'
    $pkgName = "$cleanCategory-$cleanFolder".ToLower() -replace '-+', '-'

    Write-Host "`n[$count/$total] Initializing: $parentCategory -> $folderName" -ForegroundColor Cyan

    # 1. Ensure Directory Exists
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }

    Set-Location $dir

    # 2. Initialize standalone uv project if pyproject.toml does not exist
    if (-not (Test-Path (Join-Path $dir "pyproject.toml"))) {
        uv init --name $pkgName --no-readme --python "3.14"
        
        # 3. Add core dependencies into this project's pyproject.toml
        uv add langgraph langchain-core langchain-google-genai langchain-mcp-adapters mcp python-dotenv pydantic
    }

    # 4. Create standard main.py entrypoint if missing
    $mainFile = Join-Path $dir "main.py"
    if (-not (Test-Path $mainFile)) {
        $mainContent = @"
import os
from pathlib import Path
from dotenv import load_dotenv

# Load API key
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

def main():
    print("=" * 60)
    print("Running Project: $folderName")
    print("Category:        $parentCategory")
    print("=" * 60)

if __name__ == "__main__":
    main()
"@
        Set-Content -Path $mainFile -Value $mainContent -Encoding utf8
    }

    # 5. Add custom [project.scripts] to this project's pyproject.toml
    $tomlPath = Join-Path $dir "pyproject.toml"
    if (Test-Path $tomlPath) {
        $tomlContent = Get-Content $tomlPath -Raw
        if ($tomlContent -notmatch "\[project\.scripts\]") {
            $scriptsBlock = @"

[project.scripts]
start = "main:main"
run = "main:main"
$folderName = "main:main"
"@
            Add-Content -Path $tomlPath -Value $scriptsBlock -Encoding utf8
        }
    }

    # 6. Copy .env with API keys into this individual project
    if (Test-Path $commonEnv) {
        Copy-Item $commonEnv (Join-Path $dir ".env") -Force
    }
}

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " Complete! All $total folders are now independent projects." -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
