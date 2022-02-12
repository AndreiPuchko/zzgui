docker run --rm -it \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY=$DISPLAY \
    -u zzgui \
    zzgui \
    python3 demo/${1-demo_00.py} /ini:none
