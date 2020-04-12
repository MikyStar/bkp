#!/usr/local/anaconda3/envs/bkp_custom/bin/python3

#############################################

import click
import tarfile
import os.path
import shutil

#############################################

"""
- Encrypt
- Decrypt
- Add timestamp
- Choose format of timestamp
- Make temporary names to 'hide' the steps 
"""

@click.command()
@click.option( '-c', '--create', is_flag=True )
@click.option( '-x', '--extract', is_flag=True )
@click.option( '-e', '--encrypt', is_flag=True )
@click.option( '-h', '--hash-type', type=click.Choice(['MD5', 'SHA1'], case_sensitive=False))
@click.option( '-d', '--decrypt', is_flag=True )
@click.option( '-t', '--timestamp', is_flag=True )
@click.argument('path', type=click.Path(exists=True))
@click.argument('dest', type=click.Path(exists=False ))
def main( create, extract, encrypt, hash_type, decrypt, timestamp, path, dest ) :

    #if encrypt and not decrypt:
    #    encrypt_dir( dir )

    # Archiving
    if create and not extract:
        click.echo( click.style( 'Copying files ...', fg='cyan' ))
        cp( path, dest )

        make_tarfile( dest, dest + '.tgz')

        rm( dest )
        mv( dest + '.tgz', dest )

        click.echo( click.style( 'Archive created.', fg='green' ))
    elif extract and not create :
        extract_tarfile( path, dest )
        
        click.echo( click.style( 'Extraction complete.', fg='green' ))
    


#############################################

def make_tarfile( source_dir, output_filename ):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def extract_tarfile( path, dest ) :
    tar = tarfile.open( path )
    tar.extractall( path=dest )
    tar.close()

def mv( path, dest ) :
    os.rename(path, dest)

def cp( path, dest ) :
    if os.path.isdir( path ) :
        shutil.copytree( path, dest )
    if os.path.isfile( path ) :
        shutil.copyfile( path, dest)

def rm( path ) :
    if os.path.isdir( path ) :
        shutil.rmtree( path )
    elif os.path.isfile( path ) :
        os.remove( path )

#############################################

if __name__ == '__main__':
    main()