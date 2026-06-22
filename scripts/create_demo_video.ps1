param(
    [string]$FfmpegPath = ""
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$mediaDir = Join-Path $repoRoot "media"
$outputPath = Join-Path $mediaDir "evidencegraph_demo.mp4"
$workDir = Join-Path $mediaDir ".evidencegraph-video-build"

function Find-Ffmpeg {
    param([string]$RequestedPath)
    if ($RequestedPath) {
        $resolved = Resolve-Path -LiteralPath $RequestedPath -ErrorAction SilentlyContinue
        if ($resolved) { return $resolved.Path }
        throw "The ffmpeg path does not exist: $RequestedPath"
    }
    $local = Join-Path $repoRoot "ffmpeg.exe"
    if (Test-Path -LiteralPath $local) { return $local }
    $command = Get-Command ffmpeg -ErrorAction SilentlyContinue
    if ($command) { return $command.Source }
    return $null
}

function ConvertTo-FilterPath {
    param([string]$Path)
    return $Path.Replace("\", "/").Replace(":", "\:").Replace("'", "\'")
}

$ffmpeg = Find-Ffmpeg -RequestedPath $FfmpegPath
if (-not $ffmpeg) {
    Write-Error "ffmpeg was not found. Pass -FfmpegPath with the exact executable path. Nothing was installed."
    exit 1
}

$fontPath = Join-Path $env:WINDIR "Fonts\segoeui.ttf"
$boldFontPath = Join-Path $env:WINDIR "Fonts\segoeuib.ttf"
if (-not (Test-Path -LiteralPath $fontPath)) { $fontPath = Join-Path $env:WINDIR "Fonts\arial.ttf" }
if (-not (Test-Path -LiteralPath $boldFontPath)) { $boldFontPath = $fontPath }

$scenes = @(
    @{
        Duration = 12; Color = "0x13271f"; Kicker = "GENLAYER BUILDER TOOL";
        Title = "EvidenceGraph";
        Body = "Better evidence in. Better reasoning out."
    },
    @{
        Duration = 15; Color = "0x263b34"; Kicker = "THE PROBLEM";
        Title = "Raw evidence is messy";
        Body = "GenLayer apps need reliable evidence.`nBut raw claims, links, screenshots, and logs arrive`nscattered, vague, and difficult to verify."
    },
    @{
        Duration = 15; Color = "0x174f3c"; Kicker = "THE SOLUTION";
        Title = "One structured evidence package";
        Body = "EvidenceGraph turns claims and public URLs into`nquality scores, missing-proof detection, manipulation risk,`nrecommendations, and contract-ready JSON."
    },
    @{
        Duration = 16; Color = "0x482b28"; Kicker = "WEAK SELF-CLAIM";
        Title = "31 / 100  |  High manipulation risk";
        Body = "Source quality: WEAK`nVerdict: HIGH_MANIPULATION_RISK`n`nMissing: independent source, timestamped proof,`nand at least two evidence items."
    },
    @{
        Duration = 16; Color = "0x164a38"; Kicker = "STRONG MILESTONE EVIDENCE";
        Title = "100 / 100  |  GenLayer ready";
        Body = "Source quality: STRONG   |   Manipulation risk: LOW`n`nPublic repository + timestamped release + documentation`n+ demo video + reproducible test result."
    },
    @{
        Duration = 16; Color = "0x243a46"; Kicker = "WHY GENLAYER";
        Title = "Evidence needs judgment";
        Body = "Milestones, grants, disputes, and agent SLAs require`nsubjective judgment, natural-language understanding,`nand reasoning across unstructured web inputs."
    },
    @{
        Duration = 15; Color = "0x13271f"; Kicker = "THE QUALITY LAYER BEFORE JUDGMENT";
        Title = "EvidenceGraph";
        Body = "Evidence preparation and quality scoring`nfor GenLayer Intelligent Contracts.`n`nNot escrow. Not a bounty. Not a court."
    }
)

if (Test-Path -LiteralPath $workDir) {
    $resolvedWork = (Resolve-Path -LiteralPath $workDir).Path
    if (-not $resolvedWork.StartsWith($mediaDir, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to clear a build directory outside media: $resolvedWork"
    }
    Remove-Item -LiteralPath $workDir -Recurse -Force
}
New-Item -ItemType Directory -Path $workDir | Out-Null

$fontFilter = ConvertTo-FilterPath $fontPath
$boldFontFilter = ConvertTo-FilterPath $boldFontPath
$segmentPaths = @()
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

try {
    for ($index = 0; $index -lt $scenes.Count; $index++) {
        $scene = $scenes[$index]
        $sceneNumber = $index + 1
        $prefix = "{0:D2}" -f $sceneNumber
        $kickerFile = Join-Path $workDir "$prefix-kicker.txt"
        $titleFile = Join-Path $workDir "$prefix-title.txt"
        $bodyFile = Join-Path $workDir "$prefix-body.txt"
        $segmentPath = Join-Path $workDir "$prefix-scene.mp4"
        [System.IO.File]::WriteAllText($kickerFile, $scene.Kicker, $utf8NoBom)
        [System.IO.File]::WriteAllText($titleFile, $scene.Title, $utf8NoBom)
        [System.IO.File]::WriteAllText($bodyFile, $scene.Body, $utf8NoBom)

        $kickerFilter = ConvertTo-FilterPath $kickerFile
        $titleFilter = ConvertTo-FilterPath $titleFile
        $bodyFilter = ConvertTo-FilterPath $bodyFile
        $duration = [int]$scene.Duration
        $fadeOutStart = $duration - 1
        $progressWidth = [math]::Round(1520 * ($sceneNumber / $scenes.Count))
        $counter = "$sceneNumber / $($scenes.Count)"

        $filter = @(
            "drawbox=x=200:y=185:w=70:h=5:color=0xE1A53A:t=fill",
            "drawtext=fontfile='$boldFontFilter':textfile='$kickerFilter':fontcolor=0x9CCDB2:fontsize=28:x=200:y=220",
            "drawtext=fontfile='$boldFontFilter':textfile='$titleFilter':fontcolor=0xEEF5F0:fontsize=76:x=200:y=330",
            "drawtext=fontfile='$fontFilter':textfile='$bodyFilter':fontcolor=0xC4D2CB:fontsize=38:line_spacing=18:x=200:y=500",
            "drawtext=fontfile='$fontFilter':text='$counter':fontcolor=0x8FA39A:fontsize=24:x=1670:y=955",
            "drawbox=x=200:y=970:w=1520:h=4:color=0xFFFFFF@0.15:t=fill",
            "drawbox=x=200:y=970:w=${progressWidth}:h=4:color=0xE1A53A:t=fill",
            "fade=t=in:st=0:d=0.8",
            "fade=t=out:st=${fadeOutStart}:d=1",
            "format=yuv420p"
        ) -join ","

        Write-Host "Rendering scene $sceneNumber of $($scenes.Count)..."
        & $ffmpeg -hide_banner -loglevel error -y -f lavfi -i "color=c=$($scene.Color):s=1920x1080:r=30:d=$duration" -vf $filter -t $duration -an -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p $segmentPath
        if ($LASTEXITCODE -ne 0) { throw "ffmpeg failed while rendering scene $sceneNumber." }
        $segmentPaths += $segmentPath
    }

    $concatFile = Join-Path $workDir "segments.txt"
    $concatLines = $segmentPaths | ForEach-Object { "file '$($_.Replace("'", "''"))'" }
    Set-Content -LiteralPath $concatFile -Value $concatLines -Encoding ascii

    Write-Host "Combining scenes into a 105-second MP4..."
    & $ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i $concatFile -an -c copy -movflags +faststart $outputPath
    if ($LASTEXITCODE -ne 0) { throw "ffmpeg could not combine the rendered scenes." }
}
catch {
    Write-Error "Demo video generation failed: $($_.Exception.Message)"
    exit 1
}
finally {
    if (Test-Path -LiteralPath $workDir) { Remove-Item -LiteralPath $workDir -Recurse -Force }
}

Write-Host "Created $outputPath"
