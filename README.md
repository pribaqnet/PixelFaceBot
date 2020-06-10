# PixelFaceBot
El PixelFaceBot és un robot de Telegram per a pixelar cares en qualsevol fotografia, respectant la privacitat de tots els usuaris. Envia una foto i el bot te la retornarà amb totes les cares censurades.

![](readme/mockup.gif)

## Funcionament:
### Pas 1: Detecció facial
![](readme/f1.png)
### Pas 2: Extracció de la cara (ROI)
![](readme/f2.png)
### Pas 3: Censura (Pixelació)
![](readme/f3.png)
### Pas 4: Resultat
![](readme/f4.png)

## Requeriments:
```
pip install opencv-python
```
```
pip install python-telegram-bot --upgrade
```
