# Drawio-Skill-MKT

Prise en main du fork draw.io aux couleurs de
[sahelcyber.com](https://sahelcyber.com). Il produit des fichiers `.drawio`
modifiables dans draw.io, plus un PNG prêt pour Word.

Trois usages : créer un diagramme de marque, re-thémer un schéma existant,
sortir une planche paysage pour un document.

## 1. Ce qu'il faut sur le poste

| Outil | Rôle | Vérification |
| --- | --- | --- |
| Python 3.9+ | scripts du dépôt | `python3 --version` |
| draw.io (application) | export PNG, PDF, SVG | `ls /Applications/draw.io.app` |
| PyMuPDF | rasteriser les pictogrammes | voir ci-dessous |

PyMuPDF n'est utile que pour les icônes (`png`, `uri`, `cell`). macOS refuse
l'installation globale, donc un environnement jetable suffit :

```bash
python3 -m venv /tmp/ppdocx
/tmp/ppdocx/bin/pip install pymupdf
```

Tout le reste du dépôt fonctionne avec la bibliothèque standard.

## 2. Essayer en trois commandes

```bash
cd ~/Sites/Drawio-Skill-MKT
/tmp/ppdocx/bin/python examples/sahelcyber/demo-charte.py
python3 skills/drawio-skill/scripts/validate.py \
  examples/sahelcyber/demo-charte.drawio --score
```

Attendu : `0 error(s), 0 warning(s)` et `score: 0`. Le fichier
`examples/sahelcyber/demo-charte.drawio` s'ouvre dans draw.io, et le PNG voisin
montre le rendu.

```bash
/Applications/draw.io.app/Contents/MacOS/draw.io \
  --export --format png --scale 2 --border 20 \
  -o /tmp/demo.png examples/sahelcyber/demo-charte.drawio
```

## 3. Demander un diagramme à l'agent

Ouvrir ce dossier dans Qoder, puis demander par exemple :

> Crée un diagramme draw.io aux couleurs Sahel CyBER : parcours de réponse à
> incident en quatre étapes. Livre le `.drawio` et un PNG, puis passe
> `validate.py`.

L'agent lit `SKILL.md` et `references/sahelcyber.md`, applique le preset
`sahelcyber`, prend les icônes dans `ppicons.py`, valide, exporte et montre le
PNG. La règle du dépôt : tout nouveau diagramme sort en charte Sahel CyBER,
sauf demande explicite pour PetitPouss.

## 4. Reprendre un schéma existant

```bash
python3 skills/drawio-skill/scripts/restyle.py ancien.drawio \
  --preset sahelcyber -o nouveau.drawio
```

`restyle.py` remappe les couleurs par teinte, sans toucher à la mise en page.
Il ne recompose pas : un bandeau noir peut devenir gris clair, une icône
blanche peut disparaître. Pour un document de marque, régénérer la planche
plutôt que de restyler un ancien fichier, puis contrôler le PNG à l'œil.

## 5. Pictogrammes

```bash
S=skills/drawio-skill/scripts/ppicons.py

python3 $S list                                   # noms et libellés
python3 $S svg shield-check -o /tmp/shield.svg    # SVG, sans dépendance
/tmp/ppdocx/bin/python $S png cloud --color encre --size 256 -o /tmp/cloud.png
python3 $S uri code --style                       # style draw.io complet
python3 $S cell lock --id icon-lock --x 80 --y 200  # <mxCell> à coller
```

Couleurs : `violet` (défaut), `violet-fonce`, `encre`, `ambre`, `or`, `noir`,
`blanc`, `gris`, ou un code `#RRGGBB`. 26 pictogrammes, dont `shield-check`,
`server`, `cloud`, `code`, `database`, `map-pin`, `users`, `globe`.

Deux précautions, déjà gérées par le script : le data URI doit contenir `%3B`
et non `;`, et draw.io n'accepte pas le SVG embarqué, donc le PNG est
obligatoire.

## 6. La charte en un coup d'œil

| Rôle | Code | Emploi |
| --- | --- | --- |
| Violet | `#683EE5` | filets, flèches, icônes, accents |
| Encre | `#0A1233` | texte, un panneau sombre par planche |
| Ambre | `#F59E0B` | pastilles, chiffres, libellés sur fond sombre |
| Lavande | `#E6E1FB` | cartes secondaires |
| Brume | `#EFF1F8` | fond de zone |
| Blanc | `#FFFFFF` | fond de page, cartes |

Police Arial, titres en gras. Une planche réussie tient en trois matières :
cartes claires, un seul panneau encre pour le point clé, ambre réservé aux
signaux. Détail complet, rôles du preset et pièges : `references/sahelcyber.md`.

Sur un autre poste, copier `sahelcyber.json` dans `~/.drawio-skill/styles/`
puis passer `"default": true` : c'est cette copie utilisateur qui rend la
charte automatique pour tous les nouveaux diagrammes.

## 7. Insérer dans Word

Section paysage, marges 1,2 cm, image à 26,6 cm de large pour une A4. Exporter
à `--scale 2` minimum, sinon le texte bave à l'impression. Réserver `-e` au PNG
final : l'aperçu de contrôle reste léger et lisible.

## 8. Où est quoi

| Chemin | Contenu |
| --- | --- |
| `skills/drawio-skill/SKILL.md` | mode d'emploi chargé par l'agent |
| `skills/drawio-skill/styles/built-in/sahelcyber.json` | preset livré |
| `~/.drawio-skill/styles/sahelcyber.json` | copie avec `"default": true` |
| `skills/drawio-skill/references/sahelcyber.md` | charte et composition |
| `skills/drawio-skill/scripts/ppicons.py` | pictogrammes |
| `examples/sahelcyber/demo-charte.py` | planche de référence |
| `skills/drawio-skill/scripts/validate.py` | contrôle de structure |

## 9. Dépannage

| Symptôme | Correction |
| --- | --- |
| `ModuleNotFoundError: pymupdf` | utiliser `/tmp/ppdocx/bin/python` |
| `drawio: command not found` | appeler `/Applications/draw.io.app/Contents/MacOS/draw.io` |
| Icône cassée dans l'éditeur | régénérer avec `ppicons.py`, vérifier `%3B` |
| Texte invisible sur panneau encre | écrire `fontColor=#FFFFFF` sur la cellule |
| PNG flou dans Word | exporter à `--scale 2` |
| Avertissements de chevauchement | mettre textes et icônes en enfants de leur carte |

## 10. Mettre à jour et publier

```bash
git status
git add -A
git commit -m "feat(brand): ..."
git push fork main
```

| Remote | Dépôt |
| --- | --- |
| `origin` | `Agents365-ai/drawio-skill` (amont) |
| `fork` | `SahelCyBER/drawio-skill` (ce fork) |

Les commits suivent la convention `feat`, `fix`, `docs`, `chore`. Avant un
envoi vers un dépôt distant, lancer la revue de sécurité du poste si elle est
activée.
