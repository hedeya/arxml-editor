#!/usr/bin/env python3
"""
Generate a richer Visio (VDX) file with swimlanes, connectors and named shapes.

This produces `ARXML_Editor_Diagrams_rich.vdx` that contains:
- A Class Diagram page with connectors
- A Flowchart page with process swimlanes
- A DFD page with labeled data flows
- A Sequence page with lifelines (represented as boxes + connectors)

The file is a simple VDX-flavored XML intended for import into Visio. It's
not a complete .vsdx package but is compatible with Visio's XML import.
"""
from datetime import datetime
import os


def shape(id_, x, y, w, h, text, fill="#FFFFFF"):
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


def connector(id_, from_x, from_y, to_x, to_y, text=''):
    # Represent a connector as a connector-type shape so exporters detect it
    mid_x = (from_x + to_x) / 2
    mid_y = (from_y + to_y) / 2
    width = abs(to_x - from_x) or 0.2
    height = abs(to_y - from_y) or 0.2
    return f'''    <Shape ID="{id_}" Type="Connector" Name="Connector_{id_}">
      <XForm>
        <PinX>{mid_x}</PinX>
        <PinY>{mid_y}</PinY>
        <Width>{width}</Width>
        <Height>{height}</Height>
      </XForm>
      <Text>
        <cp IX="0">{text}</cp>
      </Text>
      <Line>
        <LineColor>#000000</LineColor>
        <LinePattern>1</LinePattern>
      </Line>
    </Shape>\n'''


def swimlane(id_, x, y, w, h, title):
    # Simple swimlane represented as a large fill with a title box
    lane = shape(id_, x, y, w, h, title, '#F5F5F5')
    # add title sub-shape
    lane += shape(id_ + 1000, x - (w/2) + 0.6, y + (h/2) - 0.3, w - 0.8, 0.5, title, '#E0E0E0')
    return lane


def write_page(f, id_, name, shapes):
    f.write(f'  <Page ID="{id_}" Name="{name}">\n')
    f.write('    <Shapes>\n')
    for s in shapes:
        f.write(s)
    f.write('    </Shapes>\n')
    f.write('  </Page>\n')


def create_rich_vdx(filename='ARXML_Editor_Diagrams_rich.vdx'):
    ts = datetime.now().isoformat()
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<VisioDocument xmlns="http://schemas.microsoft.com/office/visio/2003/core" Created="{ts}">\n')

        # Class diagram with connectors
        shapes = []
        shapes.append(shape(1, 1.5, 8.5, 2.0, 0.8, 'ARXMLEditorApp', '#E1F5FE'))
        shapes.append(shape(2, 4.0, 8.5, 2.0, 0.8, 'MainWindow', '#F3E5F5'))
        shapes.append(shape(3, 6.5, 8.5, 2.0, 0.8, 'ARXMLDocument', '#E8F5E8'))
        shapes.append(connector(100, 2.7, 8.5, 3.9, 8.5, 'controls'))
        shapes.append(connector(101, 4.9, 8.5, 6.4, 8.5, 'updates'))
        write_page(f, 1, 'Class Diagram (rich)', shapes)

        # Flowchart with swimlanes
        shapes = []
        shapes.append(swimlane(200, 3.0, 7.0, 6.0, 3.5, 'UI'))
        shapes.append(swimlane(201, 3.0, 3.0, 6.0, 3.5, 'Application'))
        shapes.append(shape(210, 3.0, 7.5, 1.6, 0.6, 'Start', '#C8E6C9'))
        shapes.append(shape(211, 3.0, 6.5, 2.6, 0.8, 'Open File', '#FFF9C4'))
        shapes.append(shape(212, 3.0, 5.5, 2.6, 0.8, 'Parse', '#FFF3E0'))
        shapes.append(connector(300, 3.0, 7.1, 3.0, 6.9, ''))
        shapes.append(connector(301, 3.0, 6.1, 3.0, 5.9, ''))
        write_page(f, 2, 'Flowchart (rich)', shapes)

        # DFD with labeled flows
        shapes = []
        shapes.append(shape(400, 1.5, 8.5, 2.0, 0.8, 'User', '#F0F4C3'))
        shapes.append(shape(401, 4.0, 8.5, 2.0, 0.8, 'MainWindow', '#F3E5F5'))
        shapes.append(shape(402, 6.5, 8.5, 2.0, 0.8, 'Parser', '#FFF3E0'))
        shapes.append(shape(403, 4.0, 6.5, 2.0, 0.8, 'ARXMLDocument', '#E8F5E8'))
        shapes.append(connector(500, 1.9, 8.5, 3.9, 8.5, 'open'))
        shapes.append(connector(501, 4.1, 8.5, 6.1, 8.5, 'parse request'))
        write_page(f, 3, 'DFD (rich)', shapes)

        # Sequence simplified as lifelines + connectors
        shapes = []
        shapes.append(shape(600, 1.5, 8.5, 1.6, 0.7, 'User', '#F0F4C3'))
        shapes.append(shape(601, 3.5, 8.5, 1.6, 0.7, 'MainWindow', '#F3E5F5'))
        shapes.append(shape(602, 5.5, 8.5, 1.6, 0.7, 'ARXMLEditorApp', '#E1F5FE'))
        shapes.append(shape(603, 7.5, 8.5, 1.6, 0.7, 'ARXMLParser', '#FFF3E0'))
        shapes.append(connector(700, 1.7, 8.5, 3.3, 8.5, 'open file'))
        shapes.append(connector(701, 3.7, 8.5, 5.3, 8.5, 'load_document'))
        shapes.append(connector(702, 5.7, 8.5, 7.3, 8.5, 'parse'))
        write_page(f, 4, 'Sequence (rich)', shapes)

        f.write('</VisioDocument>\n')

    print(f'Created {filename} ({os.path.getsize(filename)} bytes)')
    return filename


def main():
    print('Generating rich Visio VDX...')
    fn = create_rich_vdx()
    print('Done. File created:', fn)


if __name__ == '__main__':
    main()
