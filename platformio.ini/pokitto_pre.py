import requests
import os
import filecmp

#the following is needed, because at this stage PLATFORMIO_HOME_DIR is undefined
from os.path import expanduser
home = expanduser("~")

if os.name == 'nt': # Windows
    basePath = home + '\.platformio'
else:
    basePath = home + '/.platformio'

patchPath = basePath + '/packages/framework-mbed/targets/TARGET_NXP/TARGET_LPC11U6X/device/TOOLCHAIN_GCC_ARM/TARGET_LPC11U68/'

#get the latest startup files from github
print("Comparing startup_LPC11U68.cpp to PokittoLib repository...")
url = 'https://raw.githubusercontent.com/pokitto/PokittoLib/master/Pokitto/mbed-pokitto/targets/cmsis/TARGET_NXP/TARGET_LPC11U6X/TOOLCHAIN_GCC_ARM/TARGET_LPC11U68/startup_LPC11U68.cpp'
r = requests.get(url, allow_redirects=True, headers={'Cache-Control': 'no-cache'})
open(patchPath + 'startup_LPC11U68.tmp', 'wb').write(r.content)

#check if startup_LPC11U68.bak exists
if not (os.path.exists(patchPath + 'startup_LPC11U68.bak')):
    #first run, so create a backup
    print('Creating backup of original startup_LPC11U68.cpp')
    os.rename(patchPath + 'startup_LPC11U68.cpp', patchPath + 'startup_LPC11U68.bak')
    
#compare new .tmp file(s) to existing files
if (os.path.exists(patchPath + 'startup_LPC11U68.cpp')):
    if not filecmp.cmp(patchPath + 'startup_LPC11U68.tmp', patchPath + 'startup_LPC11U68.cpp'):
        #they are different, so update
        print('New version found. Saving it as startup_LPC11U68.cpp')
        open(patchPath + 'startup_LPC11U68.cpp', 'wb').write(r.content)
else:
    #missing completely, so save
    print('Saving startup_LPC11U68.cpp')
    open(patchPath + 'startup_LPC11U68.cpp', 'wb').write(r.content)

#delete temporary file(s)
os.remove(patchPath+'startup_LPC11U68.tmp')

#get the latest linker file from github
print("Comparing linker file LPC11U68.ld to PokittoLib repository...")
url = 'https://raw.githubusercontent.com/pokitto/PokittoLib/master/Pokitto/mbed-pokitto/targets/cmsis/TARGET_NXP/TARGET_LPC11U6X/TOOLCHAIN_GCC_ARM/TARGET_LPC11U68/LPC11U68.ld'
r = requests.get(url, allow_redirects=True, headers={'Cache-Control': 'no-cache'})
open(patchPath + 'LPC11U68.tmp', 'wb').write(r.content)

#check if LPC11U68.bak exists
if not (os.path.exists(patchPath + 'LPC11U68.bak')):
    #first run, so create a backup
    if (os.path.exists(patchPath + 'LPC11U68.ld')):
        print('Creating backup of original LPC11U68.ld')
        os.rename(patchPath + 'LPC11U68.ld', patchPath + 'LPC11U68.bak')
    
#compare new .tmp file(s) to existing files
if (os.path.exists(patchPath + 'LPC11U68.ld')):
    if not filecmp.cmp(patchPath + 'LPC11U68.tmp', patchPath + 'LPC11U68.ld'):
        #they are different, so update
        print('New version found. Saving it as LPC11U68.ld')
        open(patchPath + 'LPC11U68.ld', 'wb').write(r.content)
else:
    #missing completely, so save
    print('Saving LPC11U68.ld')
    open(patchPath + 'LPC11U68.ld', 'wb').write(r.content)   

#delete temporary file(s)
os.remove(patchPath+'LPC11U68.tmp')