# The light Python GUI builder (currently based on PyQt5)

# How to start 
## With docker && x11:
```bash
git clone https://github.com/AndreiPuchko/zzgui.git
#                      sudo if necessary 
cd zzgui/docker-x11 && ./build_and_run_menu.sh
```
## With PyPI package:
```bash
poetry new project_01 && cd project_01 && poetry shell
poetry add zzgui
cd project_01
python -m zzgui > example_app.py && python example_app.py
```
## Explore sources:
```bash
git clone https://github.com/AndreiPuchko/zzgui.git
cd zzgui
pip3 install poetry
poetry shell
poetry install
python3 demo/demo_01.py     # basic: main menu, form & widgets
python3 demo/demo_02.py     # forms and forms in form
python3 demo/demo_03.py     # grid form (CSV data), automatic creation of forms based on data
python3 demo/demo_04.py     # progressbar, data loading, sorting and filtering
python3 demo/demo_05.py     # nonmodal form
python3 demo/demo_06.py     # code editor
python3 demo/demo_07.py     # database app (4 tables, mock data loading) - requires a zzdb package
python3 demo/demo_08.py     # database app, requires a zzdb package, autoschema
```

## demo/demo_03.py screenshot
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
