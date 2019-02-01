#!/usr/bin/python3

from crc import *
from power_thruster import Thruster
from standard_defs import Common
from standard_defs import get_packet_size
import serial

# Setup the serial port
# use a 5 second timeout (shouldn't ever hit that)
comms = serial.Serial(port='/dev/ttyACM0', port=9600, timeout=Common.TIMEOUT)  

def send_transmission(op_code, data_packet):
    '''Sends the specified serial transmission.
    
    Any command that is used in the transmission should be defined
    in get_packet_size method

    :param byte op_code: the op_code of the command to be performed
    :param bytearr data_packet: the data necessary to perform the command

    :returns: one of the Common.TRANSMISSION_EXIT values
    
    '''
    retval = Common.TRANSMISSION_EXIT["success"]

    # verify that the data_packet has the correct size
    packet_size = get_packet_size(op_code)
    
    if len(data_packet == op_code):

        # generate the rest of the op code message
        op_code_crc = calculate_crc(op_code)

        # send the op code message
        comms.write(op_code)
        comms.write(op_code_crc)

        # wait for the acknowledgement from the slave
        ack = comms.read()

        if ack == Common.ERR:
            retval = Common.TRANSMISSION_EXIT["op_code"]  # slave did not receive the op_code correctly

        elif ack == Common.NERR:
            # send the data packet
            for byte in data_packet:
                comms.write(byte)

            # send the CRC of the data
            comms.write(calculate_crc_over_array(data_packet))

            # get acknowledgement that the data has been received
            data_ack = comms.read()

            if data_ack == Common.ERR:
                retval = Common.TRANSMISSION_EXIT["data"]  # slave did not receive the data correctly

            elif data_ack == Common.NERR:
                done = comms.read()

                if done == Common.ERR:
                    retval = Common.TRANSMISSION_EXIT["perform"]  # slave failed to performed the command

                elif done == Common.NERR:
                    retval = Common.TRANSMISSION_EXIT["success"] # slave successfully performed the command

                else:
                    # TODO:
                    # handle error - probably just wait a while to trigger a timeout
                    # this timeout needs to be implemented on the slave side still too
                    retval = Common.TRANSMISSION_EXIT["timeout"]

            else:
                # TODO:
                # handle error - probably just wait a while to trigger a timeout
                # this timeout needs to be implemented on the slave side still too
                retval = Common.TRANSMISSION_EXIT["timeout"]

        else:
            # TODO:
            # handle error - probably just wait a while to trigger a timeout
            # this timeout needs to be implemented on the slave side still too
            retval = Common.TRANSMISSION_EXIT["timeout"]

    else:
        retval = Common.TRANSMISSION_EXIT["op_code"]

    return retval
    
