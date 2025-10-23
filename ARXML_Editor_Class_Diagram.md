# Class Diagram

```mermaid

classDiagram
    ARXMLEditorApp <|-- MainWindow
    ARXMLEditorApp --> ARXMLParser
    ARXMLParser --> ARXMLDocument
    ARXMLEditorApp --> SwComponentType

```
