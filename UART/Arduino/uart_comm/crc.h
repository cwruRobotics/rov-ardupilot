#ifndef CRC_H
#define CRC_H

#include <stdint.h>
#include <stdbool.h>

uint8_t calculate_crc(uint8_t data);

uint8_t calculate_crc_over_array(uint8_t data[], uint32_t length);

bool check_crc(uint8_t data, uint8_t crc);

bool check_crc_over_array(uint8_t data[], uint32_t length, uint8_t crc);

#endif