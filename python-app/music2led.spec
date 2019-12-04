# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


import os
import distutils.util

DIR_PATH = os.getcwd()
COMPILING_PLATFORM = distutils.util.get_platform()

if COMPILING_PLATFORM == 'win-amd64':
    platform = 'win'
    STRIP = False
elif COMPILING_PLATFORM == 'linux-x86_64':
    platform = 'nix64'
    STRIP = True
elif "macosx" and "x86_64" in COMPILING_PLATFORM:
    platform = 'mac'
    STRIP = True

a = Analysis(['main.py'],
             pathex=['/Users/thibaudfrere/Documents/audio-reactive-led-strip/python-app'],
             binaries=[],
             datas=[('./CONFIG.yml', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='music2led',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
app = BUNDLE(exe,
             name='music2led.app',
             icon='resources/icon.icns',
             bundle_identifier=None)

import shutil
shutil.copyfile('CONFIG.yml', '{0}/CONFIG.yml'.format(DISTPATH))
shutil.copyfile('CONFIG.yml', '{0}/music2led.app/Contents/MacOS/CONFIG.yml'.format(DISTPATH))
