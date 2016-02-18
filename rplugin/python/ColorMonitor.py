import time
import fcntl
import os
import signal
import os

import neovim

FOLDER_NAME = "/tmp/colors/"
COLOR_FILE_NAME = "vimtheme"

THEME_PATH = FOLDER_NAME + COLOR_FILE_NAME

@neovim.plugin
class ColorChanger(object):
    def __init__(self, vim):
        self.vim = vim
        

    def folderChangeHandler(self, signum, frame):
        self.vim.command("Fuck")
        #try:
        f = open(THEME_PATH)

        self.vim.current.line = ("colorscheme {}".format(f.readline()))
        self.vim.command("colorscheme {}".format(f.readline()))

                #self.vim.command("e yolo")
        #except:
            #self.vim.current.line = "Exception"
            #pass

        

    def ensureFilesExist(self):
        if not os.path.exists(FOLDER_NAME):
            os.makedirs(FOLDER_NAME)

        #If there is no file containing a color theme already
        if not os.path.isfile(THEME_PATH):
            #Create the file with the current theme in it
            f = open(THEME_PATH, 'w')

            f.write(self.vim.command_output("colorscheme").replace("\n", ""))

            f.close()
            




    @neovim.command('StartColorPoll', range='', nargs='*', sync=False)
    def command_handler(self, args, range):
        self.ensureFilesExist();

        signal.signal(signal.SIGIO, self.folderChangeHandler)
        fd = os.open(FOLDER_NAME,  os.O_RDONLY)
        fcntl.fcntl(fd, fcntl.F_SETSIG, 0)
        fcntl.fcntl(fd, fcntl.F_NOTIFY,
                    fcntl.DN_MODIFY | fcntl.DN_CREATE | fcntl.DN_MULTISHOT)

        while True:
            time.sleep(10000)
        #self.vim.current.line = (
        #    'Command: Called %d times, args: %s, range: %s' % (self.calls,
        #                                                       args,
        #                                                       range))
