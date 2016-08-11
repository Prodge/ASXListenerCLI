# ASXListenerCLI
Displays Real-Time ASX information in a CLI.

![tty recording](https://raw.githubusercontent.com/Prodge/ASXListenerCLI/master/tty.gif)

## Install
```
git clone https://github.com/Prodge/ASXListenerCLI.git
cd ASXListenerCLI
sudo make install
```

## Usage
Run `asxlistener` after installing followed by the below flags.
Each stock will be output in order specified by the -c flag with the specified format.

### Flags
```
-h --help                     For help.
-s --subscribe [interval]     Subscribe prints updates at the given interval (in minutes).
-r --raw                      Get the raw hash map returned as json.
-f --format [format string]   Specify the format to display the results.
-c --codes [Security Codes]   A comma seperated list of company security codes (case insensitive).
-o --overwrite                If set, subscribe will overwrite the current line as opposed to printing a new line.
```

### Format Specifiers
Wherever you place {one of these} it will be replaced with the corresponding data shown below.
```
{code}            The stock security code.
{price}           The current price.
{change}          The amount the value has changed today.
{percent_change}  The percentage of price change today.
{bid}             The current buying price.
{offer}           The current selling price.
{open}            The price at which the first trade took place today.
{high}            The highest price for the security today.
{low}             The lowest price for the security today.
{volume}          The number of securities traded today.

```

### Examples
```
# Basic Example:
 $ asxlistener -c nab -f "Stock: {code}, Price: {price}"
 > Stock: NAB, Price: 22.220

# Multiple stocks, long form arguments, case insensitive security codes:
 $ asxlistener --codes Nab,AGL --format "{code}: ${price} ({percent_change})"
 > NAB: $22.220 (-1.05%)
 > AGL: $5.460 (+0.46%)

# Output all data as json:
 $ asxlistener -c cba -r
 > [{'code': 'CBA', 'low': '77.210', 'percent_change': '-1.29%', 'change': '-1.010', 'price': '77.400', 'open': '78.000', 'volume': '4,090,305', 'bid': '77.400', 'high': '79.090', 'offer': '77.440'}]

# Significant points throughout the day with many stocks (the limit is 10):
 $ asxlistener -c hhl,kor,rvy,hog,apd,asl -f "{code}: current {price}, open {open}, high {high}, low {low}"
 > HHL: current 4.070, open 0.000, high 0.000, low 0.000
 > KOR: current 0.022, open 0.000, high 0.000, low 0.000
 > RVY: current 0.033, open 0.027, high 0.035, low 0.027
 > HOG: current 0.006, open 0.000, high 0.000, low 0.000
 > APD: current 0.510, open 0.505, high 0.510, low 0.505
 > ASL: current 1.040, open 1.110, high 1.115, low 1.040
```
