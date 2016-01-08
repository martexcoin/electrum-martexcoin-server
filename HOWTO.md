How to run your own Electrum server
===================================

Abstract
--------

This document is an easy to follow guide to installing and running your own
Electrum server on Linux. It is structured as a series of steps you need to
follow, ordered in the most logical way. The next two sections describe some
conventions we use in this document and the hardware, software, and expertise
requirements.

The most up-to date version of this document is available at:

    https://github.com/martexcoin/electrum-mxt-server/blob/master/HOWTO.md

Conventions
-----------

In this document, lines starting with a hash sign (#) or a dollar sign ($)
contain commands. Commands starting with a hash should be run as root,
commands starting with a dollar should be run as a normal user (in this
document, we assume that user is called 'martexcoin'). We also assume the
martexcoin user has sudo rights, so we use '$ sudo command' when we need to.

Strings that are surrounded by "lower than" and "greater than" ( < and > )
should be replaced by the user with something appropriate. For example,
\<password\> should be replaced by a user chosen password. Do not confuse this
notation with shell redirection ('command < file' or 'command > file')!

Lines that lack hash or dollar signs are pastes from config files. They
should be copied verbatim or adapted without the indentation tab.

apt-get install commands are suggestions for required dependencies.
They conform to an Ubuntu 13.10 system but may well work with Debian
or earlier and later versions of Ubuntu.

Prerequisites
-------------

**Expertise.** You should be familiar with Linux command line and
standard Linux commands. You should have a basic understanding of git
and Python packages. You should have knowledge about how to install and
configure software on your Linux distribution. You should be able to
add commands to your distribution's startup scripts. If one of the
commands included in this document is not available or does not
perform the operation described here, you are expected to fix the
issue so you can continue following this howto.

**Software.** A recent Linux 64-bit distribution with the following software
installed: `python`, `easy_install`, `git`, standard C/C++
build chain. You will need root access in order to install other software or
Python libraries. Python 2.7 is the minimum supported version.

**Hardware.** The lightest setup is a pruning server with diskspace 
requirements of about 4 GB for the electrum database. However note that 
you also need to run martexcoind and keep a copy of the full blockchain, 
which is roughly 4 GB in July 2015. If you have less than 2 GB of RAM 
make sure you limit martexcoind to 8 concurrent connections. If you have more 
resources to spare you can run the server with a higher limit of historic
transactions per address. CPU speed is important for the initial block
chain import, but is also important if you plan to run a public Electrum server, 
which could serve tens of concurrent requests. Any multi-core x86 CPU from 2009 or
newer other than an Atom should do for good performance. An ideal setup
has enough RAM to hold and process the leveldb database in tmpfs (e.g. /dev/shm).

Instructions
------------

### Step 1. Create a user for running martexcoind and Electrum server

This step is optional, but for better security and resource separation I
suggest you create a separate user just for running `martexcoind` and Electrum.
We will also use the `~/bin` directory to keep locally installed files
(others might want to use `/usr/local/bin` instead). We will download source
code files to the `~/src` directory.

    $ sudo adduser martexcoin --disabled-password
    $ sudo apt-get install git
    $ sudo su - martexcoin
    $ mkdir ~/bin ~/src
    $ echo $PATH

If you don't see `/home/martexcoin/bin` in the output, you should add this line
to your `.bashrc`, `.profile`, or `.bash_profile`, then logout and relogin:

    PATH="$HOME/bin:$PATH"
    $ exit

### Step 2. Download martexcoind

We currently recommend martexcoind 0.10.2.2 stable.

If you prefer to compile martexcoind, here are some pointers for Ubuntu:

    $ sudo apt-get install make g++ python-leveldb libboost-all-dev libssl-dev libdb++-dev pkg-config automake libtool
    $ sudo su - martexcoin
    $ cd ~/src && git clone https://github.com/martexcoin-project/martexcoin.git -b master-0.10
    $ cd martexcoin
    $ ./autogen.sh
    $ ./configure --disable-wallet --without-miniupnpc
    $ make
    $ strip src/martexcoind src/martexcoin-cli src/martexcoin-tx
    $ cp -a src/martexcoind src/martexcoin-cli src/martexcoin-tx ~/bin

### Step 3. Configure and start martexcoind

In order to allow Electrum to "talk" to `martexcoind`, we need to set up an RPC
username and password for `martexcoind`. We will then start `martexcoind` and
wait for it to complete downloading the blockchain.

    $ mkdir ~/.martexcoin
    $ $EDITOR ~/.martexcoin/martexcoin.conf

Write this in `martexcoin.conf`:

    rpcuser=<rpc-username>
    rpcpassword=<rpc-password>
    daemon=1
    txindex=1
    disablewallet=1


If you have an existing installation of martexcoind and have not previously
set txindex=1 you need to reindex the blockchain by running

    $ martexcoind -reindex

If you already have a freshly indexed copy of the blockchain with txindex start `martexcoind`:

    $ martexcoind

Allow some time to pass, so `martexcoind` connects to the network and starts
downloading blocks. You can check its progress by running:

    $ martexcoin-cli getinfo

Before starting the electrum server your martexcoind should have processed all
blocks and caught up to the current height of the network (not just the headers).
You should also set up your system to automatically start martexcoind at boot
time, running as the 'martexcoin' user. Check your system documentation to
find out the best way to do this.

### Step 4. Download and install Electrum Server

We will download the latest git snapshot for Electrum to configure and install it:

    $ cd ~
    $ git clone https://github.com/martexcoin/electrum-mxt-server.git
    $ cd electrum-mxt-server
    $ sudo configure
    $ sudo python setup.py install

See the INSTALL file for more information about the configure and install commands. 

### Optional Step 5: Install Electrum dependencies manually

Electrum server depends on various standard Python libraries and leveldb. These will usually be
installed by caling "python setup.py install" above. They can be also be installed with your
package manager if you don't want to use the install routine

    $ sudo apt-get install python-setuptools python-openssl python-leveldb libleveldb-dev 
    $ sudo easy_install jsonrpclib irc plyvel

Regarding leveldb see the steps in README.leveldb for further details, especially if your system
doesn't have the python-leveldb package or if plyvel installation fails.

leveldb should be at least version 1.9.0. Earlier version are believed to be buggy.

### Step 6. Select your limit

Electrum server uses leveldb to store transactions. You can choose
how many spent transactions per address you want to store on the server.
The default is 100, but there are also servers with 1000 or even 10000.
Few addresses have more than 10000 transactions. A limit this high
can be considered equivalent to a "full" server. Full servers previously
used abe to store the blockchain. The use of abe for electrum servers is now
deprecated.

The pruning server uses leveldb and keeps a smaller and
faster database by pruning spent transactions. It's a lot quicker to get up
and running and requires less maintenance and diskspace than abe.

The section in the electrum server configuration file (see step 10) looks like this:

     [leveldb]
     path = /path/to/your/database
     # for each address, history will be pruned if it is longer than this limit
     pruning_limit = 100

### Step 7. Import blockchain into the database or download it

It's recommended to fetch a pre-processed leveldb from the net. 
The "configure" script above will offer you to download a database with pruning limit 100.

You can fetch recent copies of electrum leveldb databases with differnt pruning limits 
and further instructions from the Electrum-MXT full archival server foundry at:
http://foundry.electrum-mxt.org/leveldb-dump/


Alternatively, if you have the time and nerve, you can import the blockchain yourself.

As of April 2014 it takes between one and two days to import 500k blocks, depending
on CPU speed, I/O speed, and your selected pruning limit.

It's considerably faster and strongly recommended to index in memory. You can use /dev/shm or
or create a tmpfs which will also use swap if you run out of memory:

    $ sudo mount -t tmpfs -o rw,nodev,nosuid,noatime,size=15000M,mode=0777 none /tmpfs

If you use tmpfs make sure you have enough RAM and swap to cover the size. If you only have 2 gigs of
RAM but add 15 gigs of swap from a file that's fine too. tmpfs is rather smart to swap out the least
used parts. It's fine to use a file on an SSD for swap in this case.

It's not recommended to do initial indexing of the database on a SSD because the indexing process
does at least 10 TB (!) of disk writes and puts considerable wear-and-tear on an SSD. It's a lot better
to use tmpfs and just swap out to disk when necessary.   

Databases have grown to roughly 4 GB in April 2014, give or take a gigabyte between pruning limits 
100 and 10000. Leveldb prunes the database from time to time, so it's not uncommon to see databases
~50% larger at times when it's writing a lot, especially when indexing from the beginning.


### Step 8. Create a self-signed SSL cert

[Note: SSL certificates signed by a CA are supported by 2.0 clients.]

To run SSL / HTTPS you need to generate a self-signed certificateusing openssl. 
You could just comment out the SSL / HTTPS ports in the config and run
without, but this is not recommended.

Use the sample code below to create a self-signed cert with a recommended validity 
of 5 years. You may supply any information for your sign request to identify your server.
They are not currently checked by the client except for the validity date.
When asked for a challenge password just leave it empty and press enter.

    $ openssl genrsa -des3 -passout pass:x -out server.pass.key 2048
    $ openssl rsa -passin pass:x -in server.pass.key -out server.key
    writing RSA key
    $ rm server.pass.key
    $ openssl req -new -key server.key -out server.csr
    ...
    Country Name (2 letter code) [AU]:US
    State or Province Name (full name) [Some-State]:California
    Common Name (eg, YOUR name) []: electrum-server.tld
    ...
    A challenge password []:
    ...

    $ openssl x509 -req -days 730 -in server.csr -signkey server.key -out server.crt

The server.crt file is your certificate suitable for the ssl_certfile= parameter and
server.key corresponds to ssl_keyfile= in your electrum server config.

Starting with Electrum 1.9, the client will learn and locally cache the SSL certificate 
for your server upon the first request to prevent man-in-the middle attacks for all
further connections.

If your certificate is lost or expires on the server side, you will need to run
your server with a different server name and a new certificate.
Therefore it's a good idea to make an offline backup copy of your certificate and key
in case you need to restore it.

### Step 9. Configure Electrum server

Electrum reads a config file (/etc/electrum-mxt.conf) when starting up. This
file includes the database setup, martexcoind RPC setup, and a few other
options.

The "configure" script listed above will create a config file at /etc/electrum-mxt.conf
which you can edit to modify the settings.

Go through the config options and set them to your liking.
If you intend to run the server publicly have a look at README-IRC.md

### Step 10. Tweak your system for running electrum

Electrum server currently needs quite a few file handles to use leveldb. It also requires
file handles for each connection made to the server. It's good practice to increase the
open files limit to 64k. 

The "configure" script will take care of this and ask you to create a user for running electrum-mxt-server.
If you're using user martexcoin to run electrum and have added it manually like shown in this HOWTO run 
the following code to add the limits to your /etc/security/limits.conf:

     echo "martexcoin hard nofile 65536" >> /etc/security/limits.conf
     echo "martexcoin soft nofile 65536" >> /etc/security/limits.conf

If you are on Debian > 8.0 Jessie or other distribution based on it, you also need to add these lines in /etc/pam.d/common-session and /etc/pam.d/common-session-noninteractive otherwise the limits in /etc/security/limits.conf will not work:

    echo "session required pam_limits.so" >> /etc/pam.d/common-session
    echo "session required pam_limits.so" >> /etc/pam.d/common-session-noninteractive
    
Check if the limits are changed either by logging with the user configured to run Electrum server as. Example:

    su - martexcoin
    ulimit -n

Or if you use sudo and the user is added to sudoers group:

    sudo -u martexcoin -i ulimit -n


Two more things for you to consider:

1. To increase security you may want to close martexcoind for incoming connections and connect outbound only

2. Consider restarting martexcoind (together with electrum-mxt-server) on a weekly basis to clear out unconfirmed
   transactions from the local the memory pool which did not propagate over the network.

### Step 11. (Finally!) Run Electrum server

The magic moment has come: you can now start your Electrum server as root (it will su to your unprivileged user):

    # electrum-mxt-server start

Note: If you want to run the server without installing it on your system, just run 'run_electrum_mxt_server" as the
unprivileged user.

You should see this in the log file:

    starting Electrum server

If you want to stop Electrum server, use the 'stop' command:

    # electrum-mxt-server stop


If your system supports it, you may add electrum-mxt-server to the /etc/init.d directory. 
This will ensure that the server is started and stopped automatically, and that the database is closed 
safely whenever your machine is rebooted.

    # ln -s `which electrum-mxt-server` /etc/init.d/electrum-mxt-server
    # update-rc.d electrum-mxt-server defaults

### Step 12. Test the Electrum server

We will assume you have a working Electrum client, a wallet, and some
transactions history. You should start the client and click on the green
checkmark (last button on the right of the status bar) to open the Server
selection window. If your server is public, you should see it in the list
and you can select it. If you server is private, you need to enter its IP
or hostname and the port. Press 'Ok' and the client will disconnect from the
current server and connect to your new Electrum server. You should see your
addresses and transactions history. You can see the number of blocks and
response time in the Server selection window. You should send/receive some
martexcoins to confirm that everything is working properly.

### Step 13. Join us on IRC, subscribe to the server thread

Say hi to the dev crew, other server operators, and fans on
irc.freenode.net #electrum-mxt and we'll try to congratulate you
on supporting the community by running an Electrum-MXT node.

If you're operating a public Electrum-MXT server please subscribe
to the following mailing list:
https://groups.google.com/forum/#!forum/electrum-mxt-server
It'll contain announcements about important updates to Electrum-MXT
server required for a smooth user experience.
