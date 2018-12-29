#include <SoftwareSerial.h>
#include <stdint.h>
#include <stdbool.h>
#include "crc.h"

const static int BAUD_RATE = 9600;

// UART pin defs
const static int RX = 10;
const static int TX = 11;

// UART OP Codes
const static uint8_t WRITE_SERVO_OP = 0x01;

// UART data packet sizes
const static uint8_t WRITE_SERVO_PACKET_SIZE = 1;

// return codes
const static uint8_t NERR = 0xFF;
const static uint8_t ERR = 0x00;
const static uint8_t DONE = NERR;

SoftwareSerial comms(RX,TX);

void uart_transmission(void);
uint8_t get_packet_size(uint8_t op_code);
bool perform_command(uint8_t data[], uint8_t data_length);

void setup() 
{
    // setup the UART
    comms.begin(BAUD_RATE);

    // setup the debug output
    Serial.begin(BAUD_RATE);
    while (!Serial) 
    {
        ; // wait for serial port to connect. Needed for native USB port only
    }
}

void loop() 
{
    uart_transmission();
}

/**
 * Gets the size of the packet corresponding to the OP Code
 * 
 * @param op_code the command to look up the packet size
 * 
 * @returns the size in bytes of the OP Code or -1 if the OP Code is not defined
 */
uint8_t get_packet_size(uint8_t op_code) 
{
    uint8_t packet_size = -1;

    switch (op_code) 
    {
        case WRITE_SERVO_OP:
            packet_size = WRITE_SERVO_PACKET_SIZE;
            break;

        // received an invalid OP Code
        default:
            packet_size = -1;
            break;
    }

    return packet_size;
}

/**
 * Perform the specified command.
 * 
 * @param op_code     the command to perform
 * @param data        the data that is needed to perform the command
 * @param data_length the length of the data packet
 * 
 * @returns           True if the OP Code was valid and the command succeeded, false otherwise
 */
bool perform_command(uint8_t op_code, uint8_t data[], uint8_t data_length) 
{
    bool retval = true;

    switch(op_code) 
    {
        case WRITE_SERVO_OP:
            retval = true;
            break;
        
        // recevied and invalid OP Code
        default:
            retval = false;
            break;
    }

    return retval;
}

/**
 * Performs a UART transmission.
 * 
 * Any command that is used in the transmission should be defined in the above perform_command and get_packet_size methods
 * This method should be the same for all UART transmissions
 */
void uart_transmission()
{
    // wait for the op code
    uint8_t op_code = comms.read();
    uint8_t op_code_crc = comms.read();

    // make sure the CRC is correct to ensure data integrity
    if (check_crc(op_code, op_code_crc)) 
    {
        uint8_t packet_size = get_packet_size(op_code);
        // read the data packet if there is one and response with acknowledgement on end
        if (packet_size > 0) 
        {
            uint8_t data_packet[packet_size];

            // get all the data from the master to perform the command
            for (uint8_t i = 0; i < packet_size; i++) 
            {
                data_packet[i] = comms.read();
            }

            // read the CRC
            uint8_t crc = comms.read();
            
            // check the data packet integrity
            if (check_crc_over_array(data_packet, packet_size, crc)) 
            {
                // send back acknowledgement the data has been received
                comms.write(NERR);

                // perform the command
                bool result = perform_command(op_code, data_packet, packet_size);

                // report the result of the command after finishing
                if (result) 
                {
                    comms.write(DONE);
                }
                else
                {
                    comms.write(ERR);
                }
            }
            // if the crc does not match, repotr an error
            else
            {
                comms.write(ERR);
            }
        }
        // if there was no data to go along with the command
        else if (packet_size == 0) 
        {
            // perform the command
            bool result = perform_command(op_code, NULL, 0);

            // report the result of the command after finishing
            if (result) 
            {
                comms.write(DONE);
            }
            else
            {
                comms.write(ERR);
            }
        }
        // if the command was invalid
        else 
        {
            comms.write(ERR);
        }
    }
    // if the OP Code CRC is incorrect, report an error
    else 
    {
        comms.write(ERR);
    }
}