# CameraPi

NOTE: This is a very early version and has a number of complex steps, I'm planning to improve the process in the future

## Requirements:
* A Raspberry PI, I've tested this on the Pi2, Pi3 and PiZeroW Running Raspbian (tested this with the July 2017 Build)
* A Camera module fitted
* A domain name with access to the DNS server to create A and TXT records
* An AWS Account
* An Alexa Developer Account


1) Start with a fresh install of raspbian for this I've used the July 2017 version

2) Run `raspi-config` as root 
change the default password
edit the hostname
enable the camera in interfaceing options
expand the filesystem in advance options


3) Install camera v4l2 module:
`vi /etc/modules`
Add a line at the botom of that file
`bcm2835-v4l2`


4) Install live555 media server as pi user not root
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
cd liveMedia
wget http://s3.sammachin.com/raspi_rtsp.tgz
tar -xvzf raspi_rtsp.tgz
cd raspi
make
make install
```

6) Copy the startup script
Place start.sh in the `home` directory of the `pi` user (not root)
run `start.sh`
You can now verify that your camera is working properly using VLC on your computer by opening a network address of rtsp://[YOUR PI IP]:8080/h264

7) Install and configure stunnel (as root)
`apt-get install stunnel`
Place the stunnel.conf file at /etc/stunnel/stunnel.conf

Edit the file /etc/default/stunnel4
changing

ENABLED=0
to
ENABLED=1

8) Setup DNS entry for the Camera's private IP address on your LAN
I use AWS Route53 but any DNS host should be fine, just create a A record for the Pi's IP address and give it a hostname like camerapi.[YOURDOMAIN.COM] 
Yes Putting Private IP's into public DNS is discouraged, but if this is only for your personal use then you're not going to break the internet, I use a separate domain for my camera's just to keep stuff clean.

9) Get an SSL Cert using lets encrypt from your main machine as certbot doesn't easily run on raspbian
`certbot -d [hostname] --rsa-key-size 4096 --manual --preferred-challenges dns certonly`
It will ask you to verify domain ownership by creating a special DNS record, be careful with this as if you make a mistake it can take a long time for the DNS chace to expire so you can try again!
Copy the files `privkey.pem` and `fullchain.pem` created by certbot over to the Pi in `/etc/stunnel`

10) Start stunnel as root
`stunnel`


10) Create a Lambda Function 
Use the code in the `lambda` folder, you will need to edit the cameras.json file to contain the names and hostname of your camera(s) using the domain names you setup above, its important to keep the `:443/h264` on the end of the URLs.

11) Setup the Alexa Skill
Signin to Developer.amazon.com,
Within the Alexa Skills Kit section
Click Add a Skill
Slect the Smart Home API SKill
Give it a name like `CameraPi`
Set the Payload version to v2
There is no need for an interaction model on smart home skills
Link the skill to your Lambda Instance


12) Setup Login with Amazon
Follow the guide here https://developer.amazon.com/blogs/post/Tx3CX1ETRZZ2NPC/Alexa-Account-Linking-5-Steps-to-Seamlessly-Link-Your-Alexa-Skill-with-Login-wit
You don't  need to authenticate the cameras within the skill if its only for your own use the Smart Home skills require authentication.

13) Discover Devices
"Alexa Discover Devices"
Should find your new camera.
You can then say `Alexa show Office Camera` or whatever you've named to to open the stream
`Alexa Stop` ends the video
