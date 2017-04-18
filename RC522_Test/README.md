# Installation of Libs

In order for this to run we need the SPI-py and MFRC522-python libraries installed.

1. Clone SPI-py by cloning the git repo:
    - `git clone https://github.com/lthiery/SPI-Py.git`
2. Build and Install: 
    - `python3 setup.py build && sudo python3 setup.py install`
    - Now, it should be installed correctly
3. Clone MFRC522:
    - `git clone https://github.com/mxgxw/MFRC522-python.git`
4. Convert to python3
    - `2to3-3.6 -w MFRC522.py`
5. Copy to library folder
    - `sudo cp MFRC522.py /usr/local/lib/python3.6/`

# Running

Run the script with: `sudo ./test.py`

# Pin Setup

Pin setup for the reader/writer is simple, but important.

I followed this table for a reference:

| Name | Pin # | Pin name   | Color  |
|------|-------|------------|--------|
| SDA  | 24    | GPIO8      | Green  |
| SCK  | 23    | GPIO11     | Blue   |
| MOSI | 19    | GPIO10     | Purple |
| MISO | 21    | GPIO9      | Grey   |
| IRQ  | None  | None       | Brown  |
| GND  | Any   | Any Ground | Black  |
| RST  | 22    | GPIO25     | White  |
| 3.3V | 1     | 3V3        | Red    |
| LED  | 15    | LED        | Orange |
