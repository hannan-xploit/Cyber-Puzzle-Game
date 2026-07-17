[app]
title = Cyber Puzzle Game
package.name = cyberpuzzlegame
package.domain = org.cyberxploit

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf

version = 0.1

requirements = python3==3.11.6,pygame==2.1.2,cython==0.29.33

orientation = portrait
fullscreen = 0

[app:android]
android.bootstrap = sdl2
android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.entrypoint = org.kivy.android.PythonActivity
android.allow_backup = True
p4a.branch = develop

[buildozer]
log_level = 2
warn_on_root = 1
