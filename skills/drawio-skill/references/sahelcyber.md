# Sahel CyBER : charte, preset et pictogrammes

À lire dès qu'un diagramme porte la marque Sahel CyBER : proposition commerciale,
note de cadrage, rapport d'audit, support de formation, présentation client.

Le guide couvre trois choses : la charte relevée sur le site, le preset
`sahelcyber` (preset par défaut), et les pictogrammes de `scripts/ppicons.py`.

## 1. Charte

Couleurs relevées sur https://sahelcyber.com le 22 octobre 2026, sur les styles
calculés de la page d'accueil :

| Rôle | Code | Usage |
| --- | --- | --- |
| Violet | `#683EE5` | accents, filets, traits, icônes, flèches |
| Violet foncé | `#4B2FBF` | texte sur lavande, dégradés |
| Encre | `#0A1233` | texte, panneaux sombres, bandeaux |
| Ambre | `#F59E0B` | pastilles, chiffres clés, libellés sur fond sombre |
| Orange | `#F97316` | appel à l'action, alerte douce |
| Lavande | `#E6E1FB` | cartes secondaires, fonds de bloc |
| Brume | `#EFF1F8` | fond de zone |
| Bordure | `#C9CEE3` | contours discrets |
| Blanc | `#FFFFFF` | fond de page, cartes |

Le site combine trois matières : un fond encre, des blocs violets, des touches
ambre et orange. Un diagramme de marque reprend cet ordre : fond clair pour
l'impression, un seul panneau encre pour le bloc clé, l'ambre réservé aux
signaux (chiffre, pastille, libellé sur fond sombre).

Typographie : **Arial** partout, titres en gras. Le site charge une sans
géométrique en CSS, non installée sur les postes Windows des destinataires ;
Arial garde un rendu identique dans draw.io et dans Word. Si la police du site
est installée sur le poste qui produit le document, remplacer
`font.fontFamily` dans le preset, puis régénérer.

## 2. Preset `sahelcyber`

Deux fichiers, un seul comportement :

- `styles/built-in/sahelcyber.json` : livré avec le dépôt, `"default": false` ;
- `~/.drawio-skill/styles/sahelcyber.json` : copie de travail,
  `"default": true`. C'est elle qui fait de `sahelcyber` le preset appliqué à
  tous les nouveaux diagrammes.

Seuls les presets utilisateur peuvent être `default: true`. Ne pas modifier le
fichier livré pour cela : le test des presets intégrés le refuse.

Pour re-thémer un diagramme existant, nommer le preset explicitement :

```bash
python3 scripts/restyle.py schema.drawio --preset sahelcyber -o schema-mkt.drawio
```

Correspondance des rôles :

| Rôle | Rendu |
| --- | --- |
| service | carte blanche, contour violet |
| gateway | carte ambre pâle `#FFF8E8`, contour ambre |
| queue | carte orangée `#FFF3E6`, contour orange |
| database | carte lavande `#E6E1FB`, contour violet foncé |
| external | carte brume `#EFF1F8`, contour `#C9CEE3` |
| security | carte lavande claire `#F4F1FE`, contour violet |
| error | carte blanche, contour `#DC2626` |

Le preset ne donne que couleurs, formes, police et style d'arête. Les
espacements, la hiérarchie et les zones restent à la charge de l'auteur.

`restyle.py` remappe les couleurs par teinte. Sur une planche déjà composée,
un bandeau noir peut devenir gris clair et perdre son contraste. Pour un
document de marque, régénérer la planche avec le preset plutôt que de restyler
un ancien fichier.

## 3. Pictogrammes

```bash
# Lister les pictogrammes disponibles
python3 scripts/ppicons.py list

# Écrire un SVG (aucune dépendance)
python3 scripts/ppicons.py svg shield-check -o /tmp/shield.svg

# Écrire un PNG transparent
python3 scripts/ppicons.py png cloud --color encre --size 256 -o /tmp/cloud.png

# Style complet, à insérer tel quel dans un attribut style=""
python3 scripts/ppicons.py uri code --style

# Sommet <mxCell> prêt à coller dans un mxGraphModel
python3 scripts/ppicons.py cell lock --id icon-lock --x 80 --y 200
```

Couleurs acceptées : `violet` (défaut), `violet-fonce`, `encre`, `ambre`,
`or`, `noir`, `blanc`, `gris`, ou un code `#RRGGBB`. Les quatre dernières
appartiennent à la charte PetitPouss, conservée pour les documents de l'ONG.

Familles disponibles :

- **Personnes** : `users`, `user-round`, `cap`, `standing`
- **Contenus** : `file-text`, `messages`, `book-open`, `calendar`
- **Voix et image** : `mic`, `camera`
- **Technique** : `cpu`, `sparkles`, `tablet`, `database`, `server`, `cloud`,
  `code`, `wifi`, `wifi-off`, `lock`, `shield-check`
- **Repères** : `check`, `circle-check`, `triangle-alert`, `globe`, `map-pin`,
  `arrow-right`, `download`

Tailles : 18 à 24 px dans une ligne de texte ou une pastille, 30 à 44 px pour
une carte. Sur fond clair, un pictogramme violet signale un contenu et un
pictogramme encre un acteur ou un appareil. Sur panneau encre, inverser :
blanc pour les traits, ambre pour le signal.

## 4. Composition type

Pour une planche paysage insérée dans un document Word :

1. Titre Arial 26 en gras, encre, sous-titre 13 en gris bleuté `#5B6079`,
   filet violet de 3 px sur toute la largeur utile.
2. Deux ou trois zones maximum. Cartes blanches sur fond brume, bordure
   `#C9CEE3`, rayon 8.
3. Des cartes de 80 à 120 px de haut, pictogramme à gauche, titre en gras,
   précision en 9 ou 10 px gris.
4. Un panneau encre `#0A1233` pour le bloc clé : titre blanc, pilules lavande
   bordées de violet, pastille ambre. C'est le point que l'œil doit retenir.
5. Un bandeau encre final de 40 à 48 px, pictogrammes blancs et libellés ambre.
   C'est la synthèse en une ligne.

Marges de 40 px, gouttières de 20 px, une seule idée par carte. Deux flèches
suffisent : le flux principal en violet plein, les retours ou mises à jour en
pointillé violet.

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
| Texte invisible sur panneau encre | `fontColor` global encre | écrire la couleur blanche sur chaque cellule du panneau |
| Pastille ambre illisible | coche blanche sur ambre | coche encre sur fond ambre |
| Rendu différent chez le destinataire | police non installée | Arial uniquement |
| Diagramme flou dans Word | export à l'échelle 1 | exporter à `--scale 2` minimum |

## 7. Contrôles avant livraison

```bash
python3 scripts/validate.py schema.drawio --score    # structure
python3 scripts/ppicons.py list                       # noms exacts
grep -c "data:image/png%3Bbase64" schema.drawio       # icônes embarquées
```

Vérifier ensuite le rendu PNG à l'œil : chevauchements, libellés coupés,
flèches qui traversent une carte, pictogramme qui touche une bordure,
contraste du panneau encre.

Exemple complet : `examples/sahelcyber/demo-charte.py`.
