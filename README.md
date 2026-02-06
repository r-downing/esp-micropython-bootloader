# esp-micropython-bootloader

A simple micropython boot.py file that automatically updates the main.py from a configured URL. It also lets the user reconfigure this and wifi settings via serial.

## setup

Open this project in VSCode and install the recommended extensions, including the [micropico](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) extension.

### Flashing a device with micropython

For esp devices, there is a script to re-flash the micropython image via serial:

```bash
./flash.sh <port>
```

Then use the micropico extension to load the project onto the device.

## workflow - setting up wifi and updates

Connect to a serial terminal and press the reset button on the device. Then within 5 seconds, press CTRL+C to enter the menu. Otherwise the device will try to connect to wifi for up to 30s then proceed to the main program if there is one.

The menu should look like:

```txt
Blocking for 5 seconds. Press CTRL+C now to configure wifi or updates
w - wifi
u - update url
x - exit
enter an option #:
```

Enter `w` to set the wifi ssid and password, or `u` to set the update url. The url should be to the raw file ([example](https://raw.githubusercontent.com/r-downing/esp-micropython-bootloader/refs/heads/main/main.py)). The bootloader uses etags to verify if the file has changed.

## development

Use `prek install` to set up automated commit-hooks for linting and formatting.
