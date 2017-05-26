from ctypes import CDLL, c_char_p
from myDevices.utils.logger import exception, info, warn, error, debug, logJson
from os import path, getpid
from json import loads, dumps
from psutil import virtual_memory, swap_memory
from myDevices.os.cpu import CpuInfo


class SystemInfo():
    """Class to get system CPU, memory, uptime, storage and network info"""

    def getSystemInformation(self):
        """Get a dict containing CPU, memory, uptime, storage and network info"""
        currentSystemInfo = "{}"
        try:
            debug('Child process for systeminformation pid:' + str(getpid()))
            libSystemInformation = CDLL("/etc/myDevices/libs/libSystemInformation.so")
            if libSystemInformation:
                libSystemInformation.GetSystemInformation.restype = c_char_p
                currentSystemInfo = libSystemInformation.GetSystemInformation().decode('utf-8')
                libSystemInformation.FreeSystemInformation()
                del libSystemInformation
                libSystemInformation = None
                try:
                    system_info = loads(currentSystemInfo)
                    try:
                        cpu_info = CpuInfo()
                        system_info['Cpu'] = cpu_info.build_info()
                        system_info['CpuLoad'] = cpu_info.get_cpu_load()
                    except:
                        pass
                    system_info['Memory'] = self.getMemoryInfo()
                    system_info['Uptime'] = self.getUptime()
                    currentSystemInfo = dumps(system_info)
                except:
                    pass
        except Exception as ex:
            exception('getSystemInformation failed to retrieve: ' + str(ex))
        finally:
            return currentSystemInfo

    def getMemoryInfo(self):
        """Get a dict containing the memory info
        
        Returned dict example::

            {
                'used': 377036800,
                'total': 903979008,
                'buffers': 129654784,
                'cached': 135168000,
                'processes': 112214016,
                'free': 526942208,
                'swap': {
                    'used': 0,
                    'free': 104853504,
                    'total': 104853504
                }
            }
        """
        memory = {}
        try:
            vmem = virtual_memory()
            memory['total'] = vmem.total
            memory['free'] = vmem.available
            memory['used'] = memory['total'] - memory['free']
            memory['buffers'] = vmem.buffers
            memory['cached'] = vmem.cached
            memory['processes'] = vmem.used - vmem.buffers - vmem.cached
            swap = swap_memory()
            memory['swap'] = {}
            memory['swap']['total'] = swap.total
            memory['swap']['free'] = swap.free
            memory['swap']['used'] = swap.used
        except Exception as e:
            exception('Error getting memory info')
        return memory

    def getUptime(self):
        """Get system uptime as a dict
        
        Returned dict example::

            {
                'uptime': 90844.69,
                'idle': 391082.64
            }
        """
        info = {}
        uptime      = 0.0
        idle        = 0.0
        try:
            with open('/proc/uptime', 'r') as f_stat:
                lines = [line.split(' ') for content in f_stat.readlines() for line in content.split('\n') if line != '']
                uptime = float(lines[0][0])
                idle = float(lines[0][1])
        except Exception as e:
            exception('Error getting uptime')
        info['uptime'] = uptime
        info['idle'] = idle
        return info