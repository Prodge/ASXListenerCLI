# ASXListenerCLI
Displays Real-Time ASX information in a CLI

## Install
'''
git clone https://github.com/Prodge/ASXListenerCLI.git
cd ASXListenerCLI
make install
'''

## Usage
Run '''asxlistener''' after installing followed by the below flags.
Each stock will be output in order specified by the -c flag with the specified format.

### Flags
-h For help
-s [interval] Subscribe prints updates at the given interval
-r get the raw hash map returned
-f [format] Specify the format to display the results
-c [Security Codes] A comma seperated list of company security codes (case insensitive)

### Format
"Stock: {code} Price: {price} "
