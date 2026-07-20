[app]

# (str) Title of your application
title = Cyber Puzzle Game

# (str) Package name
package.name = cyberpuzzlegame

# (str) Package domain
package.domain = org.cyberxploit

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy,pygame,cython

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 24

# (int) Android NDK API to use
android.ndk_api = 21

# (str) Android NDK version
android.ndk = 25b

# (str) Android SDK version
android.sdk = 33

# (str) Hostpython version (Matches container 3.14.2)
android.hostpython = 3.14.2

# (bool) If True, automatically accept SDK license
android.accept_sdk_license = True

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display build progress
display_progress = 1
