import csv
from collections import namedtuple
import datetime
import getpass
import logging
from optparse import OptionParser
import os
import sys
import time
import unity

# Parse script arguments:
parser = OptionParser()

# Add the arguments
parser.add_option("-f", "--input-file",
                  action="store",
                  dest="input_file",
                  default=False,
                  help="Path to SOD Sheet saved as CSV")
# This is essentially a filter for the file
parser.add_option("-s", "--sltn-number",
                  action="store",
                  dest="sltn_num",
                  default=None,
                  help="SLTN Number to filter the input file on.")
# username to connect to the Unity systems
parser.add_option("-u", "--unity-user",
                  action="store",
                  dest="u",
                  default='admin',
                  help="Username to log into the Unity API.")

# Prompt for password.
p = getpass.getpass('Password (one password for all Unity systems): ')
if not p:
    print('You must specify a password.')
    sys.exit()
# Parse the arguments
(opts, args) = parser.parse_args()
# Get current user
current_user = getpass.getuser()
# Define named tuple 'template' for each row in the input file.
# I'm using different names for the columns, since the input file
# contains too many spaces/special characters for me ;)
row = namedtuple('row', ('status', 'prov_tc', 'prod_frame', 'prod_sp', 'prod_pool', 'prod_fs', 'prod_eth_dev',
                         'prod_nas_server', 'prod_ip', 'prod_mask', 'prod_broadcast', 'prod_qip', 'fs_capacity_gb',
                         'cob_frame', 'cob_sp', 'cob_pool', 'cob_fs', 'cob_eth_dev', 'cob_nas_server', 'cob_ip',
                         'cob_mask', 'cob_broadcast', 'cob_qip', 'qtree', 'bkup_srvr', 'bkup_ip', 'bkup_mask',
                         'bkup_gw', 'sec_style', 'ad_group', 'netgroups'))

# This reads the input file, skips the first row and
# creates a tuple based on the 'template' above.  Then
# we add that tuple to a list
with open(opts.input_file, 'r') as f:
    r = csv.reader(f, delimiter=',')
    next(r)
    rows = [row(*l) for l in r]

# This is where we get a set of unique records based on the prod/cob frame
unique_frame_pairs = set()
unique_frame_list = []
print('Begin {}'.format(datetime.datetime.now()))
for i in rows:
    if (i.prod_frame, i.cob_frame) not in unique_frame_pairs:
        unique_frame_list.append(i)
    unique_frame_pairs.add((i.prod_frame, i.cob_frame))

# fp = frame pair
for fp in unique_frame_list:
    # print('Prod: {} -> Cob: {}'.format(fp.prod_frame, fp.cob_frame))
    # This is where we do any frame level checks
    #
    # Checks:
    # 1. Test to be sure both prod/cob frame are reachable
    # 2. Test to be sure the API is reachable (unauthenticated query)
    # 3. Connect to the PROD/COB Frame
    # 4. Figure out the current pool space/subscription ratio
    # 5. Sum total all space to be provisioned, the recalculate the space/subscription
    # 6. Warn if it will exceed a default threshold, add a configurable switch to modify threshold
    #
    prod_frame = unity.Unity(fp.prod_frame, opts.u, p)
    prod_frame.connect(quiet=True)
    cob_frame = unity.Unity(fp.cob_frame, opts.u, p)
    cob_frame.connect(quiet=True)
    # Evaluate pool space subscription ratio
    prod_pool = prod_frame.get('pool', rid=0, fields='sizeSubscribed', compact=True)
    cob_pool = cob_frame.get('pool', rid=0, fields='sizeSubscribed', compact=True)
    # This is where we create a unique list of NAS servers for the
    # current prod/cob frame pair
    uniq_ns = set()
    uniq_ns_list = []
    for x in rows:
        if fp.prod_frame == x.prod_frame and fp.cob_frame == x.cob_frame:
            if x.prod_nas_server not in uniq_ns:
                uniq_ns_list.append(x)
            uniq_ns.add(x.prod_nas_server)
    # ns = nas server
    for ns in uniq_ns_list:
        # This is where we do NAS Server level checks/operations
        #
        # 1. Test to be sure the NAS Server doesn't already exist
        # 2. Test to be sure the interface doesn't already exist (query and ping?)
        # 3. Check DNS setup
        # 4. Check all types of filesystems that belong to this NAS Server
        #   4a.  This seems like it might take a while
        if ns.sec_style == 'CIFS':
            print("prodUnity.create('nasServer', {}, {}, {})".format(ns.prod_nas_server, ns.prod_pool, ns.prod_sp))
        elif ns.sec_style == 'NFS':
            print('NFS')
        elif ns.sec_style == 'Mixed':
            print('Mixed')
        else:
            continue
        # This is where we create a unique list of filesystems for the
        # current NAS Server
        uniq_fs = set()
        uniq_fs_list = []
        for y in rows:
            if ns.prod_nas_server == y.prod_nas_server:
                if y.prod_fs not in uniq_fs:
                    uniq_fs_list.append(y)
                uniq_fs.add(y.prod_fs)
        # fs = filesystem
        for fs in uniq_fs_list:
            # This is where we do Filesystem level checks/operations
            print("prodUnity.storageResource.create('Filesystem', {}, {}, {}, {})".format(fs.prod_fs, fs.prod_nas_server, fs.prod_pool, fs.fs_capacity_gb))
