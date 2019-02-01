class Common():
    # OP Codes
    WRITE_SERVO_OP = 0x00
    LEFT_THRUSTER_ON_OP = 0x01
    LEFT_THRUSTER_OFF_OP = 0x02
    RIGHT_THRUSTER_ON_OP = 0x03
    RIGHT_THRUSTER_OFF_OP = 0x04
    BOTH_THRUSTER_ON_OP = 0x05
    BOTH_THRUSTER_OFF_OP = 0x06

    # data packet sizes
    WRITE_SERVO_PACKET_SIZE = 1
    LEFT_THRUSTER_ON_PACKET_SIZE = 1
    LEFT_THRUSTER_OFF_PACKET_SIZE = 1
    RIGHT_THRUSTER_ON_PACKET_SIZE = 1
    RIGHT_THRUSTER_OFF_PACKET_SIZE = 1
    BOTH_THRUSTER_ON_PACKET_SIZE = 1
    BOTH_THRUSTER_OFF_PACKET_SIZE = 1

    # Error/Success codes
    NERR = 0xFF
    ERR = 0x00
    DONE = NERR

    TIMEOUT = 5.0

    # transmission return codes
    TRANSMISSION_EXIT = {
        "success": 0,
        "op_code": 1,
        "data": 2,
        "perform": 3,
        "timeout": 4
    }


def get_packet_size(op_code):
    '''Gets the size of the packet corresponding to the OP Code
    
    :param int op_code: the command to look up the packet size
 
    :returns: the size in bytes of the OP Code or -1 if the OP Code is not defined

    '''

    switcher = {
        Common.WRITE_SERVO_OP: Common.WRITE_SERVO_PACKET_SIZE,
        Common.LEFT_THRUSTER_ON_OP: Common.LEFT_THRUSTER_ON_PACKET_SIZE,
        Common.LEFT_THRUSTER_OFF_OP: Common.LEFT_THRUSTER_OFF_PACKET_SIZE,
        Common.RIGHT_THRUSTER_ON_OP: Common.RIGHT_THRUSTER_ON_PACKET_SIZE,
        Common.RIGHT_THRUSTER_OFF_OP: Common.RIGHT_THRUSTER_OFF_PACKET_SIZE,
        Common.BOTH_THRUSTER_ON_OP: Common.BOTH_THRUSTER_ON_PACKET_SIZE,
        Common.BOTH_THRUSTER_OFF_OP: Common.BOTH_THRUSTER_OFF_PACKET_SIZE
    }

    return switcher.get(op_code, -1)