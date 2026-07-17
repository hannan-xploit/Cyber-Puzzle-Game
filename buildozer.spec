[app]
title = Cyber Puzzle Game
package.name = cyberpuzzlegame
package.domain = org.cyberxploit

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf

version = 0.1

# IMPORTANT: don't mix kivy + pygame, only pygame is needed here.
# Pinned versions = far fewer build breaks.
requirements = python3,pygame==2.1.2,cython==0.29.33

orientation = portrait
fullscreen = 0

# icon/presplash - add real files later, keep commented until you have them
#icon.filename = %(source.dir)s/assets/icon.png
#presplash.filename = %(source.dir)s/assets/presplash.png

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
# sdl2 bootstrap is required for pure-pygame apps (not the kivy bootstrap)
android.bootstrap = sdl2

android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.entrypoint = org.kivy.android.PythonActivity
android.allow_backup = True

# use a known-stable p4a branch instead of master (master breaks often)
p4a.branch = develop
