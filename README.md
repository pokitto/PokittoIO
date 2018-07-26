# PokittoIO - core of PokittoLib reformatted for PlatformIO

PokittoLib is a library for making programs on Pokitto hardware

PokittoIO is just the core files needed to compile programs on PlatformIO

**Note: This is currently work in progress and somewhat untested**

## To build on Visual Studio Code & PlatformIO

- select LPCXpresso11U68 as target
- include "Pokitto.h" in your main file 
- see that you have a "My_settings.h" (aka Pokitto project build settings file) in the same directory as your main file. Example given at the end of this file.
- edit your platform.ini so that you have the following settings:

```
platform = nxplpc
board = lpc11u68
framework = mbed
build_flags =
  -DPOKITTO_PIO_BUILD
  -Isrc
extra_scripts = pre:pokitto_pre.py
```

- create a file called **pokitto_pre.py** in the same directory as platform.ini and copy-paste following code

```
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
url = 'https://raw.githubusercontent.com/pokitto/PokittoIO/master/src/hal/LPC11U68/mbed_patches/arm_gcc/startup_LPC11U68.cpp'
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
if (os.path.exists(patchPath + 'startup_LPC11U68.tmp')):
    os.remove(patchPath+'startup_LPC11U68.tmp')

#get the latest linker file from github
print("Comparing linker file LPC11U68.ld to PokittoLib repository...")
url = 'https://raw.githubusercontent.com/pokitto/PokittoIO/master/src/hal/LPC11U68/mbed_patches/arm_gcc/LPC11U68.ld'
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
if (os.path.exists(patchPath + 'LPC11U68.tmp')):
    os.remove(patchPath+'LPC11U68.tmp')
```

## Example of a My_settings.h file

```
/**************************************************************************/
/*!
    @file     My_settings.h
    @author   XX

    @section HOW TO USE My_settings

   My_settings can be used to set project settings inside the mbed online IDE
*/
/**************************************************************************/

#ifndef MY_SETTINGS_H
#define MY_SETTINGS_H

#define PROJ_HIRES 0            //1 = high resolution (220x176) , 0 = low resolution fast mode (110x88)
#define PROJ_ENABLE_SOUND 0     // 0 = all sound functions disabled

#endif
```

# License
```
/**************************************************************************/

	PokittoIO / PokittoLib

    Software License Agreement (BSD License)

    Copyright (c) 2016-2018, Jonne Valola
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
    1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
    3. Neither the name of the copyright holders nor the
    names of its contributors may be used to endorse or promote products
    derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ''AS IS'' AND ANY
    EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
	
/**************************************************************************/
```


