# CDprep
Preparation of files for CDPro. 

**Manual check of output files is highly recommended**

```
> py CDprep.py -h
usage: CDprep.py [-h] [-i infile] [-o outfile] [-b file] [-p c M n d] [-t]
                 [-f] [-l title] [-q] [-c IBasis] [-d title] [-n]

Preparation of files for CDPro. Converts units to molar ellipticity and may
produce some plots in the process.

optional arguments:
  -h, --help  show this help message and exit
  -i infile   Input file. Will be asked for, if not specified.
  -o outfile  Output file. Set to default, if not specified.
  -b file     Batch file. Collides with some of the other console arguments
              (-i, -o, -p, -q and -n).
  -p c M n d  Mesurement parameters - mass concentration [g/l], molar mass
              [g/mol], number of amino acids, and cuvette light path [cm].
              Will be asked for, if not specified.

plotting:
  -t          Plot theta in the process of conversion.
  -f          Plot phi in the process of conversion.
  -l title    Plot title.
  -q          Do not write output file. Might be useful for plotting.

CDPro input file:
  -c IBasis   Produce CDPro input file instead of usual molar ellipticity
              list. IBasis number must be given
  -d title    One line title in the CDPro input file. Will be replaced with
              the infile argument, if not specified
  -n          Overwrite existing outfile, instead of appending to it

Written by Jan Havránek in 2018
```

`matplotlib` package is required for plotting. It can be installed with the following command (Windows):
```
> py -m pip install matplotlib
```

## On output files
With `-c` argument, output file is formatted like an INPUT file for CDPro. If file already exists, new task is appended, unless `-n` argument is given. In such case, old file is overwritten. In this version of CDPrep, this cannot be done while in batch mode. 

When `-c` is not given, pairs of values (wavelength - molar ellipticity) are written in the output file. Such file can be later processed by CRDATA.exe from the CDPro package. In this case, *old files are always overwritten*, so be careful!


## On batch files
Multiple files can be easily processed with the use of batch files. See sample_batch.txt file for more details on their formatting.


## On IBasis numbers
IBasis number (identifying a reference set) for CDPro must be provided, if INPUT files should be written. Available options are (based on CDPro version from February 5, 2004):
```
  _________________________________________________________
  |                                                       |
  | IBasis Ref.Set  Proteins   Secondary Structre WaveLen |
  |    1   SP29   29-SOLUBLE     H1,H2,S1,S2,T,U  178-260 |
  |    2   SP22X  22-SOLUBLE     H,3-10,S,T,P2,U  178-260 |
  |    3   SP37   37-SOLUBLE     H1,H2,S1,S2,T,U  185-240 |
  |    4   SP43   43-SOLUBLE     H1,H2,S1,S2,T,U  190-240 |
  |    5   SP37A  37-SOLUBLE       H,S,P2,T,U     185-240 |
  |    6   SDP42  SP37,5 Denatrd  H1,H2,S1,S2,T,U 185-240 |
  |    7   SDP48  SP43,5 Denatrd  H1,H2,S1,S2,T,U 190-240 |
  |    8   CLSTR  Soluble/Denatr. H1,H2,S1,S2,T,U 190-240 |
  |    9   SMP50  SP37,13 Membran H1,H2,S1,S2,T,U 185-240 |
  |   10   SMP56  SP43,13 Membran H1,H2,S1,S2,T,U 190-240 |
  |_______________________________________________________|
```

See CDPro documentation for more information.