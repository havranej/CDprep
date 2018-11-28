# CDprep
Preparation of files for CDPro

**Manual check of output files is highly recommended**

```
> py CDprep.py -h
usage: CDprep.py [-h] [-o outfile] [-p c M n d] [-t] [-f] [-n] [infile]

Preparation of files for CDPro. Converts units to molar ellipticity and may
produce some plots in the process.

positional arguments:
  infile      Input file. Will be asked for, if not specified.

optional arguments:
  -h, --help  show this help message and exit
  -o outfile  Output file. Set to default, if not specified.
  -p c M n d  Mesurement parameters - mass concentration [g/l], molar mass
              [g/mol], number of amino acids, and cuvette light path [cm].
              Will be asked for, if not specified.
  -t          Plot theta in the process of conversion.
  -f          Plot phi in the process of conversion.
  -n          Do not write output file. Might be useful for plotting.

Written by Jan Havránek in 2018
```
