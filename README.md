# camerapi
Build your own security camera for the Echo Show

## Requirements:
* A Raspberry PI, I've tested this on the Pi2, Pi3 and PiZeroW Running Raspbian (tested this with the July 2017 Build)
* A Camera module fitted
* A domain name with access to the DNS server to create A and TXT records
* An AWS Account
* An Alexa Developer Account

## Steps
1) Start with a fresh install of raspbian for this I've used teh July 2017 version

2) Run raspi-config
change the default password
edit the hostname
enable the camera in interfaceing options
expand the filesystem in advance options


3) Install camera v4l2 module:
`vi /etc/modules`
Add a line at the botom of that file
`bcm2835-v4l2```

4) Install live555 media server
```
wget http://www.live555.com/liveMedia/public/live555-latest.tar.gz
tar -xvzf live555-latest.tar.gz
cd live
./genMakefiles linux
make
sudo make install
```

5) Next install the raspi rtsp server (modified from code found on https://www.raspberrypi.org/forums/viewtopic.php?t=52071)
```
wget http://s3.sammachin.com/raspi_rtsp.tgz
tar -xvzf raspi_rtsp.tgz
cd raspi
make
make install
```
6) Copy the startup script


7) Install and configure stunnel


8) Get an SSL Cert using lets encrypt from your main machine as certbot doesn't easily run on raspbian(look at doing on the pi https://www.k2dls.net/blog/2017/01/04/installing-certbot-on-raspbian-jessie/)

`certbot -d [hostname] --rsa-key-size 4096 --manual --preferred-challenges dns certonly`

9) Create a single cert file and copy over to the Pi

10) Setup the Alexa Skill

11) Create Lambda Function

12) Discover Devices
