#!/usr/bin/env python3
"""ppicons - pictogrammes de marque pour diagrammes draw.io.

Charte Sahel CyBER (defaut) : violet #683EE5, encre #0A1233, ambre #F59E0B,
violet fonce #4B2FBF. Charte PetitPouss conservee : or #D4A800, noir #1A1D20.

    python3 scripts/ppicons.py list
    python3 scripts/ppicons.py svg users --color or --out /tmp/users.svg
    python3 scripts/ppicons.py png tablet --color noir --size 256 --out /tmp/tablet.png
    python3 scripts/ppicons.py uri users --color or --style
    python3 scripts/ppicons.py cell users --id icon-users --color noir --x 80 --y 200

Pourquoi rasteriser : la CLI draw.io n'accepte pas les SVG en data URI, et son
analyseur de style coupe sur ';'. Un PNG encode en `data:image/png%3Bbase64,...`
s'affiche dans l'editeur et sort correctement a l'export. Le `%3B` est
obligatoire : un `;` brut casse l'image.

Dependance : PyMuPDF (`pip install pymupdf`), uniquement pour png/uri/cell.
Les commandes list et svg restent en bibliotheque standard.

Les tracés suivent la grille 24x24 de Lucide (licence MIT).
"""

import argparse
import base64
import sys
from xml.sax.saxutils import quoteattr

# ---------------------------------------------------------------------------
# Charte
# ---------------------------------------------------------------------------

COLORS = {
    # Charte Sahel CyBER, relevee sur sahelcyber.com
    "violet": "#683EE5",
    "violet-fonce": "#4B2FBF",
    "encre": "#0A1233",
    "ambre": "#F59E0B",
    # Charte PetitPouss
    "or": "#D4A800",
    "noir": "#1A1D20",
    "blanc": "#FFFFFF",
    "gris": "#5A5D60",
}

BRAND = COLORS["violet"]
INK = COLORS["encre"]
AMBER = COLORS["ambre"]
GOLD = COLORS["or"]
DARK = COLORS["noir"]
WHITE = COLORS["blanc"]

# ---------------------------------------------------------------------------
# Pictogrammes
# ---------------------------------------------------------------------------

ICONS = {
    # Personnes et rôles
    "users": (
        '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>'
        '<circle cx="9" cy="7" r="4"/>'
        '<path d="M22 21v-2a4 4 0 0 0-3-3.87"/>'
        '<path d="M16 3.13a4 4 0 0 1 0 7.75"/>'
    ),
    "user-round": '<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/>',
    "cap": (
        '<path d="M21.4 10.9a1 1 0 0 0 0-1.8L12.8 5.2a2 2 0 0 0-1.7 0L2.6 9.1a1 1 0 0 0 0 1.8'
        'l8.6 3.9a2 2 0 0 0 1.7 0z"/>'
        '<path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>'
    ),
    "standing": (
        '<circle cx="12" cy="5" r="1"/>'
        '<path d="m9 20 3-6 3 6"/><path d="m6 8 6 2 6-2"/><path d="M12 10v4"/>'
    ),
    # Contenus pédagogiques
    "file-text": (
        '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>'
        '<path d="M14 2v5h5"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/>'
    ),
    "messages": (
        '<path d="M14 9a2 2 0 0 1-2 2H6l-4 4V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2z"/>'
        '<path d="M18 9h2a2 2 0 0 1 2 2v11l-4-4h-6a2 2 0 0 1-2-2v-1"/>'
    ),
    "book-open": (
        '<path d="M12 7v14"/>'
        '<path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5'
        'a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/>'
    ),
    "calendar": (
        '<path d="M8 2v4"/><path d="M16 2v4"/>'
        '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>'
    ),
    # Voix, image, gestes
    "mic": (
        '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>'
        '<path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/>'
    ),
    "camera": (
        '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9'
        'a2 2 0 0 0-2-2h-3l-2.5-3z"/>'
        '<circle cx="12" cy="13" r="3"/>'
    ),
    # Technique
    "cpu": (
        '<rect width="16" height="16" x="4" y="4" rx="2"/>'
        '<rect width="6" height="6" x="9" y="9" rx="1"/>'
        '<path d="M15 2v2M15 20v2M2 15h2M2 9h2M20 15h2M20 9h2M9 2v2M9 20v2"/>'
    ),
    "sparkles": (
        '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936'
        'A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 '
        '9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 '
        '6.135a.5.5 0 0 1-.963 0z"/>'
    ),
    "tablet": (
        '<rect width="16" height="20" x="4" y="2" rx="2" ry="2"/>'
        '<line x1="12" x2="12.01" y1="18" y2="18"/>'
    ),
    "database": (
        '<ellipse cx="12" cy="5" rx="9" ry="3"/>'
        '<path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/>'
    ),
    "server": (
        '<rect width="20" height="8" x="2" y="2" rx="2" ry="2"/>'
        '<rect width="20" height="8" x="2" y="14" rx="2" ry="2"/>'
        '<line x1="6" x2="6.01" y1="6" y2="6"/><line x1="6" x2="6.01" y1="18" y2="18"/>'
    ),
    "cloud": '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>',
    "code": (
        '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>'
    ),
    "wifi": (
        '<path d="M12 20h.01"/><path d="M2 8.82a15 15 0 0 1 20 0"/>'
        '<path d="M5 12.859a10 10 0 0 1 14 0"/><path d="M8.5 16.429a5 5 0 0 1 7 0"/>'
    ),
    "wifi-off": (
        '<path d="M12 20h.01"/><path d="M8.5 16.4a5 5 0 0 1 7 0"/>'
        '<path d="M5 12.9a10 10 0 0 1 5.2-2.7"/><path d="M19 12.9a10 10 0 0 0-2-1.5"/>'
        '<path d="M2 8.8a15 15 0 0 1 4.2-2.6"/><path d="M22 8.8a15 15 0 0 0-11.3-3.8"/>'
        '<path d="m2 2 20 20"/>'
    ),
    "lock": (
        '<rect width="18" height="11" x="3" y="11" rx="2"/>'
        '<path d="M7 11V7a5 5 0 0 1 10 0v4"/>'
    ),
    "shield-check": (
        '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6'
        'a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5'
        'a1 1 0 0 1 1 1z"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    # Symboles et repères
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "circle-check": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "triangle-alert": (
        '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16'
        'a2 2 0 0 0 1.73-3"/>'
        '<path d="M12 9v4"/><path d="M12 17h.01"/>'
    ),
    "globe": (
        '<circle cx="12" cy="12" r="10"/>'
        '<path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/>'
        '<path d="M2 12h20"/>'
    ),
    "map-pin": (
        '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0'
        'C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/>'
        '<circle cx="12" cy="10" r="3"/>'
    ),
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "download": (
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
        '<polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>'
    ),
}

LABELS = {
    "users": "groupe, acteurs",
    "user-round": "personne, enfant",
    "cap": "enseignant, école",
    "standing": "accessibilité, handicap",
    "file-text": "document, contenu",
    "messages": "échange, question / réponse",
    "book-open": "leçon, programme",
    "calendar": "calendrier, planning",
    "mic": "voix, audio, langue",
    "camera": "gestes filmés, vidéo",
    "cpu": "modèle embarqué, calcul",
    "sparkles": "intelligence artificielle",
    "tablet": "tablette, appareil",
    "database": "données, stockage",
    "server": "serveur, bureau",
    "cloud": "cloud, hébergement",
    "code": "développement, logiciel",
    "wifi": "connexion",
    "wifi-off": "hors ligne",
    "lock": "maîtrise, verrouillage",
    "shield-check": "protection, conformité",
    "check": "validation",
    "circle-check": "réussi, prêt",
    "triangle-alert": "alerte, limite",
    "globe": "langues, pays",
    "map-pin": "lieu, région",
    "arrow-right": "flux, étape",
    "download": "installation, mise à jour",
}

# ---------------------------------------------------------------------------
# Rendu
# ---------------------------------------------------------------------------

PAD = 1.6          # marge du viewBox : évite que le trait soit rogné
STROKE = 1.7       # épaisseur du trait, en unités de la grille 24


def resolve_color(value):
    """Accepte un nom de la charte (violet, encre, ambre, or, noir, blanc, gris)
    ou un code #RRGGBB."""
    key = value.lower().lstrip("#")
    if key in COLORS:
        return COLORS[key]
    if len(value) == 7 and value.startswith("#"):
        return value.upper()
    if len(value) == 6:
        return "#" + value.upper()
    raise ValueError(
        "couleur inconnue : %s (attendu : %s ou #RRGGBB)"
        % (value, ", ".join(COLORS))
    )


def svg(name, color=BRAND, stroke=STROKE, pad=PAD):
    """Renvoie le SVG complet du pictogramme."""
    if name not in ICONS:
        raise KeyError("pictogramme inconnu : %s" % name)
    size = 24 + 2 * pad
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="%g" height="%g" '
        'viewBox="%s %s %s %s" fill="none" stroke="%s" stroke-width="%s" '
        'stroke-linecap="round" stroke-linejoin="round">%s</svg>'
        % (
            size,
            size,
            -pad,
            -pad,
            size,
            size,
            color,
            stroke,
            ICONS[name],
        )
    )


def png(name, color=BRAND, size=256, stroke=STROKE):
    """Rasterise le pictogramme en PNG transparent (necessite PyMuPDF)."""
    try:
        import pymupdf
    except ImportError:  # pragma: no cover - dependance optionnelle
        sys.exit(
            "PyMuPDF est requis pour png/uri/cell :\n"
            "  python3 -m pip install pymupdf\n"
            "ou :\n"
            "  python3 -m venv /tmp/ppicons && /tmp/ppicons/bin/pip install pymupdf"
        )
    markup = svg(name, color, stroke)
    doc = pymupdf.open(stream=markup.encode(), filetype="svg")
    scale = size / (24 + 2 * PAD)
    pix = doc[0].get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=True)
    return pix.tobytes("png")


def data_uri(name, color=BRAND, size=256, stroke=STROKE):
    """Data URI directement utilisable dans un style draw.io."""
    blob = png(name, color, size, stroke)
    # Le point-virgule doit etre encode : le parseur de style draw.io coupe sur ';'.
    return "data:image/png%3Bbase64," + base64.b64encode(blob).decode()


def image_style(name, color=BRAND, size=256, stroke=STROKE):
    """Style complet d'un sommet image."""
    return "shape=image;html=1;imageAspect=1;image=%s;" % data_uri(
        name, color, size, stroke
    )


def cell(cid, name, color=BRAND, x=0, y=0, size=32, parent="1"):
    """Sommet <mxCell> pret a coller dans un mxGraphModel."""
    return (
        '<mxCell id=%s value="" style=%s vertex="1" parent=%s>'
        '<mxGeometry x="%s" y="%s" width="%s" height="%s" as="geometry"/></mxCell>'
        % (
            quoteattr(str(cid)),
            quoteattr(image_style(name, color)),
            quoteattr(str(parent)),
            x,
            y,
            size,
            size,
        )
    )


# ---------------------------------------------------------------------------
# Ligne de commande
# ---------------------------------------------------------------------------


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="ppicons",
        description="Pictogrammes de marque pour draw.io (violet #683EE5 par defaut).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="lister les pictogrammes")
    p_list.add_argument("--names", action="store_true", help="noms seuls, pour un script")

    for name, helptext in (
        ("svg", "ecrire le SVG"),
        ("png", "ecrire le PNG"),
        ("uri", "afficher le data URI ou le style draw.io"),
        ("cell", "afficher un <mxCell> pret a coller"),
    ):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("icon", choices=sorted(ICONS), help="nom du pictogramme")
        p.add_argument(
            "--color",
            default="violet",
            help="violet, encre, ambre, or, noir, blanc, gris ou #RRGGBB",
        )
        p.add_argument("--stroke", type=float, default=STROKE, help="epaisseur du trait")
        if name == "uri":
            p.add_argument("--size", type=int, default=256, help="resolution du PNG embarque")
            p.add_argument("--style", action="store_true", help="sortir le style draw.io complet")
        elif name == "cell":
            p.add_argument("--size", type=int, default=32, help="cote du sommet, en pixels")
            p.add_argument("--x", type=float, default=0)
            p.add_argument("--y", type=float, default=0)
            p.add_argument("--id", default="icon", help="identifiant de la cellule")
            p.add_argument("--parent", default="1")
        else:
            p.add_argument("--size", type=int, default=256, help="cote du PNG, en pixels")
            p.add_argument("--out", "-o", help="fichier de sortie (defaut : stdout)")

    args = parser.parse_args(argv)

    if args.command == "list":
        if args.names:
            print(" ".join(sorted(ICONS)))
            return 0
        width = max(len(n) for n in ICONS) + 2
        for name in sorted(ICONS):
            print("%-*s %s" % (width, name, LABELS.get(name, "")))
        return 0

    try:
        color = resolve_color(args.color)
    except ValueError as exc:
        parser.error(str(exc))

    if args.command == "svg":
        markup = svg(args.icon, color, args.stroke)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as handle:
                handle.write(markup)
        else:
            print(markup)
        return 0

    if args.command == "png":
        blob = png(args.icon, color, args.size, args.stroke)
        if args.out:
            with open(args.out, "wb") as handle:
                handle.write(blob)
        else:
            sys.stdout.buffer.write(blob)
        return 0

    if args.command == "uri":
        if args.style:
            print(image_style(args.icon, color, args.size, args.stroke))
        else:
            print(data_uri(args.icon, color, args.size, args.stroke))
        return 0

    if args.command == "cell":
        print(
            cell(
                args.id,
                args.icon,
                color,
                args.x,
                args.y,
                args.size,
                args.parent,
            )
        )
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
