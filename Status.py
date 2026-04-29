import threading
import time

class Status:
  def __init__(self, devices, fn="/tmp/sf8_status"):
    self.devices = devices  # a dict of the connected device objects
    self.filename = fn
    self.end_threads = False
    self.interval = 1


  def __run(self):
    while not self.end_threads:
      f = open(self.filename, "w")
      f.write(__str_status_header())
      for dev in self.devices.values():
        f.write(__str_status_line(dev))
      time.sleep(self.interval)


  def run(self):
    self.run_thread = threading.Thread(target=self.__run,
                                        args=(,))
    self.run_thread.start()
    

def __str_status_header():
  return "ser_no\tConnection\tDriver\tCurrent (mA)\tTec\tCurrent (A)\n"


def __str_status_line(device):
  serial_no = device.serial_no
  is_connected = device.connected
  is_driver_on = device.driver_on()
  is_tec_on = device.tec_on()
  dri_cur = device.get_driver_current()
  tec_cur = device.get_tec_current()

  return str(serial_no) + 
        "\tGOOD" if is_connected else "\tBAD" +
        "\tON\t" if is_driver_on else "\tOFF\t" + 
        str(dri_cur) +
        "\tON\t" if is_tec_on else "\tOFF\t" +
        str(tec_cur) + "\n"
