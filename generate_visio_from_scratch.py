#!/usr/bin/env python3
"""
Simple Visio (VDX) Diagram Generator - fresh start

This script generates a minimal Visio-compatible XML (.vdx) file containing
four pages: Class Diagram, Flowchart, Data Flow Diagram (DFD) and Sequence.

Notes:
- Produces a simple VDX XML file which many Visio versions can import.
- If you require a fully-compliant .vsdx package, I can create a zipped
  package with the required parts (more complex). For now this produces a
  single XML file that's easy to inspect and tweak.
"""
from datetime import datetime
import os


def make_shape(id_, x, y, w, h, text, fill="#FFFFFF"):
    # Minimal shape element for VDX-like XML
    return f'''    <Shape ID="{id_}" Type="Shape" Name="{text}">
      <XForm>
        <PinX>{x}</PinX>
        <PinY>{y}</PinY>
        <Width>{w}</Width>
        <Height>{h}</Height>
      </XForm>
      <Text>
        <cp IX="0">{text}</cp>
      </Text>
      <Fill>
        <FillForegnd>{fill}</FillForegnd>
      </Fill>
    </Shape>\n'''


def create_vdx(filename="ARXML_Editor_Diagrams.vdx"):
    ts = datetime.now().isoformat()
    header = f'<?xml version="1.0" encoding="UTF-8"?>\n<VisioDocument xmlns="http://schemas.microsoft.com/office/visio/2003/core" Created="{ts}">\n'

    pages = []

    # Class diagram page
    class_page = '  <Page ID="1" Name="Class Diagram">\n    <Shapes>\n'
    class_page += make_shape(1, 1.0, 8.0, 1.8, 0.8, 'ARXMLEditorApp', '#E1F5FE')
    class_page += make_shape(2, 3.0, 8.0, 1.8, 0.8, 'ARXMLDocument', '#E8F5E8')
        class_page += make_shape(3, 5.0, 8.0, 1.8, 0.8, 'ARXMLParser', '#FFF3E0')
        class_page += make_shape(4, 2.0, 6.0, 1.6, 0.7, 'SwComponentType', '#E8F5E8')
        class_page += make_shape(5, 4.0, 6.0, 1.6, 0.7, 'PortInterface', '#E8F5E8')
        # simple connectors
        class_page += f'''    <Shape ID="6" Type="Connector" Name="Connector_6">
            <XForm>
                <PinX>2.5</PinX>
                <PinY>8.0</PinY>
                <Width>2.0</Width>
                <Height>0.2</Height>
            </XForm>
            <Text>
                <cp IX="0">controls</cp>
            </Text>
            <Line>
                <LineColor>#000000</LineColor>
                <LinePattern>1</LinePattern>
            </Line>
        </Shape>\n'''
    class_page += '    </Shapes>\n  </Page>\n'
    pages.append(class_page)

    # Flowchart page
    flow_page = '  <Page ID="2" Name="Flowchart">\n    <Shapes>\n'
    flow_page += make_shape(10, 2.0, 8.0, 1.6, 0.7, 'Start', '#C8E6C9')
    flow_page += make_shape(11, 2.0, 6.5, 2.4, 0.8, 'Load Document', '#FFF9C4')
    flow_page += make_shape(12, 2.0, 5.0, 2.4, 0.8, 'Validate', '#FFCDD2')
    flow_page += make_shape(13, 2.0, 3.5, 2.0, 0.8, 'Show Results', '#BBDEFB')
    flow_page += '    </Shapes>\n  </Page>\n'
    pages.append(flow_page)

    # DFD page
    dfd_page = '  <Page ID="3" Name="DFD">\n    <Shapes>\n'
    dfd_page += make_shape(20, 1.5, 8.0, 2.0, 0.8, 'User', '#F0F4C3')
    dfd_page += make_shape(21, 4.0, 8.0, 2.0, 0.8, 'MainWindow', '#F3E5F5')
    dfd_page += make_shape(22, 4.0, 6.0, 2.0, 0.8, 'ARXMLDocument', '#E8F5E8')
    dfd_page += make_shape(23, 6.5, 6.0, 2.0, 0.8, 'Parser', '#FFF3E0')
    dfd_page += '    </Shapes>\n  </Page>\n'
    pages.append(dfd_page)

    # Sequence page
    seq_page = '  <Page ID="4" Name="Sequence">\n    <Shapes>\n'
    seq_page += make_shape(30, 1.0, 8.0, 1.6, 0.7, 'User', '#F0F4C3')
    seq_page += make_shape(31, 3.0, 8.0, 1.6, 0.7, 'MainWindow', '#F3E5F5')
    seq_page += make_shape(32, 5.0, 8.0, 1.6, 0.7, 'ARXMLEditorApp', '#E1F5FE')
    seq_page += make_shape(33, 7.0, 8.0, 1.6, 0.7, 'ARXMLParser', '#FFF3E0')
    seq_page += '    </Shapes>\n  </Page>\n'
    pages.append(seq_page)

    footer = '</VisioDocument>\n'

    content = header + ''.join(pages) + footer

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Created {filename} ({os.path.getsize(filename)} bytes)")
    return filename


def create_aux_files():
    # Also emit simple Mermaid/PlantUML artifacts for portability
    class_mermaid = """
classDiagram
    ARXMLEditorApp <|-- MainWindow
    ARXMLEditorApp --> ARXMLParser
    ARXMLParser --> ARXMLDocument
    ARXMLEditorApp --> SwComponentType
"""
    seq_mermaid = """
sequenceDiagram
    User->>MainWindow: Open File
    MainWindow->>ARXMLEditorApp: load_document()
    ARXMLEditorApp->>ARXMLParser: parse()
    ARXMLParser-->>ARXMLEditorApp: parsed
"""
    dfd_mermaid = """
graph TD
    User-->|open|MainWindow
    MainWindow-->|loads|ARXMLDocument
    ARXMLDocument-->|parsed by|ARXMLParser
"""

    with open('ARXML_Editor_Class_Diagram.md', 'w', encoding='utf-8') as f:
        f.write('# Class Diagram\n\n```mermaid\n' + class_mermaid + '\n```\n')
    with open('ARXML_Editor_Sequence_Diagram.md', 'w', encoding='utf-8') as f:
        f.write('# Sequence Diagram\n\n```mermaid\n' + seq_mermaid + '\n```\n')
    with open('ARXML_Editor_DFD_Diagram.md', 'w', encoding='utf-8') as f:
        f.write('# DFD Diagram\n\n```mermaid\n' + dfd_mermaid + '\n```\n')

    print('Created markdown/mermaid diagrams')


def main():
    print('Generating Visio (VDX) and supporting diagrams...')
    vdx = create_vdx()
    create_aux_files()
    print('Done.')


if __name__ == '__main__':
    main()
