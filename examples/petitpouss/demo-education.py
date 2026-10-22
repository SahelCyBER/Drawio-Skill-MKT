#!/usr/bin/env python3
"""Exemple : planche pédagogique aux couleurs PetitPouss.

Montre la composition type décrite dans references/petitpouss.md :
trois étapes à gauche, la tablette à droite, un bandeau de synthèse.
Les pictogrammes viennent de scripts/ppicons.py.

    python3 examples/petitpouss/demo-education.py
    python3 skills/drawio-skill/scripts/validate.py examples/petitpouss/demo-education.drawio --score

Chaque carte est un conteneur : ses textes et son pictogramme sont ses enfants,
donc ils suivent la carte quand on la déplace dans draw.io. Adapter les
libellés et les coordonnées pour une autre note ; la charte ne change pas.
"""

import sys
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "skills" / "drawio-skill" / "scripts"))

import ppicons  # noqa: E402

W, H = 900, 660
OUT = HERE / "demo-education.drawio"

GOLD = ppicons.GOLD
DARK = ppicons.DARK
GRAY = "#5A5D60"
LIGHT = "#F5F6F7"
BORDER = "#EAEAEA"
WHITE = "#FFFFFF"

cells = []

# Styles -------------------------------------------------------------------

TITLE = (
    "text;html=1;align=left;verticalAlign=middle;fontFamily=Georgia;fontSize=26;"
    "fontColor=%s;fontStyle=1;" % DARK
)
SUBTITLE = (
    "text;html=1;align=left;verticalAlign=middle;fontFamily=Arial;fontSize=13;"
    "fontColor=%s;" % GRAY
)
CARD = (
    "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;"
    "strokeWidth=1;" % (LIGHT, BORDER)
)
CARD_TITLE = (
    "text;html=1;whiteSpace=wrap;align=left;verticalAlign=middle;fontFamily=Arial;fontSize=13;"
    "fontColor=%s;fontStyle=1;" % DARK
)
CARD_DESC = (
    "text;html=1;whiteSpace=wrap;align=left;verticalAlign=top;fontFamily=Arial;fontSize=9;"
    "fontColor=%s;" % GRAY
)
RULE = "rounded=0;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;" % (GOLD, GOLD)
PILL = (
    "rounded=1;arcSize=50;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;"
    "strokeWidth=1.5;fontFamily=Arial;fontSize=11;fontColor=%s;"
    "align=center;verticalAlign=middle;" % (WHITE, GOLD, DARK)
)
BAND = "rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;" % (
    DARK,
    DARK,
)
BAND_TEXT = (
    "text;html=1;align=left;verticalAlign=middle;fontFamily=Arial;fontSize=11;"
    "fontColor=%s;" % WHITE
)
BADGE = (
    "rounded=1;arcSize=50;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;"
    "fontFamily=Arial;fontSize=9;fontColor=%s;fontStyle=1;"
    "align=center;verticalAlign=middle;" % (DARK, DARK, WHITE)
)
ARROW = (
    "endArrow=block;html=1;rounded=0;strokeColor=%s;strokeWidth=2;"
    "fontFamily=Arial;fontSize=9;fontColor=%s;" % (GOLD, GRAY)
)
ARROW_DASHED = (
    "endArrow=block;html=1;rounded=0;dashed=1;dashPattern=6 4;strokeColor=%s;"
    "strokeWidth=1.5;" % GOLD
)


def add(cid, value, style, x, y, w, h, parent="1"):
    cells.append(
        '<mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s">'
        '<mxGeometry x="%s" y="%s" width="%s" height="%s" as="geometry"/></mxCell>'
        % (cid, escape(value, {'"': "&quot;"}), style, parent, x, y, w, h)
    )


def icon(cid, name, color, x, y, size, parent="1"):
    cells.append(ppicons.cell(cid, name, color, x, y, size, parent))


def edge(cid, style, source, target, label=""):
    cells.append(
        '<mxCell id="%s" value="%s" style="%s" edge="1" parent="1" '
        'source="%s" target="%s"><mxGeometry relative="1" as="geometry"/></mxCell>'
        % (cid, label, style, source, target)
    )


# En-tête ------------------------------------------------------------------

add("title", "École numérique PetitPouss", TITLE, 40, 24, 640, 34)
add(
    "subtitle",
    "Préparer les contenus, entraîner le modèle, équiper la classe",
    SUBTITLE,
    40,
    62,
    760,
    22,
)
add("rule", "", RULE, 40, 96, 820, 3)

# Trois étapes -------------------------------------------------------------
# Chaque carte mesure 350 x 112. Ses enfants sont positionnés dans son repère.

STEPS = [
    ("c1", "file-text", GOLD, "1. Contenus préparés",
     "Phrases, consignes et paires question / réponse, validées par les enseignants."),
    ("c2", "cpu", DARK, "2. Entraînement local",
     "Le modèle apprend sur la tablette, sans connexion. Les enseignants testent et corrigent."),
    ("c3", "tablet", DARK, "3. Tablette prête",
     "Réponses figées, contenus installés. La tablette part en classe."),
]

for index, (cid, icon_name, color, title, desc) in enumerate(STEPS):
    add(cid, "", CARD, 40, 132 + index * 140, 350, 112)
    icon("icon-%s" % cid, icon_name, color, 22, 24, 30, parent=cid)
    add("%s-title" % cid, "<b>%s</b>" % title, CARD_TITLE, 64, 14, 268, 24, parent=cid)
    add("%s-desc" % cid, desc, CARD_DESC, 64, 42, 268, 58, parent=cid)

# Pastille de validation, enfant de la carte d'entraînement
add("badge-dot", "",
    "ellipse;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;" % (GOLD, GOLD),
    34, 44, 16, 16, parent="c2")
icon("icon-check", "check", WHITE, 3, 3, 10, parent="badge-dot")

edge("e1", ARROW + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;", "c1", "c2")
edge("e2", ARROW + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;", "c2", "c3")

# Tablette -----------------------------------------------------------------

add("tablet-body", "",
    "rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;"
    % (DARK, DARK), 470, 150, 300, 410)
add("tablet-screen", "",
    "rounded=1;arcSize=5;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;"
    % (WHITE, BORDER), 16, 18, 268, 364, parent="tablet-body")

add("tablet-title", "<b>Assistant IA local</b>",
    "text;html=1;align=center;verticalAlign=middle;fontFamily=Georgia;fontSize=17;"
    "fontColor=%s;" % DARK, 10, 20, 248, 28, parent="tablet-screen")
add("tablet-rule", "", RULE, 24, 52, 220, 2, parent="tablet-screen")

for index, label in enumerate(("Langues nationales", "Voix et gestes", "Leçons et exercices")):
    add("pill-%d" % index, label, PILL, 14, 68 + index * 44, 240, 30,
        parent="tablet-screen")

add("tablet-note", "Réponses citées,<br>contenus validés",
    "text;html=1;align=center;verticalAlign=middle;fontFamily=Arial;fontSize=10;"
    "fontColor=%s;" % GRAY, 10, 202, 248, 32, parent="tablet-screen")
add("tablet-dot", "",
    "ellipse;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;" % (GOLD, GOLD),
    114, 246, 30, 30, parent="tablet-screen")
icon("icon-ready", "check", WHITE, 7, 7, 16, parent="tablet-dot")
add("tablet-ready", "Prêt pour la classe",
    "text;html=1;align=center;verticalAlign=middle;fontFamily=Arial;fontSize=9;"
    "fontColor=%s;" % GRAY, 10, 284, 248, 18, parent="tablet-screen")
add("tablet-home", "",
    "ellipse;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;" % (GOLD, GOLD),
    142, 390, 16, 16, parent="tablet-body")

# Badge hors ligne
icon("icon-offline", "wifi-off", DARK, 520, 116, 16)
add("offline", "AUCUNE CONNEXION INTERNET", BADGE, 544, 112, 200, 24)

edge("e3", ARROW_DASHED + "exitX=1;exitY=0.5;entryX=0;entryY=0.85;", "c3", "tablet-body")

# Bandeau de synthèse ------------------------------------------------------

add("band", "", BAND, 40, 584, 820, 46)
icon("icon-lang", "globe", WHITE, 21, 13, 20, parent="band")
add("band-1", "Langues nationales", BAND_TEXT, 48, 0, 240, 46, parent="band")
icon("icon-acc", "standing", WHITE, 309, 13, 20, parent="band")
add("band-2", "Voix, gestes, sous-titres", BAND_TEXT, 336, 0, 270, 46, parent="band")
icon("icon-lock", "lock", WHITE, 627, 13, 20, parent="band")
add("band-3", "Contenus maîtrisés", BAND_TEXT, 654, 0, 160, 46, parent="band")

# Écriture -----------------------------------------------------------------

xml = (
    '<mxfile host="local" type="device">'
    '<diagram id="petitpouss-demo" name="École numérique">'
    '<mxGraphModel dx="900" dy="660" grid="0" gridSize="10" guides="1" tooltips="1" '
    'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="%d" '
    'pageHeight="%d" background="%s" math="0" shadow="0">'
    '<root><mxCell id="0"/><mxCell id="1" parent="0"/>%s</root>'
    "</mxGraphModel></diagram></mxfile>"
    % (W, H, WHITE, "".join(cells))
)

OUT.write_text(xml, encoding="utf-8")
print("schéma généré : %s (%d Ko, %d cellules)" % (OUT, len(xml) // 1024, len(cells)))
