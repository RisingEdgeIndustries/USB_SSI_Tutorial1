# Project Name:
# tutorial p1 - descriptor and reg space query
#
# Project Description:
# ----------------------
# This module (tutorial 1 part1) opens a connection to the USB 
# SSI bridge and reads the descriptor information and the entire
# configuration register space of the bridge.
#
#
# TODO:
# ----------------------
#
#
# ----------------------------------------------------------------
# Project Notes:
# ----------------------------------------------------------------
# 1. The REIndustries library comes with a logger. The user can pass
# 	a filename for the file logger into the library which is done
# 	here.
#


from USB_SSI_Libs.rei_usb_lib import USB20F_Device



# for logger
log_file_name = "tst_dump-regs"

# open USB lib
usb_dev0 = USB20F_Device(quiet=True, name=log_file_name)
usb_dev0.open_usb()

# read and print all configuration register info
usb_dev0.dump_regspace()

# read and print all USB descriptor info
usb_dev0.dump_descriptors()

# close brige USB library
usb_dev0.close_usb()


