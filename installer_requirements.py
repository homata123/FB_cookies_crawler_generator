import sys
import subprocess
import importlib
import os

def read_txt(filepath):
    f = open(filepath, "r")
    libs=f.readlines()
    f.close()
    return libs
def write_txt(content):
    f = open("check_installed.txt", "a")
    f.write(content)
    f.close()
def init_file_n_folder():
    #create cookies folder
    try:
        os.mkdir("cookies")
    except:
        pass
    try:
        with open('requirements.txt', 'w') as f:
            f.write('pyinstaller==5.1\n')
            f.write('bs4==0.0.1\n')
            f.write('pickle-mixin==1.0.2\n')
            f.write('requests==2.27.1\n')
            f.write('urllib3==1.26.10\n')
            f.write('tk==0.1.0\n')
        f.close()
    except:
        pass
    try:
        with open('check_installed.txt', 'w') as f:
            f.write('')
        f.close()
    except:
        pass

def installer():
    libs=read_txt("requirements.txt")
    for lib in libs:
        try:
            lib_no_ver=lib.split("==")[0]
            lib_import=importlib.import_module("{}".format(lib_no_ver))
            print(lib_no_ver ,lib_import.__version__)
            write_txt("y")
        except:
            try:
                print("Lib {} has not been installed. Installer started ...".format(lib))
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '{}'.format(lib)],check=True)
                write_txt("y")
            except:
                write_txt("y")
                pass

def installer_caller():
    try:
        check_installed=read_txt("check_installed.txt")
        if len(check_installed)==0: 
            installer()
        else:
            pass
    except:
        init_file_n_folder()
        check_installed=read_txt("check_installed.txt")
        if len(check_installed)==0: 
            installer()
        else:
            pass

