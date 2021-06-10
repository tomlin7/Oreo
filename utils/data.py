import sys
import tkinter
import pyglet
import platform

oreo_version = "1.0.0"
oreo_commit = "..."
oreo_updatedate = "..."
tk_version = tkinter.TkVersion

python_version = "{0}.{1}.{2}".format(
    sys.version_info.major,
    sys.version_info.minor,
    sys.version_info.micro
)
os_version = platform.platform()

pyglet.font.add_file('res/fonts/firasans.ttf')
pyglet.font.add_file('res/fonts/firacode.ttf')
pyglet.font.add_file('res/fonts/jbmono.ttf')

icon = "./res/images/oreo.ico"

fira_sans = ('Fira Sans', 10)
fira_code = ('Fira Code', 11)
jetbrains_mono = ('JetBrains Mono', 11)

about_text = """
Oreo 
Integrated Development Environment for Kookie.

Version: {0} (user setup)
Commit: {1}
Date: {2} (... weeks ago)
Tk: {3}
Python: {4}
OS: {5}
""".format(
    oreo_version, oreo_commit, oreo_updatedate,
    tk_version, python_version, os_version
)

help_text = """
File
----
New         - Creates a new file.
Open        - Opens an existing file.
Save        - Saves the current file.
Save As     - Saves file as a new file.
Exit        - Quit the application
-----------------------------------
Edit
-----
Copy        - Copy selected text.
Cut         - Cut selected text.
Paste       - Paste text from clipboard.
-----------------------------------
Run
-----
Build       - Compile the open cookie.
Build & Run - Compile and run the cookie.
Debug       - Debug the cookie (not yet, no).

Start Interactive Session - Start a kookie Interactive session.
"""
