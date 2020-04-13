#!/usr/bin/env conda run -n bkp python

#############################################

import click
import tarfile
import os.path
import os
import shutil
import pyAesCrypt
from getpass import getpass
from datetime import datetime

#############################################

BUFFER_SIZE = 64 * 1024

#############################################

@click.command()
@click.option( '-c', '--create', is_flag=True )
@click.option( '-x', '--extract', is_flag=True )
@click.option( '-e', '--encrypt', is_flag=True )
@click.option( '-d', '--decrypt', is_flag=True )
@click.option( '-t', '--timestamp', is_flag=True )
@click.option( '--extension/--no-extension', default=True )
@click.argument('path', type=click.Path(exists=True))
@click.argument('dest', default='' )
def main( create, extract, encrypt, decrypt, timestamp, extension, path, dest ) :
    """
    DEST if not provided will be same path with '.bkp' for archiving or '.full' for extracting
    """
    final_extension = ''

    if timestamp:
        final_extension += '.' + get_timestamp()

    if extension :
        final_extension += '.bkp' if ( create and not extract ) else '.full'

    if dest == '' :
        dest = path + final_extension
    else :
        dest = dest + final_extension

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
        pyAesCrypt.encryptFile( path, dest, password, BUFFER_SIZE )

def decrypt_aes( path, dest ) :
    password = prompt_pswd()
    pyAesCrypt.decryptFile( path, dest, password, BUFFER_SIZE )

def get_timestamp() :
    now = datetime.now()
    return now.strftime( "%d.%m.%Y.%H.%M.%S")

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
