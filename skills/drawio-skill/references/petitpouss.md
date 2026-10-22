# PetitPouss — charte, preset et pictogrammes

À lire dès qu'un diagramme est destiné à l'ONG PetitPouss : note de réflexion,
dossier bailleur, fiche pédagogique, rapport d'activité, présentation.

Le guide couvre trois choses : la charte graphique, le preset `petitpouss`, et
les pictogrammes fournis par `scripts/ppicons.py`.

## 1. Charte

Couleurs relevées sur petitpouss.fr :

| Rôle | Code | Usage |
| --- | --- | --- |
| Or | `#D4A800` | accents, filets, traits, icônes |
| Noir | `#1A1D20` | texte, cartes sombres, bandeaux |
| Gris | `#5A5D60` | texte secondaire |
| Gris clair | `#F5F6F7` | fond de zone, cartes |
| Bordure | `#EAEAEA` | contours discrets |
| Blanc | `#FFFFFF` | fond, cartes sur gris |

Typographie : **Georgia** pour les titres, **Arial** pour le texte et les
libellés. Le site utilise DMSans et FrankRuhlLibre ; elles ne sont pas
installées partout, donc le rendu Word et le rendu draw.io resteraient
incohérents. Georgia et Arial existent sur macOS et Windows.

Si les polices du site sont installées sur le poste qui produit le document,
remplacer `font.fontFamily` dans le preset par `DMSans`, puis régénérer.

## 2. Preset `petitpouss`

Fichier : `styles/built-in/petitpouss.json`. Il s'applique à la génération ou
re-thème un diagramme existant :

```bash
python3 scripts/restyle.py schema.drawio --preset petitpouss -o schema-pp.drawio
```

Correspondance des rôles :

| Rôle | Rendu |
| --- | --- |
| service | carte blanche, contour or |
| gateway | carte crème `#FBF3D9`, contour or |
| queue | carte crème, contour or |
| database | carte gris clair, contour noir |
| external | carte gris clair, contour `#EAEAEA` |
| security | carte blanche, contour noir |
| error | carte blanche, contour `#B3261E` |

Le preset ne remplace pas la composition : il ne donne que couleurs, formes,
police et style d'arête. Les espacements, la hiérarchie et les zones restent à
la charge de l'auteur.

## 3. Pictogrammes

```bash
# Lister les pictogrammes disponibles
python3 scripts/ppicons.py list

# Écrire un SVG (aucune dépendance)
python3 scripts/ppicons.py svg cap --color or -o /tmp/cap.svg

# Écrire un PNG transparent
python3 scripts/ppicons.py png tablet --color noir --size 256 -o /tmp/tablet.png

# Style complet, à insérer tel quel dans un attribut style=""
python3 scripts/ppicons.py uri users --color or --style

# Sommet <mxCell> prêt à coller dans un mxGraphModel
python3 scripts/ppicons.py cell tablet --id icon-tablet --color noir --x 80 --y 200
```

Couleurs acceptées : `or`, `noir`, `blanc`, `gris`, ou un code `#RRGGBB`.

Familles disponibles :

- **Personnes** : `users`, `user-round`, `cap`, `standing`
- **Contenus** : `file-text`, `messages`, `book-open`, `calendar`
- **Voix et image** : `mic`, `camera`
- **Technique** : `cpu`, `sparkles`, `tablet`, `database`, `server`, `wifi`,
  `wifi-off`, `lock`, `shield-check`
- **Repères** : `check`, `circle-check`, `triangle-alert`, `globe`, `map-pin`,
  `arrow-right`, `download`

Tailles : 18 à 24 px dans une ligne de texte ou une pastille, 30 à 44 px pour
une carte. Un pictogramme or signale un contenu, un pictogramme noir signale un
acteur ou un appareil, un pictogramme blanc ne sert que sur fond sombre.

## 4. Composition type

Pour une planche paysage insérée dans un document Word :

1. Titre Georgia 26 à 30 px, sous-titre Arial 13 à 14 px en gris, filet or de
   3 px sur toute la largeur utile.
2. Deux ou trois zones maximum, titrées en capitales Arial 12 or, sur fond
   `#F5F6F7` arrondi (`arcSize=4`).
3. Des cartes de 80 à 120 px de haut, pictogramme à gauche, titre en gras,
   précision en 9 ou 10 px gris.
4. Un bandeau noir final de 40 à 48 px avec trois pictogrammes blancs et des
   libellés or. C'est la synthèse en une ligne.
5. Marges de 40 px, gouttières de 20 px. Une seule idée par carte.

Deux flèches croisées suffisent : le flux principal en or, les retours ou les
mises à jour en pointillé or.

## 5. Export

```bash
# Aperçu pour contrôle visuel (sans XML embarqué)
/Applications/draw.io.app/Contents/MacOS/draw.io \
  --export --format png --scale 2 --border 20 \
  -o schema.png schema.drawio
```

Sans le binaire draw.io : `python3 scripts/validate.py schema.drawio --score`
contrôle la structure, puis livrer le `.drawio` (il reste éditable).

Ne pas utiliser `-e` pour l'aperçu : le PNG devient lourd et illisible pour
l'inspection. Réserver `-e` au PNG final si le destinataire veut rouvrir le
diagramme depuis l'image.

Insertion dans Word : section paysage, marges 1,2 cm, puis image à 26,6 cm de
large pour une A4. Renommer le fichier en majuscules avec la date du document.

## 6. Pièges

| Symptôme | Cause | Correction |
| --- | --- | --- |
| Icône cassée dans l'éditeur | `;` brut dans le data URI | passer par `ppicons.py`, qui écrit `%3B` |
| Icône cassée à l'export | SVG dans `image=` | rasteriser en PNG (fait par `ppicons.py`) |
| Image absente du `.drawio` envoyé | fichier lié par `file://` | data URI embarqué, jamais de chemin local |
| Texte noir sur fond noir | carte sombre + `extras.fontColor` global | écriture blanche portée par la cellule, pas par le preset |
| Rendu différent chez le destinataire | police non installée | Georgia et Arial uniquement |
| Diagramme flou dans Word | export à l'échelle 1 | exporter à `--scale 2` minimum |

## 7. Contrôles avant livraison

```bash
python3 scripts/validate.py schema.drawio --score    # structure
python3 scripts/ppicons.py list                       # noms exacts
grep -c "data:image/png%3Bbase64" schema.drawio       # icônes embarquées
```

Vérifier ensuite le rendu PNG à l'œil : chevauchements, libellés coupés,
flèches qui traversent une carte, pictogramme qui touche une bordure.
