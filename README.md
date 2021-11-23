# The light Python GUI builder (currently based on PyQt5)

# How to run:
```bash
git clone https://github.com/AndreiPuchko/zzgui.git
cd zzgui
pip3 install poetry
poetry shell
poetry install
python3 demo/demo.py
```

# Build standalone executable 
(The resulting executable file will appear in the folder  dist/)
## One file
```bash
pyinstaller -F demo/demo.py
```

## One directory
```bash
pyinstaller -D demo/demo.py
```

![Alt text](https://andreipuchko.github.io/zzgui/screenshot.png)
