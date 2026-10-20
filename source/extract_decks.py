"""Extract the game logic from every .pptx under versions/ into readable source.

A PowerPoint game has no compiled code: its "source" is the slide XML. For
each deck this writes, under source/<deck path>/:

  xml/      the deck's XML parts, pretty-printed (media files are skipped;
            the originals live in data/ and inside the .pptx)
  game.md   the game logic per slide: shapes, click/hover actions with
            resolved slide targets, auto-advance timers, media and
            animation triggers

Run from the project root:  python3 source/extract_decks.py
Requires: pip install defusedxml
Read-only on the decks; overwrites previous output in source/.
"""
import re
import sys
import zipfile
from pathlib import Path

# defusedxml blocks XXE / entity-expansion attacks from untrusted deck XML.
import defusedxml.ElementTree as ET
import defusedxml.minidom

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
R_ID = "{%s}id" % NS["r"]
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "source"

SHOW_JUMPS = {
    "nextslide": "next slide", "previousslide": "previous slide",
    "firstslide": "first slide", "lastslide": "last slide",
    "endshow": "END SHOW", "lastslideviewed": "last viewed slide",
}


def read_rels(z, part):
    """Return {rId: (target, is_external)} for one part's .rels file."""
    rels_path = re.sub(r"([^/]+)$", r"_rels/\1.rels", part)
    if rels_path not in z.namelist():
        return {}
    root = ET.fromstring(z.read(rels_path))
    return {
        rel.get("Id"): (rel.get("Target"), rel.get("TargetMode") == "External")
        for rel in root
    }


def slide_order(z):
    """Return slide part paths in presentation order."""
    pres = ET.fromstring(z.read("ppt/presentation.xml"))
    rels = read_rels(z, "ppt/presentation.xml")
    return ["ppt/" + rels[s.get(R_ID)][0] for s in pres.iterfind("p:sldIdLst/p:sldId", NS)]


def describe_action(link, rels, slide_numbers):
    """Turn an a:hlinkClick / a:hlinkHover element into readable text."""
    action = link.get("action", "")
    target, external = rels.get(link.get(R_ID), ("", False))
    if "hlinksldjump" in action:
        name = target.split("/")[-1]
        return "go to slide %s" % slide_numbers.get(name, "? (%s)" % name)
    if "hlinkshowjump" in action:
        jump = action.split("jump=")[-1]
        return SHOW_JUMPS.get(jump, jump)
    if action == "ppaction://noaction":
        return None
    if action == "ppaction://program":
        return "RUN PROGRAM: %s" % target.replace("%20", " ").replace("%22", '"')
    if action == "ppaction://media":
        return "play media"
    if action:
        return action
    return "open %s" % target if target else None


def shape_rows(sp_tree, rels, slide_numbers):
    """Yield (id, kind, name, text, click, hover, media) for every shape, recursing into groups."""
    for el in sp_tree:
        tag = el.tag.split("}")[-1]
        if tag == "grpSp":
            yield from shape_rows(el, rels, slide_numbers)
            continue
        if tag not in ("sp", "pic", "cxnSp", "graphicFrame"):
            continue
        cnv = el.find(".//p:cNvPr", NS)
        if cnv is None:
            continue
        text = " / ".join(t.text for t in el.iterfind(".//a:t", NS) if t.text and t.text.strip())
        click = hover = None
        for link in el.iter():
            kind = link.tag.split("}")[-1]
            if kind == "hlinkClick":
                click = click or describe_action(link, rels, slide_numbers)
            elif kind == "hlinkHover":
                hover = hover or describe_action(link, rels, slide_numbers)
        media = []
        for ref in el.iter():
            rid = ref.get(R_ID) or ref.get("{%s}link" % NS["r"]) or ref.get("{%s}embed" % NS["r"])
            if rid in rels and ref.tag.split("}")[-1] in ("audioFile", "videoFile", "wavAudioFile"):
                target, external = rels[rid]
                media.append(("LINKED " if external else "") + target.split("\\")[-1].split("/")[-1])
        yield (cnv.get("id"), tag, cnv.get("name", ""), cnv.get("descr", ""), text, click, hover, media)


def animation_rows(slide, names):
    """Yield readable lines for each animation effect and what starts it."""
    timing = slide.find("p:timing", NS)
    if timing is None:
        return
    parents = {child: parent for parent in timing.iter() for child in parent}
    for ctn in timing.iter("{%s}cTn" % NS["p"]):
        preset = ctn.get("presetClass")
        if not preset:
            continue
        targets = {t.get("spid") for t in ctn.iterfind(".//p:tgtEl/p:spTgt", NS)}
        start = "on slide load" if ctn.get("nodeType") != "clickEffect" else "on click"
        node = ctn
        while node in parents:
            node = parents[node]
            trig = node.find("p:stCondLst/p:cond[@evt='onClick']/p:tgtEl/p:spTgt", NS)
            if trig is not None:
                start = "when '%s' is clicked" % names.get(trig.get("spid"), trig.get("spid"))
                break
        label = {"entr": "appear", "exit": "disappear", "emph": "emphasis",
                 "path": "motion path", "mediacall": "play/stop media"}.get(preset, preset)
        repeat = " (loops)" if ctn.get("repeatCount") == "indefinite" else ""
        for spid in sorted(targets):
            yield "%s -> %s%s: '%s'" % (start, label, repeat, names.get(spid, spid))


def deck_to_markdown(z, deck_name):
    """Build the game.md text for one deck."""
    slides = slide_order(z)
    slide_numbers = {path.split("/")[-1]: i for i, path in enumerate(slides, 1)}
    out = ["# %s" % deck_name, "", "%d slides. Slide numbers are show order." % len(slides), ""]
    for number, part in enumerate(slides, 1):
        slide = ET.fromstring(z.read(part))
        rels = read_rels(z, part)
        hidden = " (HIDDEN)" if slide.get("show") == "0" else ""
        out.append("## Slide %d — `%s`%s" % (number, part.split("/")[-1], hidden))
        trans = slide.find("p:transition", NS)
        if trans is not None:
            adv = trans.get("advTm")
            on_click = trans.get("advClick", "1") != "0"
            if adv:
                out.append("- Auto-advance after %.1f s%s" % (int(adv) / 1000, "" if on_click else ", click disabled"))
            elif not on_click:
                out.append("- Click-to-advance disabled")
        rows = list(shape_rows(slide.find("p:cSld/p:spTree", NS), rels, slide_numbers))
        names = {r[0]: r[2] for r in rows}
        for _id, kind, name, descr, text, click, hover, media in rows:
            parts = ["**%s**" % name]
            if descr:
                parts.append("[%s]" % descr)
            if text:
                parts.append('"%s"' % text)
            if click:
                parts.append("CLICK: %s" % click)
            if hover:
                parts.append("HOVER: %s" % hover)
            if media:
                parts.append("MEDIA: %s" % ", ".join(media))
            if text or click or hover or media or kind == "pic":
                out.append("- " + " — ".join(parts))
        anims = list(animation_rows(slide, names))
        if anims:
            out.append("- Animations:")
            out.extend("  - " + a for a in anims)
        out.append("")
    return "\n".join(out)


def extract(deck):
    """Write xml/ and game.md for one deck."""
    rel = deck.relative_to(ROOT / "versions").with_suffix("")
    dest = OUT / rel
    with zipfile.ZipFile(deck) as z:
        for name in z.namelist():
            if name.startswith("ppt/media/") or name.endswith("/"):
                continue
            target = dest / "xml" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            data = z.read(name)
            if name.endswith((".xml", ".rels")):
                data = defusedxml.minidom.parseString(data).toprettyxml(indent="  ").encode("utf-8")
            target.write_bytes(data)
        (dest / "game.md").write_text(deck_to_markdown(z, str(rel)), encoding="utf-8")
    print("wrote", dest.relative_to(ROOT))


if __name__ == "__main__":
    decks = sorted((ROOT / "versions").rglob("*.pptx"))
    if not decks:
        sys.exit("no .pptx files under versions/")
    for deck in decks:
        extract(deck)
