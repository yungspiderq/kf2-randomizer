"""Build a genuine Win32 UI EXE on Linux or Windows with clang + lld-link.
Uses only Windows OS DLL imports and no external runtime, Qt, HTML, or browser.
"""
from pathlib import Path
import subprocess
import shutil
ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'build'
WORK.mkdir(exist_ok=True)
DLLS = {
  'kernel32': ['GetModuleHandleW','GetEnvironmentVariableW','CreateDirectoryW', 'GetPrivateProfileIntW',
               'GetPrivateProfileStringW','WritePrivateProfileStringW','GetTickCount64',
               'GetLocalTime','ExitProcess','GlobalAlloc','GlobalLock','GlobalUnlock','GlobalFree'],
  'user32': ['RegisterClassExW','CreateWindowExW','DefWindowProcW','ShowWindow','UpdateWindow',
             'GetMessageW','TranslateMessage','DispatchMessageW','PostQuitMessage','SendMessageW',
             'MoveWindow','SetWindowTextW','SetFocus','LoadCursorW','BeginPaint','EndPaint',
             'FillRect','GetClientRect','InvalidateRect','DrawTextW','OpenClipboard','EmptyClipboard',
             'SetClipboardData','CloseClipboard','MessageBoxW'],
  'gdi32': ['CreateSolidBrush','CreateFontW','SelectObject','DeleteObject','SetTextColor',
            'SetBkColor','SetBkMode','RoundRect','GetStockObject']
}
for dll,symbols in DLLS.items():
    d=WORK/(dll+'.def')
    d.write_text('LIBRARY '+dll.upper()+'.DLL\nEXPORTS\n'+'\n'.join(' '+s for s in symbols)+'\n')
    subprocess.run(['lld-link','/dll','/noentry','/machine:x64','/def:'+str(d),
      '/out:'+str(WORK/(dll+'.dll')),'/implib:'+str(WORK/(dll+'.lib'))],check=True)
obj=WORK/'kf2_win32.obj'
subprocess.run(['clang','-target','x86_64-pc-windows-msvc','-c','-O2','-Wno-unknown-pragmas',
  '-Wno-ignored-attributes',str(ROOT/'src/kf2_win32.c'),'-o',str(obj)],check=True)
out=ROOT/'KF2-Randomizer-Native.exe'
subprocess.run(['lld-link','/machine:x64','/subsystem:windows','/entry:WinMainCRTStartup',
  '/out:'+str(out),str(obj),*(str(WORK/(name+'.lib')) for name in DLLS)],check=True)
print(f'Built native Windows GUI: {out} ({out.stat().st_size} bytes)')