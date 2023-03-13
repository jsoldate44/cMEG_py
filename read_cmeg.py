import sys,os
import struct
import numpy as np
import matplotlib.pyplot as plt


def read_cmeg(dataname,sessionname,byte_order='>'):

    if not(os.path.exists(dataname)) or not('.cMEG' in dataname):
        raise(f'No file named {dataname} exists \nPlease supply a .cMEG data file to load')

    if not(os.path.exists(sessionname)) or not('_SessionInfo.txt' in sessionname):
        raise(f'No file named {sessionname} exists \nPlease supply a session file from circa magnetics recording')

    with open(sessionname) as f:
        sinfo = f.read().strip().split('\n')

        if 'Sensor Names:' in sinfo[-1]:
            chan_names = sinfo[-1].split(',')
    
    with open(dataname,'r+b') as f:
        binfo = f.read()
        off = 0
        total = []
        while off < len(binfo):
            (d1, d2) = struct.unpack_from('>II',binfo,off)
            off+=struct.calcsize(f'>II')
            dsize = d1 * d2

            dat = struct.unpack_from(f'>{dsize}d',binfo,off)
            off+=struct.calcsize(f'>{dsize}d')

            dat_array = np.array(dat).reshape((d2,d1),order='F')

            total.append(dat_array)
        
    raw_dat = np.concatenate(total,axis=0)

    return raw_dat[:,1:], chan_names


if __name__ == '__main__':
    fname = sys.argv[1]

    short = fname[:-5]

    if os.path.exists(f'{short}.cMEG') and os.path.exists(f'{short}_SessionInfo.txt'):
        beef,keef = read_cmeg(f'{short}.cMEG',f'{short}_SessionInfo.txt')

    print(beef.shape,len(keef))

