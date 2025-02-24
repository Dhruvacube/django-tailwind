import subprocess
import sys

from tailwind import get_config


class NPMException(Exception):
    pass


class NPM:
    cwd = None
    npm_bin_path = None

    def __init__(self, cwd=None, npm_bin_path=None):
        self.npm_bin_path = npm_bin_path if npm_bin_path else get_config("NPM_BIN_PATH")
        self.cwd = cwd

    def cd(self, cwd):
        self.cwd = cwd

    def command(self, *args, **kwargs):
        times_cwd_ran = 0 if kwargs.get('times_cwd_ran') is None else kwargs.get('times_cwd_ran')
        try:
            subprocess.run([self.npm_bin_path] + list(args), cwd=self.cwd,check=kwargs.get('check', True), shell=True)
            return True
        except subprocess.CalledProcessError:
            sys.exit(1)
        except OSError:
            if times_cwd_ran>=1:
                raise NPMException(
                    "\nIt looks like node.js and/or npm is not installed or cannot be found.\n\n"
                    "Visit https://nodejs.org to download and install node.js for your system.\n\n"
                    "If you have npm installed and still getting this error message, "
                    "set NPM_BIN_PATH variable in settings.py to match path of NPM executable in your system.\n\n"
                    ""
                    "Example:\n"
                    'NPM_BIN_PATH = "/usr/local/bin/npm"'
                )
            else:
                self.npm_bin_path = 'npm'
                self.command(times_cwd_ran=times_cwd_ran+1,check=False,*args, **kwargs)
                return True
                
