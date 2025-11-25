#!/bin/bash
git clone --branch feature/perfil-user https://github.com/juanfranciscosolis/IDS-TPFINAL.git

cd IDS-TPFINAL

rm -rf .venv
rm -rf venv
mkdir .venv

python3 -m venv .venv
source .venv/bin/activate

pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
