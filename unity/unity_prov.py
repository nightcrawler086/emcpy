import csv
from collections import namedtuple
import logging
from optparse import OptionParser
import unity

# Parse script arguments:
parser = OptionParser()

# Add the arguments
parser.add_option("-f", "--input-file",
                  action="store",
                  dest="input_file",
                  default=False,
                  help="Path to SOD Sheet saved as CSV")

parser.add_option("-s", "--sltn-number",
                  action="store",
                  dest="sltn_num",
                  default=None,
                  help="SLTN Number to filter the input file on.")

# Parse the arguments
(opts, args) = parser.parse_args()

"""
# Import csv file to list of dicts
with open(opts.input_file) as f:
    sod_dict = [{k: str(v) for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)]
"""
# Define named tuple 'template' for each row in the input file.
# I'm using different names for the columns, since the input file
# contains too many spaces/special characters for me ;)
row = namedtuple('row', ('status', 'prov_tc', 'prod_frame', 'prod_sp', 'prod_pool', 'prod_fs', 'prod_eth_dev',
                         'prod_nas_server', 'prod_ip', 'prod_mask', 'prod_broadcast', 'prod_qip', 'fs_capacity_gb',
                         'cob_frame', 'cob_sp', 'cob_pool', 'cob_fs', 'cob_eth_dev', 'cob_nas_server', 'cob_ip',
                         'cob_mask', 'cob_broadcast', 'cob_qip', 'qtree', 'bkup_srvr', 'bkup_ip', 'bkup_mask',
                         'bkup_gw', 'sec_style', 'ad_group', 'netgroups'))

with open(opts.input_file, 'r') as f:
    r = csv.reader(f, delimiter=',')
    next(r)
    rows = [row(*l) for l in r]

current_prod_frame = None
current_cob_frame = None
sorted_rows = sorted(rows, key=lambda i: [i.prod_frame, i.cob_frame])

for x in sorted_rows:
    if x.prod_frame == current_prod_frame and x.cob_frame == current_cob_frame:
        continue
    else:
        current_prod_frame = x.prod_frame
        current_cob_frame = x.cob_frame
        print('Prod: {} -> Cob: {}'.format(x.prod_frame, x.cob_frame))
# Unique list of source/target frames


"""
print('Total records in file: {}'.format(len(sod_dict)))
# Sort sheet by PROD/COB filer pairs
# sod_dict_sorted = sorted(sod_dict, key=lambda i: (i['Prod Physical Device'], i['COB Physical Device']))
uniq = [list(y) for x, y in itertools.groupby(sorted(sod_dict, key=lambda x:
(x['Prod Physical Device'], x['COB Physical Device'])))]
print('Number of unique records: {}'.format(len(uniq)))
for x in sod_dict_sorted:
    print('Prod: {} -> Cob: {}'.format(x['Prod Physical Device'], x['COB Physical Device']))
    # Do all frame level operations here (pool space, etc)
    # Get unique list of NAS Servers from the input file (now a dict)
    #unique_nas_servers = list({v['Prod VDM/EVS / CIFS / NFS server']: v for v in sod_dict}.values())
    for r in unique_nas_servers:
        # do all NAS Server operations here
        # print('{}'.format(r['Prod VDM/EVS / CIFS / NFS server']))
        key = r['Prod VDM/EVS / CIFS / NFS server']
        unique_fs = list(filter(lambda d: d['Prod VDM/EVS / CIFS / NFS server'] in key, sod_dict))
        for fs in unique_fs:
            # Do all filesystem operations here
            print(fs['File System'])
"""
