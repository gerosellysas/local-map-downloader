'''
@ Title : XYZ MAP DOWNLOADER
@ Author : Geroselly Suryo Adi S
@ Date : 20 Dec 2022
'''

import sys
import requests
import time
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

MAP_URL = os.getenv('MAP_URL')

zFolder = os.getenv('Z_FOLDER')
firstXFolder = int(os.getenv('FIRST_X_FOLDER')) # first X folder
lastXFolder = int(os.getenv('LAST_X_FOLDER'))  # last X folder
firstYFile = int(os.getenv('FIRST_Y_FILE')) # first Y file
lastYFile = int(os.getenv('LAST_Y_FILE')) # last Y file
path = ''
done = 0

print('\n========== START DOWNLOAD ==========')

if os.path.exists(zFolder):
    print('\nChecking Z Folder =====> Z Folder %s already exist !!!' % zFolder)
else:
    print('\nChecking Z Folder =====> Creating Z Folder =====> %s' % zFolder)
    os.makedirs(zFolder)

async def downloadFile(filename):
    url = '{map_url}{filename}'.format(map_url = MAP_URL, filename = filename)
    with open(filename, 'wb') as f:
        print('Downloading =====> %s' % filename)
        try:
            response = requests.get(url, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None: # no content length header
                print('No Content Length Header !!!')
                f.write(response.content)
                done = 0
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write('\r[%s%s%s]' % ('=' * done, ' ' * (50-done), ' ' + str(done*2) + '%') )
                    sys.stdout.flush()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print('Failed to donwload file =====> %s !!!' % filename)
            # raise SystemExit(e)
            time.sleep(0.5)
            print('\n')
            done = 0
    return done*2

async def startDownload():
    for xFolder in range(firstXFolder, (lastXFolder + 1)):
        path = '{zFolder}/{xFolder}'.format(zFolder = zFolder,  xFolder=xFolder)
        if os.path.exists(path):
            print('\nChecking X Folder =====> X Folder %s is already exist !!!' % xFolder)
            print('\nChecking Y File =====>\n')
            for yFile in range(firstYFile, (lastYFile + 1)):
                filename = '{path}/{yFile}.png'.format(path=path, yFile=yFile)
                if os.path.isfile(filename):
                    if(os.path.getsize(filename) == 0):
                        if os.path.exists(filename):
                            os.remove(filename)
                            print('REMOVE %s FILE !!!\n' % yFile)
                        done = await downloadFile(filename)
                        if (done == 100):
                            time.sleep(0.5)
                            print('\n')
                    else:
                        print('File %s is already exist !!!' % yFile)
                        print('Size %s\n' % os.path.getsize(filename))
                else:
                    done = await downloadFile(filename)
                    if (done == 100):
                        time.sleep(0.5)
                        print('\n')
       
        else:
            print('\nChecking X Folder =====> Creating X Folder =====> %s' % xFolder)
            os.makedirs(path)
            print('\n===== Checking Y File =====\n')
            for yFile in range(firstYFile, (lastYFile + 1)):
                filename = '{path}/{yFile}.png'.format(path=path, yFile=yFile)
                if os.path.isfile(filename):
                    print('File %s is already exist !!!\n' % yFile)
                else:
                    done = await downloadFile(filename)
                    if (done == 100):
                        time.sleep(0.5)
                        print('\n')
    

asyncio.run(startDownload())
print('\n========== DOWNLOAD COMPLETE ==========')