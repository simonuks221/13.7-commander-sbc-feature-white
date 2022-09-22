from serial import Serial
from struct import pack, unpack
from enum import IntEnum
from typing import Optional
from time import time

DEBUG = True

MAX_RETRIES = 3

baud_rates = [
    115200,  # (default)
    230400,
    460800,
    576000,
    921600,
    960000,
    1000000,
    1200000,
    1500000,
    2000000,
    3000000,
    6000000
]


class ResponseStatus(IntEnum):
    OK = 0
    ERROR = 1
    TIMEOUT = 2


class CMD(IntEnum):
    ERROR = 0x00
    OK = 0x01
    ASCII = 0x02
    SET_TIME = 0x03
    CHANGE_BAUDRATE = 0x04
    GET_TEMPERATURE = 0x05
    GET_SUPPLY_VOLTAGE = 0x06

    ENABLE_MOTOR = 0x10
    DISABLE_MOTOR = 0x11
    SET_MOTOR = 0x12
    MOVE_SERVO = 0x13

    ENABLE_RGBW = 0x20
    DISABLE_RGBW = 0x21
    UPDATE_RGBW = 0x22
    SET_RGBW = 0x23

    ENABLE_ARGB = 0x30
    DISABLE_ARGB = 0x31
    UPDATE_ARGB = 0x32
    SET_ARGB = 0x33
    DIM_ARGB = 0x34
    GRADIENT_ARGB = 0x35

    ENABLE_IO = 0x40
    DISABLE_IO = 0x41
    READ_IO = 0x42
    SET_IO = 0x43

    ENABLE_WEIGHT_SENSOR = 0x50
    DISABLE_WEIGHT_SENSOR = 0x51
    RECALIBRATE_WEIGHT_SENSOR = 0x52
    READ_WEIGHT_SENSOR = 0x53

    ENABLE_DISTANCE_SENSOR = 0x60
    DISABLE_DISTANCE_SENSOR = 0x61
    RECALIBRATE_DISTANCE_SENSOR = 0x62
    READ_DISTANCE_SENSOR = 0x63

    ENABLE_ANALOG = 0x70
    DISABLE_ANALOG = 0x71
    READ_ANALOG = 0x72


def write_cmd(s: Serial, address: int, cmd: CMD, data: Optional[bytes]):
    payload = pack("2B", address, cmd)
    if data:
        payload += data
    s.write(payload)
    s.flushOutput()


def check_cmd_status(s: Serial, expected_cmd: CMD) -> ResponseStatus:
    response = s.read(2)
    if len(response) != 2:
        return ResponseStatus.TIMEOUT

    response_device, status = unpack("2B", response)
    if response_device == 0 and status == expected_cmd:
        return ResponseStatus.OK
    else:
        return ResponseStatus.ERROR


def send_cmd(
    s: Serial, address: int, cmd: CMD,
    data: Optional[bytes] = None,
    expected_status: CMD = CMD.OK,
    retries: int = MAX_RETRIES,
    skip_response: bool = False
) -> ResponseStatus:
    status = ResponseStatus.ERROR
    for _ in range(retries):
        s.reset_input_buffer()
        write_cmd(s, address, cmd, data)

        if skip_response or address == 255:
            return ResponseStatus.OK

        status = check_cmd_status(s, expected_status)
        if status == ResponseStatus.OK:
            return ResponseStatus.OK
    return status

# System commands


def send_ascii_cmd(s: Serial, address: int, cmd: str):
    """ Allows communicating with the controller in ASCII formatted CLI commands """
    return send_cmd(s, address,
                    CMD.ASCII,
                    cmd.encode("ascii"),
                    skip_response=True
                    )


def set_time(s: Serial, address: int, timestamp: int):
    """ Updates current time """
    return send_cmd(s, address,
                    CMD.SET_TIME,
                    pack(">Q", timestamp)
                    )


def sync_time(s: Serial, address: int) -> ResponseStatus:
    """ Sync current time """
    return set_time(s, address, round(time() * 1000))


def change_baudrate(s: Serial, address: int, baudrate: int):
    """ Changes communication speed """
    return send_cmd(s, address,
                    CMD.CHANGE_BAUDRATE,
                    pack(">B", baudrate)
                    )


def get_temperature(s: Serial, address: int) -> tuple[ResponseStatus, int]:
    """ Gets the controller temperature """
    status = send_cmd(s, address, CMD.GET_TEMPERATURE)
    if status != ResponseStatus.OK:
        return (status, -1)

    temperature = unpack("B", s.read())[0]
    return (status, temperature)


def get_supply_voltage(s: Serial, address: int) -> tuple[ResponseStatus, int]:
    """ Gets the supply voltage value of the controller """
    status = send_cmd(s, address, CMD.GET_SUPPLY_VOLTAGE)
    if status != ResponseStatus.OK:
        return (status, -1)

    temperature = unpack("B", s.read())[0]
    return (status, temperature)


def ping(s: Serial, address: int):
    """ Test connection to controller """
    return send_cmd(s, address, CMD.OK, retries=1)


def assert_controllers(s: Serial, start_address: int, end_address: int):
    for address in range(start_address, end_address+1):
        status = ping(s, address)
        assert status == ResponseStatus.OK, f"Failed to ping controller 0x{address:02X}"

# Motor commands


def enable_motor(s: Serial, address: int, port: int):
    """ Enables motors and servos """
    return send_cmd(s, address,
                    CMD.ENABLE_MOTOR,
                    pack(">B", port)
                    )


def disable_motor(s: Serial, address: int, port: int):
    """ Disables motors and servos """
    return send_cmd(s, address,
                    CMD.DISABLE_MOTOR,
                    pack(">B", port)
                    )


def set_motor(s: Serial, address: int, port: int, speed: int, direction: bool):
    """ Sets motor speed and direction """
    return send_cmd(s, address,
                    CMD.SET_MOTOR,
                    pack(">2B?", port, speed, direction)
                    )


def move_servo(s: Serial, address: int, port: int, start: int, end: int, timestamp: int, duration: int):
    """ Moves servo shaft position in provided time interval """
    return send_cmd(s, address,
                    CMD.MOVE_SERVO,
                    pack(">3BQH", port, start, end, timestamp, duration)
                    )

# RGBW LED strip commands


def enable_rgbw(s: Serial, address: int, port: int):
    """ Enables RGBW LED strips """
    return send_cmd(s, address,
                    CMD.ENABLE_RGBW,
                    pack(">B", port)
                    )


def disable_rgbw(s: Serial, address: int, port: int):
    """ Disables RGBW LED strips """
    return send_cmd(s, address,
                    CMD.DISABLE_RGBW,
                    pack(">B", port)
                    )


def set_rgbw(
    s: Serial,
    address: int, port: int,
    r: int, g: int, b: int, w: int
):
    """ Sets the RGBW color to the LED strips """
    return send_cmd(s, address,
                    CMD.SET_RGBW,
                    pack("5B", port, r, g, b, w)
                    )


def update_rgbw(s: Serial, address: int):
    """ Updates RGBW LED strips """
    return send_cmd(s, address, CMD.UPDATE_RGBW)


def update_all_rgbw(s: Serial):
    """ Updates RGBW LED strips """
    return send_cmd(s, 255, CMD.UPDATE_RGBW)


def clear_rgbw(s: Serial, address: int, port: int):
    return set_rgbw(s, address, port, 0, 0, 0, 0)


def clear_all_rgbw(s: Serial):
    send_cmd(s, 255,
             CMD.SET_RGBW,
             pack("5B", 0, 0, 0, 0, 0)
             )
    send_cmd(s, 255,
             CMD.SET_RGBW,
             pack("5B", 1, 0, 0, 0, 0)
             )

# ARGB LED strip commands


def enable_argb(s: Serial, address: int, port: int, pixel_count: int):
    """ Enables ARGB LED strips """
    return send_cmd(s, address,
                    CMD.ENABLE_ARGB,
                    pack(">BH", port, pixel_count)
                    )


def disable_argb(s: Serial, address: int, port: int):
    """ Disables ARGB LED strips """
    return send_cmd(s, address,
                    CMD.DISABLE_ARGB,
                    pack(">B", port)
                    )


def set_argb(
    s: Serial, address: int, port: int,
    start_pixel: int, end_pixel: int,
    r: int, g: int, b: int
):
    """ Sets the RGB color to all the pixels on ARGB LED strips """
    return send_cmd(s, address,
                    CMD.SET_ARGB,
                    pack(">BHH3B", port, start_pixel, end_pixel, r, g, b)
                    )


def set_white_argb(
    s: Serial, addr: int, port: int,
    start_pixel: int, end_pixel: int,
    grayscale: int
):
    return set_argb(s, addr, port, start_pixel, end_pixel, grayscale, grayscale, grayscale)


def dim_argb(
    s: Serial, address: int, port: int,
    start_pixel: int, end_pixel: int,
    amount: int
):
    """ Dims a segment of ARGB pixel buffer by specified ammount """
    return send_cmd(s, address,
                    CMD.DIM_ARGB,
                    pack(">BHHB", port, start_pixel, end_pixel, amount)
                    )


def set_gradient_argb(
    s: Serial, address: int, port: int,
    start_pixel: int, end_pixel: int,
    start_r: int, start_g: int, start_b: int,
    end_r: int, end_g: int, end_b: int,
    correction_index: int = 0
):
    """ Adds a specified gradient to the ARGB pixel buffer segment """
    return send_cmd(s, address,
                    CMD.GRADIENT_ARGB,
                    pack(">BBHH6B", port,
                         correction_index, start_pixel, end_pixel,
                         start_r, start_g, start_b,
                         end_r, end_g, end_b
                         )
                    )


def set_white_gradient_argb(
    s: Serial, address: int, port: int,
    start_pixel: int, end_pixel: int,
    start: int, end: int,
    correction_index: int = 0
):
    return set_gradient_argb(s, address, port,
                             start_pixel, end_pixel,
                             start, start, start,
                             end, end, end,
                             correction_index
                             )


def update_argb(s: Serial, address: int):
    """ Updates ARGB LED strips """
    return send_cmd(s, address, CMD.UPDATE_ARGB)


def update_all_argb(s: Serial):
    """ Updates ARGB LED strips """
    return send_cmd(s, 255, CMD.UPDATE_ARGB)


def clear_argb(s: Serial, address: int, port: int, pixel_count: int):
    return set_argb(s, address, port, 0, pixel_count-1, 0, 0, 0)

# IO commands


def enable_io(s: Serial, address: int, port: int, function: int):
    """ Enables IO ports """
    return send_cmd(s, address,
                    CMD.ENABLE_IO,
                    pack(">BB", port, function)
                    )


def disable_io(s: Serial, address: int, port: int):
    """ Disables IO ports """
    send_cmd(s, address,
             CMD.DISABLE_IO,
             pack(">B", port)
             )


def read_io(s: Serial, address: int, port: int) -> tuple[ResponseStatus, int]:
    """ Reads and returns states of IO ports """
    cmd = CMD.READ_IO
    status = send_cmd(s, address, cmd, pack(">B", port), expected_status=cmd)
    if status != ResponseStatus.OK:
        return (status, -1)

    response_port, io = unpack("B", s.read())
    assert response_port == port
    return (status, io)


def set_io(s: Serial, address: int, port: int, states: int):
    """ Sets states of IO ports """
    return send_cmd(s, address,
                    CMD.READ_IO,
                    pack(">2B", port, states)
                    )

# Weight sensor commands


def enable_weight_sensor(s: Serial, address: int, port: int):
    """ Enables weight sensors """
    return send_cmd(s, address,
                    CMD.ENABLE_WEIGHT_SENSOR,
                    pack(">B", port)
                    )


def disable_weight_sensor(s: Serial, address: int, port: int):
    """ Disables weight sensors """
    return send_cmd(s, address,
                    CMD.DISABLE_WEIGHT_SENSOR,
                    pack(">B", port)
                    )


def recalibrate_weight_sensor(s: Serial, address: int, port: int):
    """ Recalibrates the weight sensors """
    return send_cmd(s, address,
                    CMD.RECALIBRATE_WEIGHT_SENSOR,
                    pack(">B", port)
                    )


def read_weight_sensor(s: Serial, address: int, port: int) -> tuple[ResponseStatus, int]:
    """ Gets the current weight read by sensor """
    cmd = CMD.READ_IO
    status = send_cmd(s, address, cmd, pack("B", port), expected_status=cmd)
    if status != ResponseStatus.OK:
        return (status, -1)

    response_port, weight = unpack("BL", s.read(5))
    assert response_port == port
    return (status, weight)

# Distance sensor commands


def enable_distance_sensor(s: Serial, address: int, port: int):
    """ Enables distance sensors """
    return send_cmd(s, address,
                    CMD.ENABLE_DISTANCE_SENSOR,
                    pack(">B", port)
                    )


def disable_distance_sensor(s: Serial, address: int, port: int):
    """ Disables distance sensors """
    return send_cmd(s, address,
                    CMD.DISABLE_DISTANCE_SENSOR,
                    pack(">B", port)
                    )


def recalibrate_distance_sensor(s: Serial, address: int, port: int):
    """ Recalibrates distance sensors """
    return send_cmd(s, address,
                    CMD.RECALIBRATE_DISTANCE_SENSOR,
                    pack(">B", port)
                    )


def read_distance_sensor(s: Serial, address: int, port: int) -> tuple[ResponseStatus, int]:
    """ Gets the current distance read by sensor """
    cmd = CMD.READ_DISTANCE_SENSOR
    status = send_cmd(s, address, cmd, pack("B", port), expected_status=cmd)
    if status != ResponseStatus.OK:
        return (status, -1)

    response_port, distance = unpack("BH", s.read(3))
    assert response_port == port
    return (status, distance)

# Analog input commands


def enable_analog(s: Serial, address: int, port: int):
    """ Enables analog input """
    return send_cmd(s, address,
                    CMD.ENABLE_ANALOG,
                    pack(">B", port)
                    )


def disable_analog(s: Serial, address: int, port: int):
    """ Disables analog input """
    return send_cmd(s, address,
                    CMD.DISABLE_ANALOG,
                    pack(">B", port)
                    )


def read_analog(s: Serial, address: int, port: int) -> tuple[ResponseStatus, int]:
    """ Gets the current analog value read by ADC """
    cmd = CMD.READ_ANALOG
    status = send_cmd(s, address, cmd, pack("B", port), CMD.READ_ANALOG)
    if status != ResponseStatus.OK:
        return (status, -1)

    response_port, analog = unpack("BH", s.read(3))
    assert response_port == port
    return (status, analog)
