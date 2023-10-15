
# 1. Overview
This tutorial introduces the USB to SSI/SPI bridge focusing on connecting and a single register read.  The example steps through the software side only (not the embedded SPI / SSI side interfaces) illustrating how a software engineer can get up and running quickly with Python and libusb1.0.  The basic architecture of the bridge is also discussed as well as an internal configuration register access. Each code segment is discussed briefly and the Python module can be used as a template for customers starting from scratch.

## 1.1 USB to SSI Bridge
The USB bridge used in this tutorial is the USB2F-SSI-0-1A which, in general, is a small module that converts USB traffic into SPI / synchronous serial traffic for an embedded system.  This part number supports 0.05" pitch through hole headers on both sides of the SOM.  
The USB link is USB2.0 full speed with 3x interfaces.  One interface is for internal bridge register configuration and the other two interfaces are for high and low throughput data paths.  The module converts this USB traffic to/from embedded synchronous serial traffic. The embedded side consists of two interfaces, one for data transmit to an embedded system and the other for data reception from an embedded system. These two embedded interfaces are unidirectional.
The value and novel approach of this product architecture provides a more advanced solution for software to embedded communication when compared to virtual com. ports (VCP).  Some of the key bullet points are shown below:
-	3x different USB interfaces: Internal bridge register access, 64kB/s deterministic latency data interface, 600+kB/s high throughput interface.
-	Free to use any USB user space driver or develop a custom one
-	Auto enumerates with WINUSB Windows kernel driver
-	Separate TX and RX embedded synchronous serial data interfaces

 


