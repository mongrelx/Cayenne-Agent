from setuptools import setup, Extension
import os
import pwd

classifiers = ['Development Status :: 1 - Alpha',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: Home Automation',
               'Topic :: System :: Hardware']

try:
      # Try to install under the cayenne user, if it exists.
      user = pwd.getpwnam('cayenne')
      user_id = user.pw_uid
      group_id = user.pw_gid
except KeyError:
      # Otherwise install under the user that ran sudo.
      user_id = int(os.environ['SUDO_UID'])
      group_id = int(os.environ['SUDO_GID'])
directories = ('/etc/myDevices', '/var/log/myDevices', '/var/run/myDevices')
for directory in directories:
      try:
            os.makedirs(directory)
      except FileExistsError:
            pass
      os.chown(directory, user_id, group_id)

setup(name             = 'myDevices',
      version          = '0.2.1',
      author           = 'myDevices',
      author_email     = 'N/A',
      description      = 'myDevices Cayenne agent',
      long_description = 'N/A',
      license          = 'N/A',
      keywords         = 'myDevices Cayenne IoT',
      url              = 'https://www.mydevices.com/',
      classifiers      = classifiers,
      packages         = ["myDevices", "myDevices.ipgetter", "myDevices.cloud", "myDevices.utils", "myDevices.os", "myDevices.sensors" , "myDevices.wifi", "myDevices.schedule", "myDevices.requests_futures", "myDevices.devices", "myDevices.devices.analog", "myDevices.devices.digital", "myDevices.devices.sensor", "myDevices.devices.shield", "myDevices.decorators"],
      install_requires = ['enum34', 'iwlib', 'jsonpickle', 'netifaces', 'psutil >= 0.7.0', 'requests'],
      data_files       = [('/etc/myDevices/scripts', ['scripts/config.sh'])]
      )

os.chmod('/etc/myDevices/scripts/config.sh', 0o0755)
