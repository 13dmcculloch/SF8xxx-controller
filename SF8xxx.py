# -*- coding: utf-8 -*-
"""
SF8xxx controller library

SF8xxx: control a board
Command classes: Set and Get things on/from board
Response: deals with response data

***NO NEGATIVE NUMBERS***

Created on Fri May 17 13:35:35 2024

@author: drm1g20
"""

import serial

class SF8xxx:
    """
    Object handling I/O to and from SF8xxx.
    """
    def __init__(self, port):
        self.port = port
        self.dev = serial.Serial(port, 115200, timeout=0.2)
        print("Opened", self.dev.name)
        self.serial_no = self.get_serial_no()
        
        self.driver_mask = self.get_driver_state()
        self.driver_off = True if self.driver_mask[3] & 0x2 else False
        
        self.tec_mask = self.get_tec_state()
        self.tec_off = True if self.tec_mask[3] & 0x2 else False
    
    
    def __del__(self):
        self.dev.close()
        
    
    def qrd(self):
        """
        Quick rundown: print important device stats
        """
        self.driver_on()
        print("\tCurrent:", str(self.get_driver_current()) + " mA")
        self.tec_on()
        print("\tTemp:", str(self.get_tec_temperature()) + " C")
        print("\tCurrent:", str(self.get_tec_current()) + " A (Limit:",
              str(self.get_tec_current_limit()) + "A)")

    
        
    def __get_response(self, parameter):
        """
        Return Response object from getter function
        """
        cmd = Getter(parameter)
        self.dev.write(cmd.data_bytes())
        
        return Response(self.dev.read_until(expected='\r'))
        
    
    def get_driver_state(self):
        """
        Return a 8-bit mask representing driver state
        """
        return self.__get_response('DRIVER_STATE').raw()
        
    def driver_state(self):
        """
        Prints the driver state
        """
        state = self.get_driver_state()
        
        print("Device:\t\t", "ON" if state[3] & 0x1 else "OFF")
        print("Driver:\t\t", "ON" if state[3] & 0x2 else "OFF")
        print("Current:\t\t", "INT" if state[3] & 0x4 else "EXT")
        print("Enable:\t\t", "INT" if state[2] & 0x1 else "EXT")
        print("NTC int.:\t\t", "DENY" if state[3] & 0x4 else "ALLOW")
        print("Interlock:\t\t", "DENY" if state[3] & 0x8 else "ALLOW")
        
    
    def driver_on(self):
        """
        Print driver on/off state specifically
        """
        state = self.get_driver_state()
        
        print("Driver:\t\t", "ON" if state[3] & 0x2 else "OFF")
        
    
    def get_driver_value(self):
        """
        Returns driver setpoint current
        """
        return self.__get_response('DRIVER_CURRENT_VALUE').rtoi() / 10
    
    
    def get_driver_current(self):
        """
        Returns driver current measurement
        """
        return self.__get_response('DRIVER_CURRENT_MEASURED').rtoi() / 10
    
    
    def get_driver_current_max(self):
        """
        Returns max driver current
        """
        return self.__get_response('DRIVER_CURRENT_MAXIMUM').rtoi() / 10
    
        
    def get_tec_state(self):
        """
        Return a bit mask representing driver state
        """
        return self.__get_response('TEC_STATE').raw()
    
    
    def tec_state(self):
        """
        Print TEC state
        """
        state = self.get_tec_state()
        
        print("TEC:\t\t", "ON" if state[3] & 0x2 else "OFF")
        print("Temp set:\t\t", "INT" if state[3] & 0x4 else "EXT")
        print("Enable:\t\t", "INT" if state[2] & 0x1 else "EXT")
        
        print("TEC temperature:", self.get_tec_temperature())
        print("TEC set point:", self.get_tec_value())
        
    
    def tec_on(self):
        """
        Print tec on/off state specifically
        """
        state = self.get_tec_state()
        
        print("TEC:\t\t", "ON" if state[3] & 0x2 else "OFF")
        
        
    def get_tec_value(self):
        """
        Returns TEC setpoint temperature
        """
        return self.__get_response('TEC_TEMPERATURE_VALUE').rtoi() / 100
    
    
    def get_tec_temperature(self):
        return self.__get_response('TEC_TEMPERATURE_MEASURED').rtoi() / 100
    
    
    def get_tec_current(self):
        res = self.__get_response('TEC_CURRENT_MEASURED')
        current = res.rtoi()
            
        return current / 10
    
    
    def get_tec_current_limit(self):
        return self.__get_response('TEC_CURRENT_LIMIT').rtoi() / 10

    
    def get_lock_state(self):
        return self.__get_response('LOCK_STATE').data        


    def lock_state(self):
        """
        Print lock state
        """
        state = self.get_lock_state()
        
        print("Interlock:\t\t", "ON" if state[4] & 0x2 else "OFF")
        print("LD OC:\t\t", "ON" if state[4] & 0x8 else "OFF")
        print("LD OH:\t\t", "ON" if state[3] & 0x1 else "OFF")
        print("NTC ext.:\t\t", "ON" if state[3] & 0x2 else "OFF")
        print("TEC err.:\t\t", "ON" if state[3] & 0x4 else "OFF")
        print("TEC SH:\t\t", "ON" if state[3] & 0x8 else "OFF")


    def get_serial_no(self):
        return self.__get_response('SERIAL_NO').rtoi()
        
    
    def __set_routine(self, parameter, value):
        cmd = Setter(parameter, value)
        self.dev.write(cmd.data_bytes())
        
        res = Response(self.dev.read_until(expected='\r'), 'set')
        if res.state == 'error':
            print("Error setting", parameter)
            return
        
        return res
    
    
    def set_driver_state(self):
        # internal enables
        self.__set_routine('DRIVER_STATE', 0x0020)
        self.__set_routine('DRIVER_STATE', 0x0400)
        # deny ext NTC
        self.__set_routine('DRIVER_STATE', 0x4000)

            
    
    def set_driver_on(self):
        if self.tec_off:
            return 'tec'
        
        if type(self.__set_routine('DRIVER_STATE', 0x0008)) != None:
            self.driver_off = False
        else:
            print(self.serial_no, "Failed to set driver on")
            
        
    def set_driver_off(self):
        if type(self.__set_routine('DRIVER_STATE', 0x0010)) != None:
            self.driver_off = True
        else:
            print(self.serial_no, "Failed to set driver off")
            
    
    def set_driver_current_max(self, current_mA):
        self.__set_routine('DRIVER_CURRENT_MAXIMUM', current_mA * 10)
        
    
    def set_driver_current(self, current_mA):
        self.__set_routine('DRIVER_CURRENT_VALUE', current_mA * 10)

    
    def set_tec_temperature(self, temp_C):
        self.__set_routine('TEC_TEMPERATURE_VALUE', temp_C * 100)

    
    def set_tec_int(self):
        # internal enables
        self.__set_routine('TEC_STATE', 0x0020)
        self.__set_routine('TEC_STATE', 0x0400)
    
    
    def set_tec_on(self):
        if type(self.__set_routine('TEC_STATE', 0x0008)) != None:
            self.tec_off = False
        else:
            print(self.serial_no, "Failed to set TEC on")
        
        
    def set_tec_off(self):
        if not self.driver_off:
            return 'driver'
        
        if type(self.__set_routine('TEC_STATE', 0x0010)) != None:
            self.tec_off = True
        else:
            print(self.serial_no, "Failed to set TEC off")

    
class Command:
    """
    Builds SF8xxx byte arrays from input parameters.
    """
    def __init__(self):
        self.terminator = 0x0D
        
        self.parameters = {
            'DRIVER_STATE': '0700',
            'DRIVER_CURRENT_VALUE': '0300',
            'DRIVER_CURRENT_MAXIMUM': '0302',
            'DRIVER_CURRENT_MAXIMUM_LIMIT': '0306',
            'DRIVER_CURRENT_MEASURED': '0307',
            'DRIVER_VOLTAGE_MEASURED': '0407',
            
            'TEC_STATE': '0A1A',
            'TEC_TEMPERATURE_VALUE': '0A10',
            'TEC_TEMPERATURE_MAXIMUM': '0A11',
            'TEC_TEMPERATURE_MAXIMUM_LIMIT': '0A13',
            'TEC_TEMPERATURE_MEASURED': '0A15',
            'TEC_CURRENT_MEASURED': '0A16',
            'TEC_CURRENT_LIMIT': '0A17',
            'TEC_VOLTAGE_MEASURED': '0A18',
            
            'LOCK_STATE': '0800',
            
            'SERIAL_NO': '0701'
            }
        
    
    def set_parameter(self, parameter):
        """
        parameter: hex string
        """
        self.data[1:5] = parameter.encode('ascii')
        
        
    def data_bytes(self):
        return bytes(self.data)
    
    
    def data_print(self):
        print(self.data_bytes())
        

class Setter(Command):
    """
    SF8xxx set "P" type commands.
    """
    def __init__(self, parameter, value):
        Command.__init__(self)
        self.data = bytearray(11)
        self.data[0] = 0x50
        self.data[-1] = self.terminator
        self.data[5] = 0x20
        self.set_parameter(self.parameters[parameter])
        self.set_input(value)
        
    
    # work on this one
    def set_input(self, value):
        """
        value: integer
        """
        def hextoa(val):
            val_len = 4
            val = str(hex(val))[2:].upper()
            
            while len(val) < val_len:
                val = '0' + val
            
            return val
        
        if type(value) == int:
            value = hextoa(value)
            
        self.data[6:10] = value.encode('ascii')

    
class Getter(Command):
    """
    SF8xxx request "J" type commands.
    """

    def __init__(self, parameter):
        Command.__init__(self)
        self.data = bytearray(6)
        self.data[0] = 0x4A
        self.data[-1] = self.terminator
        self.set_parameter(self.parameters[parameter])

    
class Response:
    """
    SF8xxx response "K" structure.
    """
    def __init__(self, data, flag='get'):        
        self.data = data
        self.state = 'untested'
        
        if len(data) == 0:
            if flag == 'set':
                return
            
            print("ERROR: Response: no data")
            self.state = 'error'
            return
        
        if self.data[0] == ord('E'):
            self.state = 'error'
        
        if(self.data == b'E0000\r'):
            print("ERROR:", self.data, "No terminator/buffer/format.")
        elif(self.data == b'E0001\r'):
            print("ERROR:", self.data, "Undefined header.")
        elif(self.data == b'E0002\r'):
            print("ERROR:", self.data, "CRC.")
        
    
    def raw(self):
        """
        Return response value as bytes
        """
        return self.data[6:10]
    
    
    def rtoa(self):
        """
        Return response value as ASCII string
        """
        return self.data[6:10].decode('ascii')
    
    
    def rtoi(self):
        """
        Return response value as decimal integer
        """
        return int(self.rtoa(), 16)
    
    
    def data_print(self):
        print(self.data)
