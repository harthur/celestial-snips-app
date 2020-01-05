# Celestial

This is a [Snips](snips.ai) voice assistant that runs on a Raspberry Pi 3 that has a Sense HAT attachment.

# Setup

The first part of these instructions come from: https://docs.snips.ai/getting-started/quick-start-raspberry-pi

1) Burn [Raspian Stretch](https://www.raspberrypi.org/documentation/installation/installing-images/) onto a 16GB-128GB micro SD Card. If it doesn't work, try sliding the little “read-only” physical switch on SD card.

2) Add a `wpa_supplicant.conf` to the `/boot` directory of the SD card that looks like this:

```conf
# Giving configuration update rights to wpa_cli
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

# ISO/IEC alpha2 country code in which the device is operating
country=US

network={
  ssid="Your Wi-Fi network name"
  psk="Your Wi-Fi network password"
}

network={
  ssid="Second network"
  psk="Second password"
}
```

So that it can connect to wifi when it boots. In the future, you can edit this file at `/etc/wpa_supplicant/wpa_supplicant.conf` on the Pi.

3) Put micro SD card into the Raspberry Pi,

4) Plug in the Raspberry Pi's power supply.

5) SSH using `ssh pi@raspberrypi.local` with password “raspberry” to get into the Pi.

6) Change the hostname on the Pi to something unique e.g. `celestialpi` in `/etc/hostname`. Also update `/etc/hosts` to include the line `127.0.1.1 celestialpi`.

7) Change the password with `passwd` so that your Pi doesn't get recruited for a botnet.

8) Always shut down the Pi with `sudo shutdown now` and wait for Pi light to stop blinking. This prevents the SD card from being corrupted if it's interrupted by unplugging the power supply.

# Sense HAT set-up

1) Plug the Sense HAT into the Pi's GPIO pins

2) Install `sudo apt-get install libjpeg-dev`

3) Calibrate the Sense HAT's compass with:

```bash
sudo apt-get install octave
cp /usr/share/librtimulib-utils/RTEllipsoidFit ./ -a
cd RTEllipsoidFit
RTIMULibCal
```

And follow the instructions for `m`.

Then update the global calibration config with:

```bash
rm ~/.config/sense_hat/RTIMULib.ini
sudo cp RTIMULib.ini /etc
```

4) Many issues with Sense HAT + Snips come from the fact that the Snips skill server runs as another user with less permissions than the pi user, so you need to enable them with:

```bash
sudo usermod -a -G video,input,i2c _snips-skills
```
