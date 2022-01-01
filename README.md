# The light Python GUI builder (currently based on PyQt5)

# How to start with PyPI package:
```bash
poetry new project_01 && cd project_01 && poetry shell
poetry add zzgui
cd project_01
python -m zzgui > example_app.py && python example_app.py
```
# Explore sources:
```bash
git clone https://github.com/AndreiPuchko/zzgui.git
cd zzgui
pip3 install poetry
poetry shell
poetry install
python3 demo/demo.py
python3 demo/demo_01.py
python3 demo/demo_02.py
python3 demo/demo_03.py
python3 demo/demo_04.py
```

# demo/demo_03.py screenshot
![Alt text](https://andreipuchko.github.io/zzgui/screenshot.png)
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
