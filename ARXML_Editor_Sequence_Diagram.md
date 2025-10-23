# Sequence Diagram

```mermaid

sequenceDiagram
    User->>MainWindow: Open File
    MainWindow->>ARXMLEditorApp: load_document()
    ARXMLEditorApp->>ARXMLParser: parse()
    ARXMLParser-->>ARXMLEditorApp: parsed

```
