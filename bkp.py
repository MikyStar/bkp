#!/usr/local/anaconda3/envs/bkp_custom/bin/python3

#############################################

import click
import tarfile
import os

#############################################

"""
- Make bkp
- Extract bkp
- Encrypt
- Decrypt
- Add timestamp
- Choose format of timestamp
"""

@click.command()
@click.option( '-c', '--create', is_flag=True )
@click.option( '-x', '--extract', is_flag=True )
@click.option( '-e', '--encrypt', is_flag=True )
@click.option( '-h', '--hash-type', type=click.Choice(['MD5', 'SHA1'], case_sensitive=False))
@click.option( '-d', '--decrypt', is_flag=True )
@click.option( '-t', '--timestamp', is_flag=True )
@click.argument('dir', type=click.Path(exists=True, dir_okay=True))
@click.argument('dest', type=click.Path(exists=False ))
def main( create, extract, encrypt, hash_type, decrypt, timestamp, dir, dest ) :
    print( create )
    print(hash_type)

def make_tarfile( output_filename, source_dir ):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

#############################################

if __name__ == '__main__':
    main()