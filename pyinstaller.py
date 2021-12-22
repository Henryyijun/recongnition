
if __name__ == '__main__':
    from PyInstaller.__main__ import run
    opts=['charRecognition.py','-F','-w','--hidden-import=queue','--icon=./myicon.ico']
    run(opts)