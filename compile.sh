#!/usr/bin/bash
python3 -m pip install PyInstaller
python3 -m PyInstaller --noconfirm --onefile --console --name instastalk ./instastalk.py
rm -f ./instastalk.spec
rm -rf ./build
folder_name="$(lsb_release -ds)"
mkdir compiled && cd compiled
mkdir "./$folder_name" && cd ..
mv "dist/instastalk" "./compiled/$folder_name"
rm -rf dist
echo "[?] Do you want to Installed the compiled file[Y/n]?: "
read installyn
if [ $installyn = "y" ]; then
    chmod +x "./compiled/$folder_name/instastalk"
    sudo cp "./compiled/$folder_name/instastalk" "/usr/bin/instastalk"
    echo "[+] Compiled and Installed!"
else
    echo "[+] Compiled!"
fi