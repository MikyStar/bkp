#!/usr/local/anaconda3/envs/bkp_custom/bin/python3

#############################################

import click
import tarfile
import os.path
import shutil
import pyAesCrypt
from getpass import getpass

#############################################

bufferSize = 64 * 1024

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

    if create and not extract:
        click.echo( click.style( 'Copying files ...', fg='cyan' ))
        cp( path, dest )

        make_tarfile( dest, dest + '.tgz')

        rm( dest )
        mv( dest + '.tgz', dest )

        click.echo( click.style( 'Archive created.', fg='green' ))

        if encrypt and not decrypt:
            encrypt_aes( dest, dest + '.enc' )

            rm( dest )
            mv( dest + '.enc', dest )
            
            click.echo( click.style( 'Archive encrypted.', fg='green' ))
    elif extract and not create :
        if decrypt and not encrypt:
            decrypt_aes( path, dest + '.dec' )
            click.echo( click.style( 'Archive decrypted.', fg='green' ))

            extract_tarfile( dest + '.dec', dest )
            rm( dest + '.dec' )
            click.echo( click.style( 'Extraction complete.', fg='green' ))
        else :
            extract_tarfile( input, dest )
            click.echo( click.style( 'Extraction complete.', fg='green' ))


#############################################

def make_tarfile( source_dir, output_filename ):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def extract_tarfile( path, dest ) :
    tar = tarfile.open( path )
    tar.extractall( path=dest )
    tar.close()

def encrypt_aes( path, dest ) :
    if os.path.isfile( path ) :
        password = prompt_pswd(confirmation=True)
        pyAesCrypt.encryptFile( path, dest, password, bufferSize )

def decrypt_aes( path, dest ) :
    password = prompt_pswd()
    pyAesCrypt.decryptFile( path, dest, password, bufferSize )


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

def prompt_pswd( confirmation=False) :
    entry1 = getpass()

    if confirmation == False :
        return entry1
    else :
        entry2 = getpass('Confirmation: ')

        if entry1 != entry2 :
            click.echo( click.style( 'Not matching', fg='red' ))
            quit(-1)
        else :
            return entry1

#############################################

if __name__ == '__main__':
    main()