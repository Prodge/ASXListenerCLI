# ASXListenerCLI
Displays Real-Time ASX information in a CLI

## Install
```
git clone https://github.com/Prodge/ASXListenerCLI.git
cd ASXListenerCLI
make install
```

## Usage
Run `asxlistener` after installing followed by the below flags.
Each stock will be output in order specified by the -c flag with the specified format.

### Flags
```
-h For help.
-s [interval] Subscribe prints updates at the given interval.
-r get the raw hash map returned.
-f [format] Specify the format to display the results.
-c [Security Codes] A comma seperated list of company security codes (case insensitive).
-l If set, subscribe will overwrite the current line as opposed to printing a new line.
```

### Format Specifiers
```
{code}
{price}
{percent_change}
...

```

### Examples
```
# Basic Example:
 $ asxlistener -c nab -f "Stock: {code}, Price: {price}"
 > Stock: NAB, Price: 22.220

# Long form arguments can be used and security codes are case insensitive
 $ asxlistener --codes nab,AGL --format "Stock: {code}, Price: {price} ({percent_change})"
 > Stock: NAB, Price: 22.220 (-1.05%)
 > Stock: AGL, Price: 5.460 (+0.46%)
```
