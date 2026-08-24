# arsivden-geri-don.ps1 — F0 sigortasi
# Restukturizasyon oncesi duzene tek komutla donus.
# Kullanim (AIOS klasorunde): powershell -ExecutionPolicy Bypass -File arsivden-geri-don.ps1
# Not: Eski hook'u geri kurmak icin sonrasinda:
#   uv run --no-project python arsiv/adapters/claude-code/install.py

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$arsiv = Join-Path $root "arsiv"

# Yeni (v3) DECISIONS once yana tasınır - eski log uzerine yazmasin diye.
$v3 = Join-Path $root "DECISIONS.md"
if (Test-Path $v3) {
    Move-Item -LiteralPath $v3 -Destination (Join-Path $arsiv "DECISIONS-v3.md") -Force
    Write-Output "v3 log guvene alindi: arsiv/DECISIONS-v3.md"
}

$items = @(
    "DECISIONS.md", "REJECTED.md", "PROFILE.md", "REQUIREMENTS.md",
    "STATE.md", "vision.md", "VISION-ANALYSIS.md", "CLAUDE.md",
    "PROJECT-INSTRUCTIONS.md", "tools", "hooks", "tests", "adapters",
    ".gate-canary.log"
)
foreach ($i in $items) {
    $src = Join-Path $arsiv $i
    $dst = Join-Path $root $i
    if (Test-Path $src) {
        Move-Item -LiteralPath $src -Destination $dst -Force
        Write-Output "geri geldi: $i"
    } else {
        Write-Output "arsivde yok: $i"
    }
}
Write-Output ""
Write-Output "Eski duzen geri geldi. PLAN.md root'ta kaldi; v3 log arsiv/DECISIONS-v3.md olarak korundu."
Write-Output "Hook geri kurulumu: uv run --no-project python arsiv/adapters/claude-code/install.py"
