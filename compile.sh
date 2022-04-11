python3 -m pip install PyInstaller
python3 -m PyInstaller --onefile --console --noconfirm InstaStalker.py
rm -rf ./build
rm ./InstaStalker.spec -f
rm ./__pycache__ -rf
echo "COMPILED SUCCESSFULLY!"