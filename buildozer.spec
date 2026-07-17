[app]

# (str) Title of your application
title = Cyber Puzzle Game

# (str) Package name
package.name = cyberpuzzlegame

# (str) Package domain (needed for android/ios packaging)
package.domain = org.cyberxploit

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 24

# (int) Android NDK API to use
android.ndk_api = 21

# (bool) If True, automatically accept SDK license
android.accept_sdk_license = True

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity
