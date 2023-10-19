#
# Project Name:
# USB Bridge - Tutorial 1
#
# Author: rvalentine
# Date: 10/7/2023
#
# Project Description:
# ----------------------
# Supplemental code supporting USB bridge tutorial 1
# which finds, connects and displays bridge descriptor
# information.
#
#






import ctypes as ct
import libusb as usb



#
# operational definitions
#
DEF_VID = 0x1cbf
DEF_PID = 0x0007
DEF_SN = "00000001"
ENDPOINT1_OUT = 0x01
ENDPOINT1_IN = 0x81 	# usb.LIBUSB_ENDPOINT_IN + 1 # 0x81
EP1IN_SIZE = 64*1
EP1IN_TIMEOUT = 1000 	# mS
EP1OUT_SIZE = 64*1
EP1OUT_TIMEOUT = 250 	# mS
DEV_MODE = True


#
# Libusb variables/data structures
#
dev = None
dev_found = False
#sn_tstring = ""	
sn_string = (ct.c_ubyte* 18)()	# sn string
pd_string = (ct.c_ubyte* 30)()	# product string
mf_string = (ct.c_ubyte* 26)()	# manf string
device_configuration = ct.POINTER(ct.c_int)()
dev_handle = ct.POINTER(usb.device_handle)() # creates device handle (not device obj)
devs = ct.POINTER(ct.POINTER(usb.device))() # creates device structure
ep_data_out = (ct.c_ubyte*(EP1OUT_SIZE))()
ep_data_in = (ct.c_ubyte*(EP1IN_SIZE))()
bulk_transferred = ct.POINTER(ct.c_int)()	

#
# inits
#
device_configuration.contents = ct.c_int(0)
bulk_transferred.contents = ct.c_int(0)

def run():
	# open usb library
	r = usb.init(None)
	if r < 0:
		print(f'usb init failure: {r}')
		return -1

	# get list of USB devices
	cnt = usb.get_device_list(None, ct.byref(devs))
	# error check
	if cnt < 0:
		print(f'get device list failure: {cnt}')
		return -1

	print("\n[Getting USB device list]")
	# Check all USB devices for VID/PID match
	i = 0
	while devs[i]:
		dev = devs[i]

		# get device descriptor information
		desc = usb.device_descriptor()
		r = usb.get_device_descriptor(dev, ct.byref(desc))
		# error check
		if r < 0:
			print(f'failed to get device descriptor: {r}')
			return -1

		# print usb device info for each device
		print("{:04x}:{:04x} (bus {:d}, device {:d})\n".format(
			  desc.idVendor, desc.idProduct, 
			  usb.get_bus_number(dev), usb.get_device_address(dev)), end="")


		if(desc.idVendor == DEF_VID) and (desc.idProduct == DEF_PID):
			# print all member info for descriptor structure for target device
			print('\n[Descriptor Inforamtion]')
			print(f"{'bLength: ':.<30}{f'{desc.bLength:#02x}':.>20}")
			print(f"{'bDescriptorType: ':.<30}{f'{desc.bDescriptorType:#02x}':.>20}")
			print(f"{'bcdUSB: ':.<30}{f'{desc.bcdUSB:#04x}':.>20}")
			print(f"{'bDeviceClass: ':.<30}{f'{desc.bDeviceClass:#02x}':.>20}")
			print(f"{'bDeviceSubClass: ':.<30}{f'{desc.bDeviceSubClass:#02x}':.>20}")
			print(f"{'bDeviceProtocol: ':.<30}{f'{desc.bDeviceProtocol:#02x}':.>20}")
			print(f"{'bMaxPacketSize0: ':.<30}{f'{desc.bMaxPacketSize0:#02x}':.>20}")
			print(f"{'idVendor: ':.<30}{f'{desc.idVendor:#02x}':.>20}")
			print(f"{'idProduct: ':.<30}{f'{desc.idProduct:#02x}':.>20}")
			print(f"{'bcdDevice: ':.<30}{f'{desc.bcdDevice:#02x}':.>20}")
			print(f"{'iManufacturer: ':.<30}{f'{desc.iManufacturer:#02x}':.>20}")
			print(f"{'iProduct: ':.<30}{f'{desc.iProduct:#02x}':.>20}")
			print(f"{'iSerialNumber: ':.<30}{f'{desc.iSerialNumber:#02x}':.>20}")
			print(f"{'bNumConfigurations: ':.<30}{f'{desc.bNumConfigurations:#02x}':.>20}")
			dev_found = True		
			break

		i += 1


	#
	# open device if matching vid/pid was found
	#
	if(dev_found == True):

		r = usb.open(dev, dev_handle)
		# error check
		if r < 0:
			print(f"ret val: {r} - {usb.strerror(r)}")
			print("failed to open device!")
			return -1

		#
		# Get device string information
		#
		r = usb.get_string_descriptor(dev_handle, desc.iSerialNumber, 0x409, sn_string, 18)
		r = usb.get_string_descriptor(dev_handle, desc.iProduct, 0x409, pd_string, 30)
		r = usb.get_string_descriptor(dev_handle, desc.iManufacturer, 0x409, mf_string, 26)
		
		#
		# Print bridge string information
		#
		# utf-16 decoding
		# skip first two bytes b/c they are USB protocol specific not SN
		#
		print('\n')
		sn_string_d = bytes(sn_string)[2:].decode("utf-16") # type - string
		pd_string_d = bytes(pd_string)[2:].decode("utf-16") # type - string
		mf_string_d = bytes(mf_string)[2:].decode("utf-16") # type - string

		print("[String descriptor info]")
		print(f"{'Manufacturer Description: ':.<30}{mf_string_d:.>20}")		
		print(f"{'Product Description: ':.<30}{pd_string_d:.>20}")
		print(f"{'Serial Number: ':.<30}{sn_string_d:.>20}")
		


		#
		# get additional device endpoint/configuration information
		#
		print("\n[Endpoint Sizes]")
		ep_size = usb.get_max_packet_size(dev, 0x01)
		print(f"ep_out_size: {ep_size}")
		ep_size = usb.get_max_packet_size(dev, 0x81)
		print(f"ep_in_size: {ep_size}")
		print("\n[Configuration]")
		r = usb.get_configuration(dev_handle, device_configuration)
		print(f"r: {r}, configuration: {device_configuration.contents}")












		# -------------------------------------------------------------------
		print('\n\n\n===================================')
		print('[Register Read Transaction]')

		# claim interface 0 - register access
		r = usb.claim_interface(dev_handle, 0)
		# error check
		if(r != 0):
			print(f'ERROR: failed to claim interface, ret val = {r}')
			print(f"ERROR: code - {usb.strerror(r)}")


		# --------------------------------------
		# Handle Transmit Case
		# --------------------------------------
		ep_data_out[0] = 0x24	# r/w flag

		ep_data_out[1] = 20	# reg addres (32-bit value)
		ep_data_out[2] = 0
		ep_data_out[3] = 0
		ep_data_out[4] = 0

		# execute read transaction
		r = usb.bulk_transfer(dev_handle, ENDPOINT1_OUT, ep_data_out, 
								EP1OUT_SIZE, bulk_transferred, EP1OUT_TIMEOUT)	
		print(f'Transferred {bulk_transferred.contents} bytes!')



		# --------------------------------------
		# Handle Receive Case
		# --------------------------------------

		# execute write transaction
		r = usb.bulk_transfer(dev_handle, ENDPOINT1_IN, ep_data_in, 
								EP1IN_SIZE, bulk_transferred, EP1IN_TIMEOUT)	
		# error check
		if (r < 0):
			print(f'ERROR: Total bytes transferred <{bulk_transferred.contents}> bytes!')
			print(f'ERROR: Expected to xfer <{EP1IN_SIZE}> bytes!')
			print(f'ERROR: bulk_transfer() ret code <{r}> bytes!')
			return -1
		else:	
			print(f'Transferred {bulk_transferred.contents} bytes!')



		# print read result
		rd_val = ep_data_in[2] + (ep_data_in[3] << 8) + (ep_data_in[4] << 16) + (ep_data_in[5] << 24)
		print(f"{'Header: ':.<30}{f'{ep_data_in[0]:#02x}':.>20}")
		print(f"{'Category: ':.<30}{f'{ep_data_in[1]:#02x}':.>20}")
		print(f"{'reg_value: ':.<30}{f'{rd_val:#08x}':.>20}")





#
# Run module
#
run()






