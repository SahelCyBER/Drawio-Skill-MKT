# Exemple Sahel CyBER

Planche de référence de la charte : trois étapes, un panneau encre, un bandeau
de synthèse. Tout est généré par `demo-charte.py`, sans aucun asset externe.

![Aperçu](demo-charte.png)

## Générer

```bash
python3 -m venv /tmp/ppdocx
/tmp/ppdocx/bin/pip install pymupdf
/tmp/ppdocx/bin/python examples/sahelcyber/demo-charte.py
python3 skills/drawio-skill/scripts/validate.py examples/sahelcyber/demo-charte.drawio --score
```

## Exporter

```bash
/Applications/draw.io.app/Contents/MacOS/draw.io \
  --export --format png --scale 2 --border 20 \
  -o examples/sahelcyber/demo-charte.png examples/sahelcyber/demo-charte.drawio
```

## Adapter

| Élément | Où |
| --- | --- |
| Titre, sous-titre | `title`, `subtitle` |
| Trois étapes | `STEPS` |
| Panneau encre | `panel-*` |
| Badge | `host`, `icon-host` |
| Bandeau | `band-*` |

Remplacer les libellés, garder la structure : chaque carte et chaque panneau
contient ses textes et son icône, donc le déplacement reste propre dans
draw.io.
