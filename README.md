# Application Web d'analyse des sentiments
## Installation
### Set virtual environment 
```bash
python3.10 -m venv .venv
```

### Start virtual environmnet 
#### Windows 
```bash
.venv/Scripts/Ativate.ps1
```

#### Unix 
```bash
source .venv/bin/activate
```
### Dependencies installation 
```bash
pip install -r requirement.tx
```
## Launch app
### Launch server
```bash
uvicorn main:app --host 127.0.0.1 --port 9000 --reload
```
### Launch streamlit
```bash
streamlit run app.py
```
## TODO
- [x] Optimiser les FPS pour communication avec l'API ( 5 FPS),
- [ ] Intégrer le image to text pour avoir une description, bouton qui prend une photo et donne la description,
- [x] Intègre la journalisation (loguru) + pytest  (BONUS),
- [ ] Remplacer le resnet par Yolo11 (BONUS)