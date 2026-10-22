#!/usr/bin/env python3
"""Exemple : planche aux couleurs de sahelcyber.com.

Montre la charte décrite dans references/sahelcyber.md : trois étapes à
gauche, un panneau encre à droite, un bandeau de synthèse.
Les pictogrammes viennent de scripts/ppicons.py.

    python3 examples/sahelcyber/demo-charte.py
    python3 skills/drawio-skill/scripts/validate.py examples/sahelcyber/demo-charte.drawio --score

Chaque carte et chaque panneau est un conteneur : ses textes et son
pictogramme sont ses enfants, donc ils suivent le bloc quand on le déplace
dans draw.io. Adapter les libellés et les coordonnées ; la charte ne change pas.
"""

import sys
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "skills" / "drawio-skill" / "scripts"))

import ppicons  # noqa: E402

W, H = 900, 660
OUT = HERE / "demo-charte.drawio"

BRAND = ppicons.BRAND      # #683EE5
DEEP = ppicons.COLORS["violet-fonce"]   # #4B2FBF
INK = ppicons.INK          # #0A1233
AMBER = ppicons.AMBER      # #F59E0B
SOFT = "#F4F1FE"
LIGHT = "#EFF1F8"
BORDER = "#C9CEE3"
MUTED = "#5B6079"
WHITE = "#FFFFFF"

cells = []

# Styles -------------------------------------------------------------------

TITLE = (
    "text;html=1;align=left;verticalAlign=middle;fontFamily=Arial;fontSize=26;"
    "fontColor=%s;fontStyle=1;" % INK
)
SUBTITLE = (
    "text;html=1;align=left;verticalAlign=middle;fontFamily=Arial;fontSize=13;"
    "fontColor=%s;" % MUTED
)
CARD = (
    "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;"
    "strokeWidth=1;" % (WHITE, BORDER)
)
CARD_TITLE = (
    "text;html=1;whiteSpace=wrap;align=left;verticalAlign=middle;fontFamily=Arial;fontSize=13;"
    "fontColor=%s;fontStyle=1;" % INK
)
CARD_DESC = (
    "text;html=1;whiteSpace=wrap;align=left;verticalAlign=top;fontFamily=Arial;fontSize=9;"
    "fontColor=%s;" % MUTED
)
RULE = "rounded=0;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;" % (BRAND, BRAND)
PANEL = (
    "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;"
    "strokeWidth=1;" % (INK, INK)
)
PANEL_TITLE = (
    "text;html=1;align=center;verticalAlign=middle;fontFamily=Arial;fontSize=17;"
    "fontColor=%s;fontStyle=1;" % WHITE
)
PANEL_NOTE = (
    "text;html=1;align=center;verticalAlign=middle;fontFamily=Arial;fontSize=10;"
    "fontColor=%s;" % BORDER
)
PILL = (
    "rounded=1;arcSize=50;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;"
    "strokeWidth=1.5;fontFamily=Arial;fontSize=11;fontColor=%s;"
    "align=center;verticalAlign=middle;" % (SOFT, BRAND, INK)
)
BAND = "rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;" % (
    INK,
    INK,
)
BAND_TEXT = (
    "text;html=1;align=left;verticalAlign=middle;fontFamily=Arial;fontSize=11;"
    "fontColor=%s;" % AMBER
)
BADGE = (
    "rounded=1;arcSize=50;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;"
    "fontFamily=Arial;fontSize=9;fontColor=%s;fontStyle=1;"
    "align=center;verticalAlign=middle;" % (INK, INK, WHITE)
)
ARROW = (
    "endArrow=block;html=1;rounded=0;strokeColor=%s;strokeWidth=2;"
    "fontFamily=Arial;fontSize=9;fontColor=%s;" % (BRAND, MUTED)
)
ARROW_DASHED = (
    "endArrow=block;html=1;rounded=0;dashed=1;dashPattern=6 4;strokeColor=%s;"
    "strokeWidth=1.5;" % BRAND
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

add("title", "Chaîne de confiance Sahel CyBER", TITLE, 40, 24, 640, 34)
add(
    "subtitle",
    "Auditer, durcir, superviser : la charte du site appliquée à draw.io",
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
    ("c1", "shield-check", BRAND, "1. Auditer l'existant",
     "Cartographie, tests d'intrusion, revue des accès et des sauvegardes."),
    ("c2", "lock", INK, "2. Durcir les systèmes",
     "Moindre privilège, chiffrement, correctifs, journalisation centralisée."),
    ("c3", "server", BRAND, "3. Superviser en continu",
     "Alertes, revue des journaux, plan de réponse et exercices de crise."),
]

for index, (cid, icon_name, color, title, desc) in enumerate(STEPS):
    add(cid, "", CARD, 40, 132 + index * 140, 350, 112)
    icon("icon-%s" % cid, icon_name, color, 22, 24, 30, parent=cid)
    add("%s-title" % cid, "<b>%s</b>" % title, CARD_TITLE, 64, 14, 268, 24, parent=cid)
    add("%s-desc" % cid, desc, CARD_DESC, 64, 42, 268, 58, parent=cid)

edge("e1", ARROW + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;", "c1", "c2")
edge("e2", ARROW + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;", "c2", "c3")

# Panneau encre ------------------------------------------------------------

add("panel", "", PANEL, 470, 150, 300, 410)
add("panel-title", "<b>Infrastructure souveraine</b>", PANEL_TITLE, 10, 20, 248, 28,
    parent="panel")
add("panel-rule", "", RULE, 24, 52, 220, 2, parent="panel")

for index, label in enumerate(
    ("Audit et tests d'intrusion", "Durcissement des serveurs", "Supervision 24/7")
):
    add("pill-%d" % index, label, PILL, 14, 68 + index * 44, 240, 30, parent="panel")

add("panel-note", "Données hébergées au Niger,<br>hors cloud étranger", PANEL_NOTE,
    10, 202, 248, 32, parent="panel")
add("panel-dot", "",
    "ellipse;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;" % (AMBER, AMBER),
    114, 246, 30, 30, parent="panel")
icon("icon-ready", "check", INK, 7, 7, 16, parent="panel-dot")
add("panel-ready", "Prestataire local",
    "text;html=1;align=center;verticalAlign=middle;fontFamily=Arial;fontSize=9;"
    "fontColor=%s;" % BORDER, 10, 284, 248, 18, parent="panel")
add("panel-sign-rule", "",
    "rounded=0;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;"
    % ("#2A3566", "#2A3566"), 24, 344, 220, 1, parent="panel")
add("panel-sign", "sahelcyber.com",
    "text;html=1;align=center;verticalAlign=middle;fontFamily=Arial;fontSize=9;"
    "fontColor=%s;" % BORDER, 10, 354, 248, 18, parent="panel")

# Badge hébergement
icon("icon-host", "map-pin", INK, 520, 116, 16)
add("host", "HÉBERGÉ AU NIGER", BADGE, 544, 112, 200, 24)

edge("e3", ARROW_DASHED + "exitX=1;exitY=0.5;entryX=0;entryY=0.85;", "c3", "panel")

# Bandeau de synthèse ------------------------------------------------------

add("band", "", BAND, 40, 584, 820, 46)
icon("icon-net", "globe", WHITE, 21, 13, 20, parent="band")
add("band-1", "Réseau maîtrisé", BAND_TEXT, 48, 0, 240, 46, parent="band")
icon("icon-data", "database", WHITE, 309, 13, 20, parent="band")
add("band-2", "Données locales", BAND_TEXT, 336, 0, 270, 46, parent="band")
icon("icon-trace", "shield-check", WHITE, 627, 13, 20, parent="band")
add("band-3", "Traçabilité", BAND_TEXT, 654, 0, 160, 46, parent="band")

# Écriture -----------------------------------------------------------------

xml = (
    '<mxfile host="local" type="device">'
    '<diagram id="sahelcyber-demo" name="Chaîne de confiance">'
    '<mxGraphModel dx="900" dy="660" grid="0" gridSize="10" guides="1" tooltips="1" '
    'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="%d" '
    'pageHeight="%d" background="%s" math="0" shadow="0">'
    '<root><mxCell id="0"/><mxCell id="1" parent="0"/>%s</root>'
    "</mxGraphModel></diagram></mxfile>"
    % (W, H, WHITE, "".join(cells))
)

OUT.write_text(xml, encoding="utf-8")
print("schéma généré : %s (%d Ko, %d cellules)" % (OUT, len(xml) // 1024, len(cells)))
