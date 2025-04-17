please use 'tool/import/shared library' to import the dll into Labview.
A path to the 'ansi' directory needs to be included (see image). 

Note that Boolean VI outputs are imported as integer outputs (e.g. VIs beginning with 'is',like 'IsControllingTemperature', see the example.vi). 

The program needs to start with the 'begin' and 'connect' VIs and has to end with the 'disconnect' VI.

The type of attoDry needs to be specified in the begin.vi input:

0 - attoDry1100
1 - attoDry2100 
2 - attoDry800