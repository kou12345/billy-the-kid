from billy_the_kid.camera import Camera

"""
MacBookの場合、0を指定するとエラーになる。とりあえず1を指定すると動作する
https://github.com/opencv/opencv-python/issues/916

外部カメラを接続している場合は、0を指定する
"""
camera = Camera(0)
camera.run()
