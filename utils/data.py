import pyglet

pyglet.font.add_file('res/fonts/firasans.ttf')
pyglet.font.add_file('res/fonts/firacode.ttf')
pyglet.font.add_file('res/fonts/jbmono.ttf')

icon = "./res/images/oreo.ico"

fira_sans = ('Fira Sans', 10)
fira_code = ('Fira Code', 11)
jetbrains_mono = ('JetBrains Mono', 11)

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