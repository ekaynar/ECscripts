# window.py

Edit config.ini
```
input_file=sample.init
```

Run
```
python window.py
```
Outputs will look like
```
line: 7495000  :  7895000
0.361745
--------------
line: 7496000  :  7896000
0.3632325
```
this outputs shows you line(start-end) and hitratio when lru used as a cache.

then you can grap the selected window by:
```
sed -n '7495000,7895000' sample.init > 36hitratio
```
# createJobs.py
usage
```
Usage: ./createJobs <uniqfiles> <jobfiles>
./createJobs.py 36per8m 36files 36jobs
```
