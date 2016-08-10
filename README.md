## VERY MUCH UNDER DEVELOPMENT
You can use it but its not going to do much

# ASXListenerCLI
Displays Real-Time ASX information in a CLI

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
-s --subscribe [interval]     Subscribe prints updates at the given interval.
-r --raw                      Get the raw hash map returned.
-f --format [format string]   Specify the format to display the results.
-c --codes [Security Codes]   A comma seperated list of company security codes (case insensitive).
-o --overwrite                If set, subscribe will overwrite the current line as opposed to printing a new line.
```

### Format Specifiers
```
{code}            The stock security code.
{price}           The current price.
{percent_change}  The percentage of price change today.
...

```

### Examples
```
# Basic Example:
 $ asxlistener -c nab -f "Stock: {code}, Price: {price}"
 > Stock: NAB, Price: 22.220

# Multiple stocks, long form arguments, case insensitive security codes:
 $ asxlistener --codes Nab,AGL --format "{code}: {price} ({percent_change})"
 > NAB: 22.220 (-1.05%)
 > AGL: 5.460 (+0.46%)
```
