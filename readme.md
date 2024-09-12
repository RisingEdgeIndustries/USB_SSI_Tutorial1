
# 1. Overview
This tutorial introduces the USB to SSI/SPI bridge which translates native USB traffic to synchronous serial communications. In this tutorial we will cover the system architecture and purpose of the bridge module as well as two basic connect and power-up excersise.

The first part of this tutorial covers communications using a REIndustries provided Python library which simplifies the software user space driver access. This library is a simple wrapper for the libusb1.0 Python library. This approach is the simplest and fastest way to get up and running.

The second part of the tutorial shows how to use the Python libusb1.0 third party library directly. This approach is more complicated, but likely more desireable for custom software applications that interface to the USB2F-SSI-0-1A module.



Solarized dark             |  Solarized Ocean
:-------------------------:|:-------------------------:
![alt text](./supplemental/pic2-top-small.png) |  ![alt text](./supplemental/pic1-side-small.png)




## 1.1 Bridge Overview
The USB bridge used in this tutorial is the USB2F-SSI-0-1A which, in general, is a small module that converts native USB traffic into SPI / synchronous serial traffic for an embedded system.  This part number supports 0.1" pitch through hole headers on both sides of the SOM and can fit in a standard prototyping breadboard. Many other configurations are available so visit [RisingEdgeIndustries](https://www.risingedgeindustries.com) online for more information or to ask about a custom solution. 

The USB link is USB2.0 full speed composite device with 3x interfaces.  One interface is for internal bridge register access supporting operational and configuration changes. The other two interfaces are for high and low throughput data paths.  Each data path works with native USB 2.0 64 byte blocks of data. The lower datarate interface is an interrupt interface capable of 64kB/s. The second data interface is a BULK interface which can operate in excess of 650kB/s (5.2Mbit/s). This datarate is dependant on how much bandwidth is available on the USB bus per USB 2.0 BULK interface protocol.

The embedded systems side of this bridge consists of two unidirectional SSI/SPI ports. The TX and RX data is separate to allow the customer embedded system to operate based on data frame interrupts rather than polling the bridge checking for data. The master SSI/SPI port forwards all USB 64 byte packets out to the target embedded system as a 68 byte frame. The frame is larger than the USB packet because 4 additional bytes of meta data are added. The meta data allows target embedded systems to know which USB interface (INT1 or BULK2) the 64 byte packet came from. This allows the embedded systems engineer to be aware of which USB interface software sent the packet over. When the embedded system assembles a frame to transmist to the USB bridge RX interface, the firmware engineer must add this meta data to the frame so the bridge knows which USB interface to forward the 68 byte frame to.

The meta data allows the software engineer and firmware engineer on either side of the bridge to stay in sync and understand which interfaces data comes from and should be sent to.

An example use case may be that an embedded system needs to send low data rate telemetry information back to software which can be done over INT1 (interrupt interface 1). The software engineer can launch a thread that constantly monitors for data on the USB interface and when available, reads the data and passes it to the main software application. The BULK2 (bulk 2) interface is used specifically for large data transfers to and from the target embedded system.

This bridge module is ideal for customers that need a more intelligent solution than a virtual serial port for software application to embedded system simple communication.

Some of the key features/improvements are shown below:
-	3x different USB interfaces: Internal bridge register access, 64kB/s deterministic latency data interface, 650+kB/s high throughput interface.
-	Free to use any USB user space driver or develop a custom one
-	Auto enumerates with WINUSB Windows kernel driver
-	Separate TX and RX embedded synchronous serial data interfaces for interrupt driven firmware development
-	Plug and play solution utilizing REIndustries free Python library
-	Prototype friendly, footprint compatible with standard breadboards
-	Many functional configuration options via internal bridge register space



# 2. Part 1: REIndustries Simple Library
Part 1 of this tutorial covers how to connect and query basic bridge information via the USB interface. The USB descriptor information is read from the device as well as the entire configuration register space. The register space is read via the configuration interface INT0 (interrupt 0). All of this access is done using an example library from REIndustries using the Python programming language. This is the 'plug-and-play' solution for users who are looking for a simple and quick way to get up and running.




