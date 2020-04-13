# bkp

_A simple command line tool to create Backups_

<hr>

## Install

`Requires conda`

```sh
conda env create -f environment.yml
chmod u+x bkp.py
```

## Use

````sh
./bkp.py -ce my_dir # Create an AES-256-CBC targz archive 
./bkp.py -xd my_dir.bkp ./here/archive # Decrypt and extract the archive to provided destination

./bkp.py --help # Further informations
```