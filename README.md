# rtl-sdr-troubleshooting

## Verify SDR Range

### You can try a test signal sweep around 1694 MHz using rtl_power:

rtl_power -f 1693000000:1695000000:1000 -g 42 -i 10 -e 2m output.csv

rtl_power -f 1693000000:1695000000:1k -g 42 -i 5 -e 1m output.csv

#### Example 

```
root@goes-receiver:~# rtl_power -f 1693000000:1695000000:1000 -g 42 -i 10 -e 2m output.csv
Number of frequency hops: 1
Dongle bandwidth: 2000000Hz
Downsampling by: 1x
Cropping by: 0.00%
Total FFT bins: 2048
Logged FFT bins: 2048
FFT bin size: 976.56Hz
Buffer size: 16384 bytes (4.10ms)
Reporting every 10 seconds
Found 1 device(s):
  0:  Nooelec, SMArTee XTR v5, SN: 00000001

Using device 0: Generic RTL2832U OEM
Found Elonics E4000 tuner
Tuner gain set to 42.00 dB.
Exact sample rate is: 2000000.052982 Hz
```

## Test RTL-SDR independently to verify gain setting works

### To make sure it's not an RTL-SDR issue, you can use rtl_test:

rtl_test -t

#### Example

```
root@goes-receiver:~# rtl_test -t
Found 1 device(s):
  0:  Nooelec, SMArTee XTR v5, SN: 00000001

Using device 0: Generic RTL2832U OEM
Found Elonics E4000 tuner
Supported gain values (14): -1.0 1.5 4.0 6.5 9.0 11.5 14.0 16.5 19.0 21.5 24.0 29.0 34.0 42.0
Sampling at 2048000 S/s.
Benchmarking E4000 PLL...
[E4K] PLL not locked for 51000000 Hz!
[E4K] PLL not locked for 2216000000 Hz!
[E4K] PLL not locked for 1108000000 Hz!
[E4K] PLL not locked for 1247000000 Hz!
E4K range: 52 to 2215 MHz
E4K L-band gap: 1108 to 1247 MHz
```

## Plot heatmaps

### show plot only

python3 heatmap.py output.csv

### scan 1694 mhz and save as png

python3 heatmap.py output.csv --png --output scan_1694mhz

### save as png

python3 heatmap.py output.csv --png

### save as png and pdf

python3 heatmap.py output.csv --png --pdf

### Show just 169.4–169.42 MHz, dim under -50 dB, save as PNG

python3 heatmap.py output.csv --fmin 1694000000 --fmax 1694200000 --threshold -50 --png

### Save trimmed spectrum to PDF only:

python3 heatmap.py output.csv --fmin 1693900000 --fmax 1694300000 --pdf

