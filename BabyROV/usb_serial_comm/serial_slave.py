#!/usr/bin/python3

from crc import *
from power_thruster import Thruster
from standard_defs import Common
from standard_defs import get_packet_size
import serial

# Create the serial port
# use a 5 second timeout (shouldn't ever hit that)
comms = serial.Serial(port='/dev/ttyACM0', port=9600, timeout=Common.TIMEOUT)

left_thruster = Thruster(Thruster.LEFT)
right_thruster = Thruster(Thruster.RIGHT)

def perform_command(op_code, data):
    '''Perform the specified command.

    :param int op_code: the command to perform
    :param arr data:    the data that is needed to perform the command

    :returns: True if the OP Code was valid and the command succeeded, false otherwise

    '''

    retval = True

    if op_code == Common.WRITE_SERVO_OP:
        retval = True

    elif op_code == Common.LEFT_THRUSTER_ON_OP:
        retval = left_thruster.set_thruster(Thruster.ON)

    elif op_code == Common.LEFT_THRUSTER_OFF_OP:
        retval = left_thruster.set_thruster(Thruster.OFF)

    elif op_code == Common.RIGHT_THRUSTER_ON_OP:
        retval = right_thruster.set_thruster(Thruster.ON)

    elif op_code == Common.RIGHT_THRUSTER_OFF_OP:
        retval = right_thruster.set_thruster(Thruster.OFF)

    elif op_code == Common.BOTH_THRUSTER_ON_OP:
        retval = left_thruster.set_thruster(Thruster.ON) and \
                 right_thruster.set_thruster(Thruster.ON)          

    elif op_code == Common.BOTH_THRUSTER_OFF_OP:
        retval = left_thruster.set_thruster(Thruster.OFF) and \
                 right_thruster.set_thruster(Thruster.OFF)      

    # received and invalid OP Code
    else:
        retval = False

    return retval


def receive_transmission():
    '''Receives and performs the action received op_code.
    
    Any command that is used in the transmission should be defined in the above 
    perform_command and get_packet_size methods 

    :returns: one of the Common.TRANSMISSION_EXIT values
    
    '''
    retval = Common.TRANSMISSION_EXIT["success"]

    # wait for the op code
    op_code = comms.read()

    if op_code is None:
        return Common.TRANSMISSION_EXIT["timeout"]

    op_code_crc = comms.read()

    if op_code_crc is None:
        return Common.TRANSMISSION_EXIT["timeout"]

    # make sure the CRC is correct to ensure data integrity
    if check_crc(op_code, op_code_crc):
        packet_size = get_packet_size(op_code)

        # read the data packet if there is one and response with acknowledgement on end
        if packet_size > 0:
            data_packet = []

            # send back the acknowledgement that the op code has been received
            comms.write(Common.NERR)

            # get all the data from the master to perform the command
            for i in range(packet_size):
                byte = comms.read()

                # handle a timeout
                if byte is None:
                    # returning here because we want to stop getting data immediately
                    # so that we can start a new transmission
                    return Common.TRANSMISSION_EXIT["timeout"]
                else:
                    data_packet.append(byte)

            # read the CRC
            crc = comms.read()

            # handle timeout
            if crc is None:
                retval = Common.TRANSMISSION_EXIT["timeout"]
            
            # check the data packet integrity
            elif check_crc_over_array(data_packet, crc):
                # send back acknowledgement the data has been received
                comms.write(Common.NERR)

                # perform the command
                result = perform_command(op_code, data_packet)

                # report the result of the command after finishing
                if (result):
                    comms.write(Common.DONE)
                    retval = Common.TRANSMISSION_EXIT["success"]

                else:
                    comms.write(Common.ERR)
                    retval = Common.TRANSMISSION_EXIT["perform"]
                
            # if the crc does not match, repotr an error
            else:
                comms.write(Common.ERR)
                retval = Common.TRANSMISSION_EXIT["data"]
            
        # if there was no data to go along with the command
        elif (packet_size == 0):
            # send back the acknowledgement that the op code has been received
            comms.write(Common.NERR)

            # perform the command
            result = perform_command(op_code, None)

            # report the result of the command after finishing
            if (result):
                comms.write(Common.DONE)
                retval = Common.TRANSMISSION_EXIT["success"]
            
            else:
                comms.write(Common.ERR)
                retval = Common.TRANSMISSION_EXIT["perform"]
        
        # if the command was invalid
        else:
            comms.write(Common.ERR)
            retval = Common.TRANSMISSION_EXIT["op_code"]
        
    # if the OP Code CRC is incorrect, report an error
    else:    
        comms.write(Common.ERR)
        retval = Common.TRANSMISSION_EXIT["op_code"]
    
    return retval


if __name__ == "__main__":
    # TODO: add functionality that handles non success error codes
    while True:
        receive_transmission()