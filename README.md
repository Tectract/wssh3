# wssh3 - websocket shell v3 with TLS SNI support

wssh3 ("wish3") is a command-line utility/shell for WebSocket inpsired by netcat.

## Install

- Assumes Python 3.6

It uses currently uses gevent > 0.13, so you may need to install libevent. This is because it uses the great work in [ws4py](https://github.com/Lawouach/WebSocket-for-Python).
The gevent websocket server+client in there could probably be generalized to work with Eventlet; then this could be trivially ported to Eventlet to drop the libevent dependency.

If you don't have libevent installed already, install it prior to running setup.py. You can install libevent using `apt-get` on Ubuntu or `brew` on a Mac. 

        sudo apt-get install libevent-dev

install python3.6 from source if it is not already on your system

warning: check for /usr/lib/python3.6/ if it exists, then do NOT execute the commands below

	wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz
	tar -xvf Python-3.6.3.tgz
	cd Python-3.6.3
	sudo ./configure --enable-optimizations
	make
	sudo make install

make sure pip3 is updated and working with python3.6 and pip3 version 21 or higher, and get gevent

	sudo pip3 install --upgrade pip
	pip3 install gevent

install the modified version of ws4py-0.2.4 that supports TLS SNI (for SNI support, which you are going to want)

	git clone git://github.com/tectract/wssh3.git 
	cd wssh/ws4py_modified
	python3 setup.py install
	
now install wssh3

	cd ..
	python3 setup.py install

## Usage

Listen for WebSocket connections on a particular path and print messages to STDOUT:

	wssh3 -l localhost:8000/websocket

example: connect to coinbase BCH-USD socket and see trades from command-line:

	echo '{"type":"subscribe","product_ids":["BCH-USD"],"channels":["ticker"]}' | wssh3 -n wss://ws-feed.exhange.coinbase.com/ | grep --line-buffered trade_id

Once connected you can use STDIN to send messages. Each line is a message. You can just as well open a peristent client connection that prints incoming messages to STDOUT and sends messages from STDIN interactively:

	wssh3 localhost:8000/websocket

## Notes

if you use wssh3 called from a script, called from your server, check if the webserver / root user can properly access wssh3 and use it properly.

Stream scripts work from the command-line but not from the cron?
because root user cannot gracefully call wssh3!

copy gevent, greenlet, zope, ws4py, wssh3 files from .local/lib/python3.6/site-packages/ to /usr/local/lib/python3.6/site-packages
then chown -R root:staff /usr/local/lib/python3.6/site-packages
now root can run wssh3 without error!

## Contributing

Feel free to fork and improve.

## License 

MIT
