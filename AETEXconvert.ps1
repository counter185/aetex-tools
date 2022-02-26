param(
    [Parameter(Mandatory=$true)][string]$fileName
)

while ($fileName.StartsWith("`"")){
    $fileName = $fileName.Substring(1)
}

while ($fileName.EndsWith("`"")){
    $fileName = $fileName.Substring(0, $fileName.Length-1)
}

$fileBytes = [System.IO.File]::ReadAllBytes($fileName)

$isDDS = $fileBytes[0x34] -eq 0x44 -and $fileBytes[0x35] -eq 0x44 -and $fileBytes[0x36] -eq 0x53

$outName = $fileName
$startIndex = 0x38

if ($isDDS){
    $outName += ".dds"
    $startIndex = 0x34
} else {
    $outName += ".tga"
}



[System.IO.File]::WriteAllBytes($outName, $fileBytes[($startIndex)..($fileBytes.length)])