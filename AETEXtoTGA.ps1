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


$outName = $fileName + ".tga"


[System.IO.File]::WriteAllBytes($outName, $fileBytes[0x38..($fileBytes.length)])