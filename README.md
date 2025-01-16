# atrophy-tools

Some tools I wrote for Atrophy Engine formats.

## aetex-tool

Python script to unwrap Atrophy Engine's AETEX texture files into their original formats (DDS, TGA, GXT and ASTC).

### Usage

```
python aetex_tool.py <file name 1> [file name 2] [...]
```

## aeshader-tool

Python script to wrap and unwrap Windows BIT.TRIP RUNNER AESHADER files into HLSL. Probably will not work with other games or versions.

### Usage
- Unwrap:
```
python aeshader_tool.py <file name>.aeshader
```
- Wrap:
```
python aeshader_tool.py <file name>.fx
```