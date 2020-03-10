from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__ = 'GPL 3'
__docformat__ = 'restructuredtext en'

from calibre.customize import EditBookToolPlugin

PLUGIN_NAME = "HorVer"
PLUGIN_SAFE_NAME = PLUGIN_NAME.strip().lower().replace(' ', '_')
PLUGIN_DESCRIPTION = 'Convert contents between horizontal and vertical'
PLUGIN_VERSION_TUPLE = (1, 0, 0)
PLUGIN_VERSION = '.'.join([str(x) for x in PLUGIN_VERSION_TUPLE])
PLUGIN_AUTHORS = 'Luke Hong'

class HorVerPlugin(EditBookToolPlugin):

    name = PLUGIN_NAME
    version = PLUGIN_VERSION_TUPLE
    author = PLUGIN_AUTHORS
    supported_platforms = ['windows', 'osx', 'linux']
    description = PLUGIN_DESCRIPTION
    minimum_calibre_version = (4, 0, 0)

    #def cli_main(self,argv):
        #Typical Usage: calibre-debug --run-plugin "Chinese Text Conversion" -- -h
        #from calibre_plugins.chinese_text.main import main as chinese_text_main
        #chinese_text_main(argv[1:], self.version, usage='%prog --run-plugin '+'\"self.name\"'+' --')
