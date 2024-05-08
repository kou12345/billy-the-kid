# camera.pyからCameraクラスをimport
from billy_the_kid.camera import Camera

"""
MacBookの場合、0を指定するとエラーになる。とりあえず1を指定すると動作する
https://github.com/opencv/opencv-python/issues/916
"""
camera = Camera(1)
camera.run()
