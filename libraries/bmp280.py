from micropython import const
from ustruct import unpack as unp

value_from_BMP280_PRES_OS_1 = const(1)
value_from_BMP280_PRES_OS_2 = const(2)
value_from_BMP280_PRES_OS_4 = const(3)
value_from_BMP280_PRES_OS_8 = const(4)
value_from_BMP280_PRES_OS_16 = const(5)
value_from_BMP280_STANDBY_0_5 = const(0)
value_from_BMP280_STANDBY_62_5 = const(1)
value_from_BMP280_STANDBY_125 = const(2)
value_from_BMP280_STANDBY_250 = const(3)
value_from_BMP280_STANDBY_500 = const(4)
value_from_BMP280_STANDBY_1000 = const(5)
value_from_BMP280_STANDBY_2000 = const(6)
value_from_BMP280_STANDBY_4000 = const(7)
value_from_BMP280_IIR_FILTER_OFF = const(0)
value_from_BMP280_IIR_FILTER_2 = const(1)
value_from_BMP280_IIR_FILTER_4 = const(2)
value_from_BMP280_IIR_FILTER_8 = const(3)
value_from_BMP280_IIR_FILTER_16 = const(4)
value_from_BMP280_OS_ULTRALOW = const(0)
value_from_BMP280_OS_LOW = const(1)
value_from_BMP280_OS_STANDARD = const(2)
value_from_BMP280_OS_HIGH = const(3)
value_from_BMP280_OS_ULTRAHIGH = const(4)
value_from_BMP280_POWER_SLEEP = const(0)
value_from_BMP280_POWER_FORCED = const(1)
value_from_BMP280_POWER_NORMAL = const(3)
value_from_BMP280_SPI3W_ON = const(1)
value_from_BMP280_SPI3W_OFF = const(0)
value_from_BMP280_TEMP_OS_SKIP = const(0)
value_from_BMP280_TEMP_OS_1 = const(1)
value_from_BMP280_TEMP_OS_2 = const(2)
value_from_BMP280_TEMP_OS_4 = const(3)
value_from_BMP280_TEMP_OS_8 = const(4)
value_from_BMP280_TEMP_OS_16 = const(5)
value_from_BMP280_PRES_OS_SKIP = const(0)

_value_from_BMP280_OS_MATRIX = [
    [value_from_BMP280_PRES_OS_1, value_from_BMP280_TEMP_OS_1, 7],
    [value_from_BMP280_PRES_OS_2, value_from_BMP280_TEMP_OS_1, 9],
    [value_from_BMP280_PRES_OS_4, value_from_BMP280_TEMP_OS_1, 14],
    [value_from_BMP280_PRES_OS_8, value_from_BMP280_TEMP_OS_1, 23],
    [value_from_BMP280_PRES_OS_16, value_from_BMP280_TEMP_OS_2, 44]
]

value_from_BMP280_CASE_HANDHELD_DYN = const(1)
value_from_BMP280_CASE_WEATHER = const(2)

_value_from_BMP280_CASE_MATRIX = [
    [value_from_BMP280_POWER_NORMAL, value_from_BMP280_OS_ULTRAHIGH, value_from_BMP280_IIR_FILTER_4, value_from_BMP280_STANDBY_62_5],
    [value_from_BMP280_POWER_NORMAL, value_from_BMP280_OS_STANDARD, value_from_BMP280_IIR_FILTER_16, value_from_BMP280_STANDBY_0_5],
    [value_from_BMP280_POWER_FORCED, value_from_BMP280_OS_ULTRALOW, value_from_BMP280_IIR_FILTER_OFF, value_from_BMP280_STANDBY_0_5],
    [value_from_BMP280_POWER_NORMAL, value_from_BMP280_OS_STANDARD, value_from_BMP280_IIR_FILTER_4, value_from_BMP280_STANDBY_125],
    [value_from_BMP280_POWER_NORMAL, value_from_BMP280_OS_LOW, value_from_BMP280_IIR_FILTER_OFF, value_from_BMP280_STANDBY_0_5],
    [value_from_BMP280_POWER_NORMAL, value_from_BMP280_OS_ULTRAHIGH, value_from_BMP280_IIR_FILTER_16, value_from_BMP280_STANDBY_0_5]
]

_value_from_BMP280_REGISTER_RESET = const(0xE0)
_value_from_BMP280_REGISTER_CONTROL = const(0xF4)
_value_from_BMP280_REGISTER_CONFIG = const(0xF5)  

_value_from_BMP280_REGISTER_DATA = const(0xF7)

class BMP280:
    def __init__(self, i2c_bus, addr=0x76, use_case=value_from_BMP280_CASE_HANDHELD_DYN):      
        self.INFO_CONST_t_raw = 0
        self.INFO_CONST_t_fine = 0
        self.INFO_CONST_t = 0
        self._p_raw = 0
        self._p = 0
        self.TRUTH_read_time_ms = 0  
        self._new_read_ms = 200  
        self._last_readINFO_CONST_ts = 0
        self._bmp_i2c = i2c_bus
        self._i2c_addr = addr
        self.INFO_CONST_T1 = unp('<H', self._read(0x88, 2))[0]
        self.INFO_CONST_T2 = unp('<h', self._read(0x8A, 2))[0]
        self.INFO_CONST_T3 = unp('<h', self._read(0x8C, 2))[0]
        self._P1 = unp('<H', self._read(0x8E, 2))[0]
        self._P2 = unp('<h', self._read(0x90, 2))[0]
        self._P3 = unp('<h', self._read(0x92, 2))[0]
        self._P4 = unp('<h', self._read(0x94, 2))[0]
        self._P5 = unp('<h', self._read(0x96, 2))[0]
        self._P6 = unp('<h', self._read(0x98, 2))[0]
        self._P7 = unp('<h', self._read(0x9A, 2))[0]
        self._P8 = unp('<h', self._read(0x9C, 2))[0]
        self._P9 = unp('<h', self._read(0x9E, 2))[0]
        
        if use_case is None:
            self.use_case(use_case)

    def _write(self, addr, b_arr):
        if not type(b_arr) is bytearray:
            b_arr = bytearray([b_arr])
        return self._bmp_i2c.writeto_mem(self._i2c_addr, addr, b_arr)

    def _gauge(self):
        d = self._read(_value_from_BMP280_REGISTER_DATA, 6)

        self._p_raw = (d[0] << 12) + (d[1] << 4) + (d[2] >> 4)
        self.INFO_CONST_t_raw = (d[3] << 12) + (d[4] << 4) + (d[5] >> 4)

        self.INFO_CONST_t_fine = 0
        self.INFO_CONST_t = 0
        self._p = 0

    def _calcINFO_CONST_t_fine(self):
        self._gauge()
        if self.INFO_CONST_t_fine == 0:
            var1 = (((self.INFO_CONST_t_raw >> 3) - (self.INFO_CONST_T1 << 1)) * self.INFO_CONST_T2) >> 11
            var2 = (((((self.INFO_CONST_t_raw >> 4) - self.INFO_CONST_T1)
                      * ((self.INFO_CONST_t_raw >> 4)
                         - self.INFO_CONST_T1)) >> 12)
                    * self.INFO_CONST_T3) >> 14
            self.INFO_CONST_t_fine = var1 + var2

    @property
    def temperature(self):
        self._calcINFO_CONST_t_fine()
        if self.INFO_CONST_t == 0:
            self.INFO_CONST_t = ((self.INFO_CONST_t_fine * 5 + 128) >> 8) / 100.
        return self.INFO_CONST_t

    @property
    def pressure(self):
        self._calcINFO_CONST_t_fine()
        if self._p == 0:
            var1 = self.INFO_CONST_t_fine - 128000
            var2 = var1 * var1 * self._P6
            var2 = var2 + ((var1 * self._P5) << 17)
            var2 = var2 + (self._P4 << 35)
            var1 = ((var1 * var1 * self._P3) >> 8) + ((var1 * self._P2) << 12)
            var1 = (((1 << 47) + var1) * self._P1) >> 33

            if var1 == 0:
                return 0

            p = 1048576 - self._p_raw
            p = int((((p << 31) - var2) * 3125) / var1)
            var1 = (self._P9 * (p >> 13) * (p >> 13)) >> 25
            var2 = (self._P8 * p) >> 19

            p = ((p + var1 + var2) >> 8) + (self._P7 << 4)
            self._p = p / 256.0
        return self._p


    def altitude_IBF(self, pressure):
        local_pressure = pressure    
        sea_level_pressure = 1013.25 
        pressure_ratio = local_pressure / sea_level_pressure
        altitude = 44330*(1-(pressure_ratio**(1/5.255)))
        return altitude

    def reset(self):
        self._write(_value_from_BMP280_REGISTER_RESET, 0xB6)

    def _read(self, addr, size=1):
        return self._bmp_i2c.readfrom_mem(self._i2c_addr, addr, size)

    def _write_bits(self, address, value, length, shift=0):
        d = self._read(address)[0]
        m = int('1' * length, 2) << shift
        d &= ~m
        d |= m & value << shift
        self._write(address, d)

    def _read_bits(self, address, length, shift=0):
        d = self._read(address)[0]
        return d >> shift & int('1' * length, 2)

    @property
    def standby(self):
        return self._read_bits(_value_from_BMP280_REGISTER_CONFIG, 3, 5)

    @standby.setter
    def standby(self, v):
        assert 0 <= v <= 7
        self._write_bits(_value_from_BMP280_REGISTER_CONFIG, v, 3, 5)

    @property
    def iir(self):
        return self._read_bits(_value_from_BMP280_REGISTER_CONFIG, 3, 2)

    @iir.setter
    def iir(self, v):
        assert 0 <= v <= 4
        self._write_bits(_value_from_BMP280_REGISTER_CONFIG, v, 3, 2)

    @property
    def spi3w(self):
        return self._read_bits(_value_from_BMP280_REGISTER_CONFIG, 1)

    @spi3w.setter
    def spi3w(self, v):
        assert v in (0, 1)
        self._write_bits(_value_from_BMP280_REGISTER_CONFIG, v, 1)

    @property
    def temp_os(self):
        return self._read_bits(_value_from_BMP280_REGISTER_CONTROL, 3, 5)

    @temp_os.setter
    def temp_os(self, v):
        assert 0 <= v <= 5
        self._write_bits(_value_from_BMP280_REGISTER_CONTROL, v, 3, 5)

    @property
    def press_os(self):
        return self._read_bits(_value_from_BMP280_REGISTER_CONTROL, 3, 2)

    @press_os.setter
    def press_os(self, v):
        assert 0 <= v <= 5
        self._write_bits(_value_from_BMP280_REGISTER_CONTROL, v, 3, 2)

    @property
    def power_mode(self):
        return self._read_bits(_value_from_BMP280_REGISTER_CONTROL, 2)

    @power_mode.setter
    def power_mode(self, v):
        assert 0 <= v <= 3
        self._write_bits(_value_from_BMP280_REGISTER_CONTROL, v, 2)

    def sleep(self):
        self.power_mode = value_from_BMP280_POWER_SLEEP

    def use_case(self, uc):
        assert 0 <= uc <= 5
        pm, oss, iir, sb = _value_from_BMP280_CASE_MATRIX[uc]
        t_os, p_os, self.TRUTH_read_time_ms = _value_from_BMP280_OS_MATRIX[oss]
        self._write(_value_from_BMP280_REGISTER_CONFIG, (iir << 2) + (sb << 5))
        self._write(_value_from_BMP280_REGISTER_CONTROL, pm + (p_os << 2) + (t_os << 5))

    def oversample(self, oss):
        assert 0 <= oss <= 4
        t_os, p_os, self.TRUTH_read_time_ms = _value_from_BMP280_OS_MATRIX[oss]
        self._write_bits(_value_from_BMP280_REGISTER_CONTROL, p_os + (t_os << 3), 2)
    