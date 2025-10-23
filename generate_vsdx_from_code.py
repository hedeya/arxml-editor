#!/usr/bin/env python3
"""
Generate a minimal .vsdx package from project code.

This script will:
- Parse Python source files under `src/` to collect class names and methods
- Render a simple Visio XML (VDX-like) as `/visio/document.xml`
- Create a minimal OPC package with `[Content_Types].xml` and `_rels/.rels`
- Zip everything into `ARXML_Editor_Diagrams_from_code.vsdx`

This produces a lightweight .vsdx that Visio can usually import/open.
If Visio reports errors, I can iterate and add missing parts.
"""
import ast
import os
from datetime import datetime
import io
import zipfile


def find_python_files(root='src'):
    py_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith('.py'):
                py_files.append(os.path.join(dirpath, fn))
    return py_files


def parse_classes(py_paths, max_classes=20):
    classes = []
    for p in py_paths:
        try:
            with open(p, 'r', encoding='utf-8') as f:
                src = f.read()
            tree = ast.parse(src, p)
        except Exception:
            continue

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                methods = []
                for b in node.body:
                    if isinstance(b, ast.FunctionDef):
                        # collect signature
                        args = [a.arg for a in b.args.args]
                        doc = ast.get_docstring(b) or ''
                        methods.append({'name': b.name, 'args': args, 'doc': doc})
                cls_doc = ast.get_docstring(node) or ''
                classes.append({'name': node.name, 'methods': methods, 'file': p, 'doc': cls_doc})
                if len(classes) >= max_classes:
                    return classes
    return classes


def parse_functions(py_paths, max_funcs=100):
    funcs = []
    for p in py_paths:
        try:
            with open(p, 'r', encoding='utf-8') as f:
                src = f.read()
            tree = ast.parse(src, p)
        except Exception:
            continue

        module_name = os.path.relpath(p)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                # collect signature-like info (arg names) and docstring
                arg_names = [a.arg for a in node.args.args]
                doc = ast.get_docstring(node) or ''
                funcs.append({'name': node.name, 'args': arg_names, 'file': module_name, 'doc': doc, 'node': node})
                if len(funcs) >= max_funcs:
                    return funcs
    return funcs


def build_call_graph(py_paths, funcs):
    """Build a simple static call graph: find Call nodes and match by function name."""
    name_to_func = {f['name']: f for f in funcs}
    edges = []
    for f in funcs:
        node = f.get('node')
        if not node:
            continue
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call):
                # get function name if simple Name or Attr
                fn = None
                if isinstance(sub.func, ast.Name):
                    fn = sub.func.id
                elif isinstance(sub.func, ast.Attribute):
                    fn = sub.func.attr
                if fn and fn in name_to_func:
                    edges.append((f['name'], fn))
    return edges


def make_visio_shape(id_, x, y, w, h, title, lines, fill='#FFFFFF'):
    # Compose Text with title and methods/attrs lines
    body = title + '\n'
    for ln in lines:
        body += f'- {ln}\n'

    # Escape XML minimal
    body = body.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    return f'''    <Shape ID="{id_}" Type="Shape" Name="{title}">
      <XForm>
        <PinX>{x}</PinX>
        <PinY>{y}</PinY>
        <Width>{w}</Width>
        <Height>{h}</Height>
      </XForm>
      <Text>
        <cp IX="0">{body}</cp>
      </Text>
      <Fill>
        <FillForegnd>{fill}</FillForegnd>
      </Fill>
    </Shape>\n'''


def make_connector_shape(id_, from_x, from_y, to_x, to_y, text=''):
        mid_x = (from_x + to_x) / 2
        mid_y = (from_y + to_y) / 2
        width = max(0.2, abs(to_x - from_x))
        height = max(0.2, abs(to_y - from_y))
        # connector represented as a labeled line-shape
        txt = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return f'''    <Shape ID="{id_}" Type="Connector" Name="Connector_{id_}">
            <XForm>
                <PinX>{mid_x}</PinX>
                <PinY>{mid_y}</PinY>
                <Width>{width}</Width>
                <Height>{height}</Height>
            </XForm>
            <Text>
                <cp IX="0">{txt}</cp>
            </Text>
            <Line>
                <LineColor>#000000</LineColor>
                <LinePattern>1</LinePattern>
            </Line>
        </Shape>\n'''


def build_document_xml(classes):
    ts = datetime.now().isoformat()
    parts = []
    parts.append(f'<?xml version="1.0" encoding="UTF-8"?>\n<VisioDocument xmlns="http://schemas.microsoft.com/office/visio/2003/core" Created="{ts}">\n')

    # One page with class shapes
    parts.append('  <Page ID="1" Name="Classes from Code">\n    <Shapes>\n')
    # Grid layout for class boxes
    cols = 3
    spacing_x = 2.8
    spacing_y = 1.4
    start_x = 1.2
    start_y = 8.5
    id_counter = 1
    for idx, c in enumerate(classes):
        col = idx % cols
        row = idx // cols
        x = start_x + col * spacing_x
        y = start_y - row * spacing_y
        methods_sample = [m['name'] for m in c['methods'][:6]]
        h = 0.6 + 0.12 * len(methods_sample)
        parts.append(make_visio_shape(id_counter, x, y, 2.6, h, c['name'], methods_sample, '#E8F5E8'))
        c['layout'] = {'x': x, 'y': y}
        id_counter += 1

    parts.append('    </Shapes>\n  </Page>\n')

    # Add a sequence page (simple)
    parts.append('  <Page ID="2" Name="Document Sequence">\n    <Shapes>\n')
    parts.append('    <Shape ID="200" Type="Shape" Name="User">\n      <XForm>\n        <PinX>1.5</PinX>\n        <PinY>8.5</PinY>\n        <Width>1.6</Width>\n        <Height>0.7</Height>\n      </XForm>\n      <Text>\n        <cp IX="0">User</cp>\n      </Text>\n      <Fill>\n        <FillForegnd>#F0F4C3</FillForegnd>\n      </Fill>\n    </Shape>\n')
    parts.append('    </Shapes>\n  </Page>\n')

    # DFD page: will be filled later by main using parsed functions/modules
    parts.append('  <Page ID="3" Name="DFD">\n    <Shapes>\n')
    parts.append('    </Shapes>\n  </Page>\n')

    # Flowchart page: placeholder for function sequence mapping
    parts.append('  <Page ID="4" Name="Flowchart">\n    <Shapes>\n')
    parts.append('    </Shapes>\n  </Page>\n')

    parts.append('</VisioDocument>\n')
    return ''.join(parts)


CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Override PartName="/visio/document.xml" ContentType="application/vnd.ms-visio.drawing.main+xml"/>
    <Override PartName="/visio/pages/page1.xml" ContentType="application/vnd.ms-visio.page+xml"/>
    <Override PartName="/visio/pages/page2.xml" ContentType="application/vnd.ms-visio.page+xml"/>
    <Override PartName="/visio/pages/page3.xml" ContentType="application/vnd.ms-visio.page+xml"/>
    <Override PartName="/visio/pages/page4.xml" ContentType="application/vnd.ms-visio.page+xml"/>
    <Override PartName="/visio/masters/Basic_U.vstm" ContentType="application/vnd.ms-visio.master+xml"/>
</Types>
'''

RELS_ROOT = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/document" Target="/visio/document.xml"/>
    <Relationship Id="rIdPages" Type="http://schemas.microsoft.com/visio/2010/relationships/pages" Target="/visio/pages/"/>
    <Relationship Id="rIdMasters" Type="http://schemas.microsoft.com/visio/2010/relationships/masters" Target="/visio/masters/"/>
</Relationships>
'''


PAGE_RELS_TEMPLATE = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/pages" Target="/visio/page.xml"/>
</Relationships>
'''


def write_vsdx(out_name='ARXML_Editor_Diagrams_from_code.vsdx'):
    py_files = find_python_files('src')
    classes = parse_classes(py_files, max_classes=24)
    funcs = parse_functions(py_files, max_funcs=200)
    doc_xml = build_document_xml(classes)

    # Build call graph edges
    edges = build_call_graph(py_files, funcs)

    # Now patch the doc_xml to insert DFD and Flowchart shapes based on funcs
    # (simple approach: inject shapes into the Page ID=3 and ID=4 blocks)
    # Build simple DFD shapes grouped by module
    dfd_shapes = []
    module_map = {}
    idc = 1000
    for f in funcs[:40]:
        mod = os.path.dirname(f['file']) or '.'
        if mod not in module_map:
            module_map[mod] = []
        module_map[mod].append(f)

    mx = 1.5
    my = 8.5
    for mod, flist in module_map.items():
        title = mod if mod != '.' else 'root'
        dfd_shapes.append(make_visio_shape(idc, mx, my, 2.2, 0.6 + 0.12 * min(len(flist), 6), title, [fn['name'] for fn in flist[:6]], '#FFFDE7'))
        idc += 1
        mx += 2.6
        if mx > 9.0:
            mx = 1.5
            my -= 1.4

    flow_shapes = []
    # take first 12 functions as sequential steps
    sx = 3.0
    sy = 7.5
    step_id = 2000
    for f in funcs[:12]:
        flow_shapes.append(make_visio_shape(step_id, sx, sy, 2.4, 0.7, f['name'], [', '.join(f['args'])], '#E3F2FD'))
        step_id += 1
        sy -= 1.0

    # Inject into document XML
    # For DFD, also add connectors between modules if call edges cross modules
    conn_id = 5000
    # Map function name to module shape center
    func_to_pos = {}
    # simplistic positions for module shapes created earlier
    midx = 1.5
    midy = 8.5
    for idx, (mod, flist) in enumerate(module_map.items()):
        # find shape center by id order approximation
        func_to_pos.update({fn['name']: (midx + (idx % 6) * 2.6, midy - (idx // 6) * 1.4) for fn in flist})

    # Add call connectors as shapes on Flowchart page between function positions (if available)
    call_connectors = []
    for caller, callee in edges:
        if caller in func_to_pos and callee in func_to_pos:
            fx, fy = func_to_pos[caller]
            tx, ty = func_to_pos[callee]
            call_connectors.append(make_connector_shape(conn_id, fx, fy, tx, ty, f"{caller}->{callee}"))
            conn_id += 1

    doc_xml = doc_xml.replace('<Page ID="3" Name="DFD">\n    <Shapes>\n    </Shapes>\n  </Page>\n', '<Page ID="3" Name="DFD">\n    <Shapes>\n' + ''.join(dfd_shapes) + '    </Shapes>\n  </Page>\n')

    doc_xml = doc_xml.replace('<Page ID="4" Name="Flowchart">\n    <Shapes>\n    </Shapes>\n  </Page>\n', '<Page ID="4" Name="Flowchart">\n    <Shapes>\n' + ''.join(flow_shapes) + ''.join(call_connectors) + '    </Shapes>\n  </Page>\n')

    # Build zip package
    with zipfile.ZipFile(out_name, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        # [Content_Types].xml
        z.writestr('[Content_Types].xml', CONTENT_TYPES)
        # _rels/.rels
        z.writestr('_rels/.rels', RELS_ROOT)
        # visio/document.xml
        z.writestr('visio/document.xml', doc_xml)

        # Add per-page XML parts (simple wrappers referencing document shapes)
        # We'll create minimal page XMLs so Visio recognizes multiple pages
        for pid in range(1, 5):
            page_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<Page ID="{pid}" Name="Page {pid}"/>\n'
            z.writestr(f'visio/pages/page{pid}.xml', page_xml)

        # Add a basic master placeholder (not a real Visio master, but helps Visio)
        master_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<Master Name="Basic_U"/>\n'
        z.writestr('visio/masters/Basic_U.vstm', master_xml)

    print(f'Wrote {out_name} ({os.path.getsize(out_name)} bytes)')
    return out_name


def main():
    print('Generating .vsdx from code...')
    fn = write_vsdx()
    print('Done:', fn)


if __name__ == '__main__':
    main()
