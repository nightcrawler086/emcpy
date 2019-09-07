import csv
import logging
from optparse import OptionParser
import unity

# Parse script arguments:
parser = OptionParser()

# Add the arguments
parser.add_option("-f", "--input-file",
                  action="store_true",
                  dest="input_file",
                  default=False,
                  help="Path to SOD Sheet saved as CSV")

# Import csv file to list of dicts
with open(input_file) as f:
    sod_dict = [{k: str(v) for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)]

# Get unique list of NAS Servers from the input file (now a dict)
unique_nas_servers = list({v['Prod VDM/EVS / CIFS / NFS server']: v for v in sod_dict}.values())

for r in unique_nas_servers:
    # do all NAS Server operations here
    print('This is the nas server from the unique list --> {}'.format(r['Prod VDM/EVS / CIFS / NFS server']))
