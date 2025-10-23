#!/usr/bin/env python3
"""
Export simple SVG images from VDX/.vsdx files produced in this workspace.

This script reads Visio XML (either a plain .vdx or a .vsdx ZIP containing visio/document.xml)
and renders each <Page> as a basic SVG: rectangles for shapes and text labels.

The output files are written next to the input file with names like
  <input_basename>_page_<pageid>.svg

This is intended for quick visual previews, not perfect Visio fidelity.
"""
import sys
import os
import zipfile
import xml.etree.ElementTree as ET
from typing import List, Dict


def read_document_xml(path: str) -> str:
    if path.lower().endswith('.vsdx'):
        # open as zip and read visio/document.xml
        with zipfile.ZipFile(path, 'r') as z:
            data = z.read('visio/document.xml')
            return data.decode('utf-8')
    else:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()


def localname(tag: str) -> str:
    if '}' in tag:
        return tag.split('}', 1)[1]
    return tag


def extract_pages(xml_text: str) -> List[Dict]:
    root = ET.fromstring(xml_text)
    pages = []
    # iterate children and find Page elements
    for page in list(root):
        if localname(page.tag) != 'Page':
            continue
        page_id = page.attrib.get('ID', '')
        page_name = page.attrib.get('Name', f'page_{page_id}')
        shapes_el = None
        for ch in list(page):
            if localname(ch.tag) == 'Shapes':
                shapes_el = ch
                break
        shapes = []
        if shapes_el is not None:
            for s in list(shapes_el):
                if localname(s.tag) != 'Shape':
                    continue
                sid = s.attrib.get('ID', '')
                stype = s.attrib.get('Type', '')
                name = s.attrib.get('Name', '')
                pinx = None
                piny = None
                width = None
                height = None
                text = ''
                # parse children
                for e in list(s):
                    lname = localname(e.tag)
                    if lname == 'XForm':
                        for ex in list(e):
                            tag = localname(ex.tag)
                            if tag == 'PinX':
                                pinx = float(ex.text or 0)
                            if tag == 'PinY':
                                piny = float(ex.text or 0)
                            if tag == 'Width':
                                width = float(ex.text or 0)
                            if tag == 'Height':
                                height = float(ex.text or 0)
                    if lname == 'Text':
                        # find cp element text
                        for tx in e.iter():
                            if localname(tx.tag) == 'cp':
                                if tx.text:
                                    text = (text + tx.text).strip()
                shapes.append({'id': sid, 'type': stype, 'name': name, 'pinx': pinx, 'piny': piny, 'width': width, 'height': height, 'text': text})
        pages.append({'id': page_id, 'name': page_name, 'shapes': shapes})
    return pages


def render_svg(page: Dict, out_path: str, scale: float = 100.0):
    shapes = page['shapes']
    if not shapes:
        # empty page
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"><text x="10" y="20">Empty page: {page.get("name")}</text></svg>'
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(svg)
        return out_path

    # determine max y to invert coordinates
    max_y = max((s['piny'] or 0) + (s['height'] or 0) / 2 for s in shapes)
    min_x = min((s['pinx'] or 0) - (s['width'] or 0) / 2 for s in shapes)
    max_x = max((s['pinx'] or 0) + (s['width'] or 0) / 2 for s in shapes)
    width_px = max(800, int((max_x - min_x) * scale + 40))
    height_px = max(600, int((max_y) * scale + 40))

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width_px}px" height="{height_px}px" viewBox="0 0 {width_px} {height_px}">']
    # defs: arrow marker for connectors
    parts.append('<defs>')
    parts.append('<marker id="arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">')
    parts.append('<path d="M0,0 L10,3.5 L0,7 z" fill="#000" />')
    parts.append('</marker>')
    parts.append('</defs>')
    # background
    parts.append(f'<rect width="100%" height="100%" fill="#ffffff"/>')

    for s in shapes:
        if s['pinx'] is None or s['piny'] is None:
            continue
        px = s['pinx']
        py = s['piny']
        w = s['width'] or 1.0
        h = s['height'] or 0.5
        x = (px - w / 2 - min_x) * scale + 20
        y = (max_y - py - h / 2) * scale + 20
        fill = '#E8F5E8'
        # treat connectors either by Type or by Name convention
        if (s['type'] and s['type'].lower().startswith('connector')) or (s.get('name','').startswith('Connector_')):
            # draw a thin line with an arrow
            # connectors in our generators are often represented as a mid-line rectangle
            # Find two nearest non-connector shapes to this connector center to approximate endpoints
            cx = px
            cy = py
            # build list of candidate shapes (centers)
            candidates = []
            for o in shapes:
                if o is s:
                    continue
                if o.get('type','').lower().startswith('connector') or o.get('name','').startswith('Connector_'):
                    continue
                if o['pinx'] is None or o['piny'] is None:
                    continue
                candidates.append(o)
            # sort by distance
            def dist(o):
                dx = (o['pinx'] or 0) - cx
                dy = (o['piny'] or 0) - cy
                return (dx*dx + dy*dy)
            candidates.sort(key=dist)
            if len(candidates) >= 2:
                a = candidates[0]
                b = candidates[1]
                x1 = (a['pinx'] - (a['width'] or 0)/2 - min_x) * scale + 20
                x2 = (b['pinx'] + (b['width'] or 0)/2 - min_x) * scale + 20
                y1 = (max_y - a['piny'] + (a['height'] or 0)/2) * scale + 20
                y2 = (max_y - b['piny'] + (b['height'] or 0)/2) * scale + 20
            else:
                x1 = (px - w / 2 - min_x) * scale + 20
                x2 = (px + w / 2 - min_x) * scale + 20
                y1 = y + h * scale / 2
                y2 = y1
            parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="2" marker-end="url(#arrow)"/>')
            if s['text']:
                parts.append(f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2 - 6}" font-family="sans-serif" font-size="12" text-anchor="middle">{escape_svg_text(s["text"])}</text>')
            continue
        # choose fill based on name
        if 'MainWindow' in s.get('name', '') or 'Window' in s.get('name', ''):
            fill = '#F3E5F5'
        if 'Parser' in s.get('name', ''):
            fill = '#FFF3E0'
        parts.append(f'<rect x="{x}" y="{y}" width="{w*scale}" height="{h*scale}" fill="{fill}" stroke="#333" stroke-width="1" rx="6"/>')
        # text: support wrapped multi-line text
        txt = s.get('text') or s.get('name') or ''
        lines = wrap_text(txt, max_chars=28)
        tx = x + 8
        ty = y + 16
        parts.append(f'<text x="{tx}" y="{ty}" font-family="sans-serif" font-size="12">')
        line_h = 14
        for i, ln in enumerate(lines):
            tsp_y = ty + i * line_h
            parts.append(f'<tspan x="{tx}" y="{tsp_y}">{escape_svg_text(ln)}</tspan>')
        parts.append('</text>')

    parts.append('</svg>')
    svg = '\n'.join(parts)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    return out_path


def escape_svg_text(t: str) -> str:
    return (t or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def wrap_text(text: str, max_chars: int = 30):
    if not text:
        return ['']
    # preserve existing newlines
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    out_lines = []
    for p in paragraphs:
        words = p.split()
        cur = ''
        for w in words:
            if len(cur) + 1 + len(w) <= max_chars:
                cur = (cur + ' ' + w).strip()
            else:
                if cur:
                    out_lines.append(cur)
                cur = w
        if cur:
            out_lines.append(cur)
    return out_lines or ['']


def export_file(path: str):
    print('Processing', path)
    xml = read_document_xml(path)
    pages = extract_pages(xml)
    out_files = []
    base = os.path.splitext(os.path.basename(path))[0]
    for p in pages:
        pid = p.get('id') or p.get('name')
        name = p.get('name')
        safe_name = ''.join(c if c.isalnum() or c in ('_', '-') else '_' for c in name)
        out = os.path.join(os.path.dirname(path), f'{base}_{safe_name}_page_{pid}.svg')
        render_svg(p, out)
        out_files.append(out)
        print('  ->', out)
    return out_files


def main(argv):
    if len(argv) < 2:
        print('Usage: export_vdx_to_svg.py <file1.vdx|.vsdx> [file2 ...]')
        return 1
    all_out = []
    for p in argv[1:]:
        if not os.path.exists(p):
            print('File not found:', p)
            continue
        outs = export_file(p)
        all_out.extend(outs)
    print('Done. Generated', len(all_out), 'SVG files.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
