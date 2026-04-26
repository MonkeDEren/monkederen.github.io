[app]

title = PermutationApp
package.name = permutationapp
package.domain = org.ankit
source.dir = .
source.include_exts = py,kv,png,jpg,ttf,txt

version = 1.0

orientation = portrait
fullscreen = 0

requirements = python3,kivy

android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

android.archs = arm64-v8a, armeabi-v7a

android.permissions = INTERNET

# Keep this ON so your KV file loads correctly
presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png

# Prevent crashes due to missing SDL2 bootstrap
android.enable_androidx = True

# Avoid unnecessary heavy libraries
android.allow_backup = True

# Faster builds
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
