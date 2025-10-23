#!/usr/bin/env python3
"""
ARXML Editor Visio Diagram Generator
Generates class, sequence, and DFD diagrams for the ARXML Editor project
"""

import os
from datetime import datetime

def create_visio_xml():
    """Create Visio-compatible XML with all three diagram types"""
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    visio_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<VisioDocument xmlns="http://schemas.microsoft.com/office/visio/2012/main" 
               xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" 
               start="0" 
               version="15.0">
  
  <DocumentProperties>
    <Title>ARXML Editor Architecture Diagrams</Title>
    <Creator>AI Assistant</Creator>
    <Description>Class, Sequence, and DFD diagrams for ARXML Editor project</Description>
    <Subject>Software Architecture</Subject>
    <Keywords>ARXML, AUTOSAR, Architecture, UML, DFD</Keywords>
    <Category>Software Design</Category>
    <TimeCreated>{timestamp}</TimeCreated>
  </DocumentProperties>

  <Pages>
    <!-- Class Diagram Page -->
    <Page ID="0" Name="Class Diagram" NameU="Class Diagram">
      <PageSheet>
        <PageProps>
          <PageWidth>11.0</PageWidth>
          <PageHeight>8.5</PageHeight>
        </PageProps>
      </PageSheet>
      
      <Shapes>
        <!-- Main Application Classes -->
        <Shape ID="1" Type="Shape" Name="ARXMLEditorApp">
          <XForm>
            <PinX>1.0</PinX>
            <PinY>7.0</PinY>
            <Width>1.5</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">ARXMLEditorApp</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#E1F5FE</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="2" Type="Shape" Name="MainWindow">
          <XForm>
            <PinX>1.0</PinX>
            <PinY>6.0</PinY>
            <Width>1.5</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">MainWindow</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#F3E5F5</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="3" Type="Shape" Name="ARXMLDocument">
          <XForm>
            <PinX>3.0</PinX>
            <PinY>7.0</PinY>
            <Width>1.5</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">ARXMLDocument</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#E8F5E8</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="4" Type="Shape" Name="ARXMLParser">
          <XForm>
            <PinX>5.0</PinX>
            <PinY>7.0</PinY>
            <Width>1.5</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">ARXMLParser</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#FFF3E0</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="5" Type="Shape" Name="ValidationService">
          <XForm>
            <PinX>7.0</PinX>
            <PinY>7.0</PinY>
            <Width>1.5</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">ValidationService</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#FFEBEE</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="6" Type="Shape" Name="SchemaService">
          <XForm>
            <PinX>9.0</PinX>
            <PinY="7.0</PinY>
            <Width>1.5</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">SchemaService</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#E0F2F1</FillForegnd>
          </Fill>
        </Shape>

        <!-- UI Components -->
        <Shape ID="7" Type="Shape" Name="TreeNavigator">
          <XForm>
            <PinX>1.0</PinX>
            <PinY>4.5</PinY>
            <Width>1.5</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">TreeNavigator</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#F3E5F5</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="8" Type="Shape" Name="PropertyEditor">
          <XForm>
            <PinX>3.0</PinX>
            <PinY>4.5</PinY>
            <Width>1.5</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">PropertyEditor</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#F3E5F5</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="9" Type="Shape" Name="ValidationList">
          <XForm>
            <PinX>5.0</PinX>
            <PinY>4.5</PinY>
            <Width>1.5</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">ValidationList</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#F3E5F5</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="10" Type="Shape" Name="DiagramView">
          <XForm>
            <PinX>7.0</PinX>
            <PinY>4.5</PinY>
            <Width>1.5</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">DiagramView</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#F3E5F5</FillForegnd>
          </Fill>
        </Shape>

        <!-- Domain Models -->
        <Shape ID="11" Type="Shape" Name="SwComponentType">
          <XForm>
            <PinX>1.0</PinX>
            <PinY>2.0</PinY>
            <Width>1.5</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">SwComponentType</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#E8F5E8</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="12" Type="Shape" Name="PortInterface">
          <XForm>
            <PinX>3.0</PinX>
            <PinY>2.0</PinY>
            <Width>1.5</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">PortInterface</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#E8F5E8</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="13" Type="Shape" Name="Composition">
          <XForm>
            <PinX>5.0</PinX>
            <PinY>2.0</PinY>
            <Width>1.5</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">Composition</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#E8F5E8</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="14" Type="Shape" Name="PortPrototype">
          <XForm>
            <PinX>7.0</PinX>
            <PinY="2.0</PinY>
            <Width>1.5</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">PortPrototype</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#E8F5E8</FillForegnd>
          </Fill>
        </Shape>

        <!-- Relationships -->
        <Shape ID="15" Type="Shape" Name="Connector">
          <XForm>
            <PinX>1.75</PinX>
            <PinY>6.4</PinY>
            <Width>0</Width>
            <Height>0.6</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0</X>
              <Y>0.6</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="16" Type="Shape" Name="Connector">
          <XForm>
            <PinX>2.25</PinX>
            <PinY>7.4</PinY>
            <Width>0.5</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0.5</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="17" Type="Shape" Name="Connector">
          <XForm>
            <PinX>3.75</PinX>
            <PinY>7.4</PinY>
            <Width>1.0</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>1.0</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="18" Type="Shape" Name="Connector">
          <XForm>
            <PinX>5.75</PinX>
            <PinY="7.4</PinY>
            <Width>1.0</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>1.0</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="19" Type="Shape" Name="Connector">
          <XForm>
            <PinX>1.75</PinX>
            <PinY>5.2</PinY>
            <Width>0</Width>
            <Height>0.6</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0</X>
              <Y>0.6</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="20" Type="Shape" Name="Connector">
          <XForm>
            <PinX>2.25</PinX>
            <PinY>4.9</PinY>
            <Width>0.5</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0.5</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="21" Type="Shape" Name="Connector">
          <XForm>
            <PinX>3.75</PinX>
            <PinY>4.9</PinY>
            <Width>0.5</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0.5</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="22" Type="Shape" Name="Connector">
          <XForm>
            <PinX>5.75</PinX>
            <PinY>4.9</PinY>
            <Width>0.5</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0.5</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="23" Type="Shape" Name="Connector">
          <XForm>
            <PinX>7.75</PinX>
            <PinY="4.9</PinY>
            <Width>0.5</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0.5</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="24" Type="Shape" Name="Connector">
          <XForm>
            <PinX>2.25</PinX>
            <PinY>6.8</PinY>
            <Width>0.5</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0.5</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="25" Type="Shape" Name="Connector">
          <XForm>
            <PinX>3.75</PinX>
            <PinY>6.8</PinY>
            <Width>0.5</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0.5</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="26" Type="Shape" Name="Connector">
          <XForm>
            <PinX>5.75</PinX>
            <PinY>6.8</PinY>
            <Width>0.5</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0.5</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="27" Type="Shape" Name="Connector">
          <XForm>
            <PinX>7.75</PinX>
            <PinY>6.8</PinY>
            <Width>0.5</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0.5</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="28" Type="Shape" Name="Connector">
          <XForm>
            <PinX>2.25</PinX>
            <PinY>4.1</PinY>
            <Width>0</Width>
            <Height>1.6</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0</X>
              <Y>1.6</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="29" Type="Shape" Name="Connector">
          <XForm>
            <PinX>3.75</PinX>
            <PinY>4.1</PinY>
            <Width>0</Width>
            <Height>1.6</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0</X>
              <Y>1.6</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="30" Type="Shape" Name="Connector">
          <XForm>
            <PinX>5.75</PinX>
            <PinY="4.1</PinY>
            <Width>0</Width>
            <Height>1.6</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0</X>
              <Y>1.6</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="31" Type="Shape" Name="Connector">
          <XForm>
            <PinX>7.75</PinX>
            <PinY="4.1</PinY>
            <Width>0</Width>
            <Height>1.6</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0</X>
              <Y>1.6</Y>
            </LineTo>
          </Geom>
        </Shape>

        <!-- Labels -->
        <Shape ID="32" Type="Shape" Name="Label">
          <XForm>
            <PinX>1.5</PinX>
            <PinY>5.8</PinY>
            <Width>0.5</Width>
            <Height>0.2</Height>
          </XForm>
          <Text>
            <cp IX="0">uses</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="33" Type="Shape" Name="Label">
          <XForm>
            <PinX>2.5</PinX>
            <PinY>7.2</PinY>
            <Width>0.5</Width>
            <Height>0.2</Height>
          </XForm>
          <Text>
            <cp IX="0">contains</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="34" Type="Shape" Name="Label">
          <XForm>
            <PinX>4.5</PinX>
            <PinY>7.2</PinY>
            <Width>0.5</Width>
            <Height>0.2</Height>
          </XForm>
          <Text>
            <cp IX="0">uses</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="35" Type="Shape" Name="Label">
          <XForm>
            <PinX>6.5</PinX>
            <PinY="7.2</PinY>
            <Width>0.5</Width>
            <Height>0.2</Height>
          </XForm>
          <Text>
            <cp IX="0">uses</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="36" Type="Shape" Name="Label">
          <XForm>
            <PinX>8.5</PinX>
            <PinY="7.2</PinY>
            <Width>0.5</Width>
            <Height>0.2</Height>
          </XForm>
          <Text>
            <cp IX="0">uses</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="37" Type="Shape" Name="Label">
          <XForm>
            <PinX>2.5</PinX>
            <PinY>4.7</PinY>
            <Width>0.5</Width>
            <Height>0.2</Height>
          </XForm>
          <Text>
            <cp IX="0">contains</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="38" Type="Shape" Name="Label">
          <XForm>
            <PinX>4.5</PinX>
            <PinY="4.7</PinY>
            <Width>0.5</Width>
            <Height>0.2</Height>
          </XForm>
          <Text>
            <cp IX="0">contains</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="39" Type="Shape" Name="Label">
          <XForm>
            <PinX>6.5</PinX>
            <PinY="4.7</PinY>
            <Width>0.5</Width>
            <Height>0.2</Height>
          </XForm>
          <Text>
            <cp IX="0">contains</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="40" Type="Shape" Name="Label">
          <XForm>
            <PinX>8.5</PinX>
            <PinY="4.7</PinY>
            <Width>0.5</Width>
            <Height>0.2</Height>
          </XForm>
          <Text>
            <cp IX="0">contains</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="41" Type="Shape" Name="Label">
          <XForm>
            <PinX>2.5</PinX>
            <PinY>3.2</PinY>
            <Width>0.5</Width>
            <Height>0.2</Height>
          </XForm>
          <Text>
            <cp IX="0">manages</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="42" Type="Shape" Name="Label">
          <XForm>
            <PinX>4.5</PinX>
            <PinY="3.2</PinY>
            <Width>0.5</Width>
            <Height>0.2</Height>
          </XForm>
          <Text>
            <cp IX="0">manages</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="43" Type="Shape" Name="Label">
          <XForm>
            <PinX>6.5</PinX>
            <PinY="3.2</PinY>
            <Width>0.5</Width>
            <Height>0.2</Height>
          </XForm>
          <Text>
            <cp IX="0">manages</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="44" Type="Shape" Name="Label">
          <XForm>
            <PinX>8.5</PinX>
            <PinY="3.2</PinY>
            <Width>0.5</Width>
            <Height>0.2</Height>
          </XForm>
          <Text>
            <cp IX="0">manages</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <!-- Title -->
        <Shape ID="45" Type="Shape" Name="Title">
          <XForm>
            <PinX>5.0</PinX>
            <PinY>8.2</PinY>
            <Width>2.0</Width>
            <Height>0.3</Height>
          </XForm>
          <Text>
            <cp IX="0">ARXML Editor - Class Diagram</cp>
            <pp IX="0" HorzAlign="1" Size="14"/>
          </Text>
        </Shape>
      </Shapes>
    </Page>

    <!-- Sequence Diagram Page -->
    <Page ID="1" Name="Sequence Diagram" NameU="Sequence Diagram">
      <PageSheet>
        <PageProps>
          <PageWidth>11.0</PageWidth>
          <PageHeight>8.5</PageHeight>
        </PageProps>
      </PageSheet>
      
      <Shapes>
        <!-- Actors and Objects -->
        <Shape ID="50" Type="Shape" Name="User">
          <XForm>
            <PinX>0.5</PinX>
            <PinY>1.0</PinY>
            <Width>0.8</Width>
            <Height>0.6</Height>
          </XForm>
          <Text>
            <cp IX="0">User</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#FFCDD2</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="51" Type="Shape" Name="MainWindow">
          <XForm>
            <PinX>2.0</PinX>
            <PinY>1.0</PinY>
            <Width>0.8</Width>
            <Height>0.6</Height>
          </XForm>
          <Text>
            <cp IX="0">MainWindow</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#E1F5FE</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="52" Type="Shape" Name="ARXMLEditorApp">
          <XForm>
            <PinX>3.5</PinX>
            <PinY>1.0</PinY>
            <Width>0.8</Width>
            <Height>0.6</Height>
          </XForm>
          <Text>
            <cp IX="0">ARXMLEditorApp</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#E8F5E8</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="53" Type="Shape" Name="ARXMLParser">
          <XForm>
            <PinX>5.0</PinX>
            <PinY>1.0</PinY>
            <Width>0.8</Width>
            <Height>0.6</Height>
          </XForm>
          <Text>
            <cp IX="0">ARXMLParser</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#FFF3E0</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="54" Type="Shape" Name="SchemaService">
          <XForm>
            <PinX>6.5</PinX>
            <PinY>1.0</PinY>
            <Width>0.8</Width>
            <Height>0.6</Height>
          </XForm>
          <Text>
            <cp IX="0">SchemaService</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#E0F2F1</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="55" Type="Shape" Name="ARXMLDocument">
          <XForm>
            <PinX>8.0</PinX>
            <PinY>1.0</PinY>
            <Width>0.8</Width>
            <Height>0.6</Height>
          </XForm>
          <Text>
            <cp IX="0">ARXMLDocument</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#F3E5F5</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="56" Type="Shape" Name="ValidationService">
          <XForm>
            <PinX>9.5</PinX>
            <PinY>1.0</PinY>
            <Width>0.8</Width>
            <Height>0.6</Height>
          </XForm>
          <Text>
            <cp IX="0">ValidationService</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#FFEBEE</FillForegnd>
          </Fill>
        </Shape>

        <!-- Lifelines -->
        <Shape ID="57" Type="Shape" Name="Lifeline">
          <XForm>
            <PinX>0.9</PinX>
            <PinY>1.6</PinY>
            <Width>0</Width>
            <Height>6.0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0</X>
              <Y>6.0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="58" Type="Shape" Name="Lifeline">
          <XForm>
            <PinX>2.4</PinX>
            <PinY>1.6</PinY>
            <Width>0</Width>
            <Height>6.0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0</X>
              <Y>6.0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="59" Type="Shape" Name="Lifeline">
          <XForm>
            <PinX>3.9</PinX>
            <PinY>1.6</PinY>
            <Width>0</Width>
            <Height>6.0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0</X>
              <Y>6.0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="60" Type="Shape" Name="Lifeline">
          <XForm>
            <PinX>5.4</PinX>
            <PinY>1.6</PinY>
            <Width>0</Width>
            <Height>6.0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0</X>
              <Y>6.0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="61" Type="Shape" Name="Lifeline">
          <XForm>
            <PinX>6.9</PinX>
            <PinY>1.6</PinY>
            <Width>0</Width>
            <Height>6.0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0</X>
              <Y>6.0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="62" Type="Shape" Name="Lifeline">
          <XForm>
            <PinX>8.4</PinX>
            <PinY>1.6</PinY>
            <Width>0</Width>
            <Height>6.0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0</X>
              <Y>6.0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <Shape ID="63" Type="Shape" Name="Lifeline">
          <XForm>
            <PinX>9.9</PinX>
            <PinY>1.6</PinY>
            <Width>0</Width>
            <Height>6.0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0</X>
              <Y>6.0</Y>
            </LineTo>
          </Geom>
        </Shape>

        <!-- Messages -->
        <Shape ID="64" Type="Shape" Name="Message">
          <XForm>
            <PinX>0.9</PinX>
            <PinY>2.0</PinY>
            <Width>1.5</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>1.5</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">1. Select "Open File"</cp>
            <pp IX="0" HorzAlign="0"/>
          </Text>
        </Shape>

        <Shape ID="65" Type="Shape" Name="Message">
          <XForm>
            <PinX>2.4</PinX>
            <PinY>2.3</PinY>
            <Width>1.1</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>1.1</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">2. load_document(file_path)</cp>
            <pp IX="0" HorzAlign="0"/>
          </Text>
        </Shape>

        <Shape ID="66" Type="Shape" Name="Message">
          <XForm>
            <PinX>3.9</PinX>
            <PinY>2.6</PinY>
            <Width>1.1</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>1.1</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">3. parse_arxml_file(file_path)</cp>
            <pp IX="0" HorzAlign="0"/>
          </Text>
        </Shape>

        <Shape ID="67" Type="Shape" Name="Message">
          <XForm>
            <PinX>5.4</PinX>
            <PinY>2.9</PinY>
            <Width>1.1</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>1.1</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">4. detect_schema_version()</cp>
            <pp IX="0" HorzAlign="0"/>
          </Text>
        </Shape>

        <Shape ID="68" Type="Shape" Name="Message">
          <XForm>
            <PinX>5.4</PinX>
            <PinY>3.2</PinY>
            <Width>1.1</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>1.1</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">5. load_from_element(root)</cp>
            <pp IX="0" HorzAlign="0"/>
          </Text>
        </Shape>

        <Shape ID="69" Type="Shape" Name="Message">
          <XForm>
            <PinX>3.9</PinX>
            <PinY>3.5</PinY>
            <Width>1.1</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>1.1</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">6. validate_document(document)</cp>
            <pp IX="0" HorzAlign="0"/>
          </Text>
        </Shape>

        <Shape ID="70" Type="Shape" Name="Message">
          <XForm>
            <PinX>8.4</PinX>
            <PinY>3.8</PinY>
            <Width>1.1</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>1.1</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">7. validate_elements()</cp>
            <pp IX="0" HorzAlign="0"/>
          </Text>
        </Shape>

        <Shape ID="71" Type="Shape" Name="Message">
          <XForm>
            <PinX>3.9</PinX>
            <PinY>4.1</PinY>
            <Width>1.1</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>1.1</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">8. document_changed signal</cp>
            <pp IX="0" HorzAlign="0"/>
          </Text>
        </Shape>

        <Shape ID="72" Type="Shape" Name="Message">
          <XForm>
            <PinX>2.4</PinX>
            <PinY>4.4</PinY>
            <Width>1.1</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>1.1</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">9. update_tree()</cp>
            <pp IX="0" HorzAlign="0"/>
          </Text>
        </Shape>

        <Shape ID="73" Type="Shape" Name="Message">
          <XForm>
            <PinX>2.4</PinX>
            <PinY>4.7</PinY>
            <Width>1.1</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>1.1</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">10. update_properties()</cp>
            <pp IX="0" HorzAlign="0"/>
          </Text>
        </Shape>

        <!-- Title -->
        <Shape ID="74" Type="Shape" Name="Title">
          <XForm>
            <PinX>5.0</PinX>
            <PinY>7.8</PinY>
            <Width>2.0</Width>
            <Height>0.3</Height>
          </XForm>
          <Text>
            <cp IX="0">ARXML Editor - Document Loading Sequence</cp>
            <pp IX="0" HorzAlign="1" Size="14"/>
          </Text>
        </Shape>
      </Shapes>
    </Page>

    <!-- Data Flow Diagram Page -->
    <Page ID="2" Name="Data Flow Diagram" NameU="Data Flow Diagram">
      <PageSheet>
        <PageProps>
          <PageWidth>11.0</PageWidth>
          <PageHeight>8.5</PageHeight>
        </PageProps>
      </PageSheet>
      
      <Shapes>
        <!-- External Entities -->
        <Shape ID="100" Type="Shape" Name="User">
          <XForm>
            <PinX>0.5</PinX>
            <PinY>6.0</PinY>
            <Width>1.0</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">User</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#FFCDD2</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="101" Type="Shape" Name="ARXMLFile">
          <XForm>
            <PinX>9.5</PinX>
            <PinY>6.0</PinY>
            <Width>1.0</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">ARXML File</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#FFCDD2</FillForegnd>
          </Fill>
        </Shape>

        <!-- Processes -->
        <Shape ID="102" Type="Shape" Name="FileLoadProcess">
          <XForm>
            <PinX>2.5</PinX>
            <PinY>6.0</PinY>
            <Width>1.2</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">1.0 Load File</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#E1F5FE</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="103" Type="Shape" Name="ParseProcess">
          <XForm>
            <PinX>4.5</PinX>
            <PinY>6.0</PinY>
            <Width>1.2</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">2.0 Parse ARXML</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#E8F5E8</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="104" Type="Shape" Name="ValidateProcess">
          <XForm>
            <PinX>6.5</PinX>
            <PinY>6.0</PinY>
            <Width>1.2</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">3.0 Validate</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#FFF3E0</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="105" Type="Shape" Name="DisplayProcess">
          <XForm>
            <PinX>2.5</PinX>
            <PinY>4.0</PinY>
            <Width>1.2</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">4.0 Display UI</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#F3E5F5</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="106" Type="Shape" Name="EditProcess">
          <XForm>
            <PinX>4.5</PinX>
            <PinY>4.0</PinY>
            <Width>1.2</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">5.0 Edit Elements</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#E0F2F1</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="107" Type="Shape" Name="SaveProcess">
          <XForm>
            <PinX>6.5</PinX>
            <PinY>4.0</PinY>
            <Width>1.2</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">6.0 Save Changes</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#FFEBEE</FillForegnd>
          </Fill>
        </Shape>

        <!-- Data Stores -->
        <Shape ID="108" Type="Shape" Name="DocumentStore">
          <XForm>
            <PinX>8.0</PinX>
            <PinY>3.0</PinY>
            <Width>1.0</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">D1 Document Model</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#E8F5E8</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="109" Type="Shape" Name="ValidationStore">
          <XForm>
            <PinX>8.0</PinX>
            <PinY>4.5</PinY>
            <Width>1.0</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">D2 Validation Rules</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#E8F5E8</FillForegnd>
          </Fill>
        </Shape>

        <Shape ID="110" Type="Shape" Name="SchemaStore">
          <XForm>
            <PinX>8.0</PinX>
            <PinY>6.0</PinY>
            <Width>1.0</Width>
            <Height>0.8</Height>
          </XForm>
          <Text>
            <cp IX="0">D3 Schema Definitions</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
          <Fill>
            <FillForegnd>#E8F5E8</FillForegnd>
          </Fill>
        </Shape>

        <!-- Data Flows -->
        <Shape ID="111" Type="Shape" Name="DataFlow">
          <XForm>
            <PinX>1.5</PinX>
            <PinY>6.4</PinY>
            <Width>1.0</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>1.0</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">File Path</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="112" Type="Shape" Name="DataFlow">
          <XForm>
            <PinX>3.7</PinX>
            <PinY>6.4</PinY>
            <Width>0.8</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0.8</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">ARXML Content</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="113" Type="Shape" Name="DataFlow">
          <XForm>
            <PinX>5.7</PinX>
            <PinY="6.4</PinY>
            <Width>0.8</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0.8</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">Parsed Data</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="114" Type="Shape" Name="DataFlow">
          <XForm>
            <PinX>7.7</PinX>
            <PinY>6.4</PinY>
            <Width>0.8</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0.8</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">Validated Data</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="115" Type="Shape" Name="DataFlow">
          <XForm>
            <PinX>2.5</PinX>
            <PinY>5.6</PinY>
            <Width>0</Width>
            <Height>1.2</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0</X>
              <Y>1.2</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">Display Data</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="116" Type="Shape" Name="DataFlow">
          <XForm>
            <PinX>4.5</PinX>
            <PinY>4.8</PinY>
            <Width>0</Width>
            <Height>0.8</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0</X>
              <Y>0.8</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">User Input</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="117" Type="Shape" Name="DataFlow">
          <XForm>
            <PinX>6.5</PinX>
            <PinY>4.8</PinY>
            <Width>0</Width>
            <Height>0.8</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0</X>
              <Y>0.8</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">Modified Data</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="118" Type="Shape" Name="DataFlow">
          <XForm>
            <PinX>7.7</PinX>
            <PinY>4.4</PinY>
            <Width>0.8</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>0.8</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">ARXML Output</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="119" Type="Shape" Name="DataFlow">
          <XForm>
            <PinX>6.5</PinX>
            <PinY>5.2</PinY>
            <Width>1.0</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>1.0</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">Schema Info</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="120" Type="Shape" Name="DataFlow">
          <XForm>
            <PinX>6.5</PinX>
            <PinY>5.6</PinY>
            <Width>1.0</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>1.0</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">Validation Rules</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <Shape ID="121" Type="Shape" Name="DataFlow">
          <XForm>
            <PinX>6.5</PinX>
            <PinY>6.4</PinY>
            <Width>1.0</Width>
            <Height>0</Height>
          </XForm>
          <Geom IX="0">
            <MoveTo IX="0">
              <X>0</X>
              <Y>0</Y>
            </MoveTo>
            <LineTo IX="1">
              <X>1.0</X>
              <Y>0</Y>
            </LineTo>
          </Geom>
          <Text>
            <cp IX="0">Document Data</cp>
            <pp IX="0" HorzAlign="1"/>
          </Text>
        </Shape>

        <!-- Title -->
        <Shape ID="122" Type="Shape" Name="Title">
          <XForm>
            <PinX>5.0</PinX>
            <PinY>7.8</PinY>
            <Width>2.0</Width>
            <Height>0.3</Height>
          </XForm>
          <Text>
            <cp IX="0">ARXML Editor - Data Flow Diagram</cp>
            <pp IX="0" HorzAlign="1" Size="14"/>
          </Text>
        </Shape>
      </Shapes>
    </Page>
  </Pages>
</VisioDocument>'''
    
    return visio_xml

def create_mermaid_diagrams():
    """Create Mermaid diagrams that can be converted to Visio"""
    
    class_diagram = '''
classDiagram
    class ARXMLEditorApp {
        -current_document: ARXMLDocument
        -validation_service: ValidationService
        -command_service: CommandService
        -schema_service: SchemaService
        -arxml_parser: ARXMLParser
        +load_document(file_path: str): bool
        +save_document(file_path: str): bool
        +new_document(): ARXMLDocument
    }
    
    class MainWindow {
        -app: ARXMLEditorApp
        -tree_navigator: TreeNavigator
        -property_editor: PropertyEditor
        -validation_list: ValidationList
        -diagram_view: DiagramView
        +_setup_ui()
        +_connect_signals()
    }
    
    class ARXMLDocument {
        -sw_component_types: List[SwComponentType]
        -compositions: List[Composition]
        -port_interfaces: List[PortInterface]
        -service_interfaces: List[ServiceInterface]
        -ecuc_elements: List[dict]
        +add_sw_component_type(component: SwComponentType)
        +add_port_interface(interface: PortInterface)
        +save_document(file_path: str): bool
    }
    
    class ARXMLParser {
        -namespaces: Dict[str, str]
        -schema_service: SchemaService
        +parse_arxml_file(file_path: str): Element
        +extract_sw_component_types(root: Element): List[SwComponentType]
        +extract_port_interfaces(root: Element): List[PortInterface]
        +serialize_to_arxml(document: ARXMLDocument): str
    }
    
    class ValidationService {
        -issues: List[ValidationIssue]
        -schema_service: SchemaService
        +validate_document(document: ARXMLDocument): List[ValidationIssue]
        +validate_element(element: Any): List[ValidationIssue]
    }
    
    class SchemaService {
        -current_version: str
        -current_schema: XMLSchema
        -available_versions: List[SchemaVersion]
        +detect_schema_version_from_file(file_path: str): str
        +validate_arxml_file(file_path: str): List[str]
        +set_version(version: str): bool
    }
    
    class TreeNavigator {
        -app: ARXMLEditorApp
        +refresh()
        +_add_component_type_item(component: SwComponentType)
        +_add_port_interface_item(interface: PortInterface)
    }
    
    class PropertyEditor {
        -app: ARXMLEditorApp
        -current_element: Any
        +set_element(element: Any)
        +_create_sw_component_type_properties(component: SwComponentType)
        +_create_port_interface_properties(interface: PortInterface)
    }
    
    class SwComponentType {
        +short_name: str
        +category: SwComponentTypeCategory
        +ports: List[PortPrototype]
        +add_port(port: PortPrototype)
        +validate_invariants(): List[str]
    }
    
    class PortInterface {
        +short_name: str
        +is_service: bool
        +data_elements: List[DataElement]
        +add_data_element(element: DataElement)
        +validate_invariants(): List[str]
    }
    
    class Composition {
        +short_name: str
        +component_types: List[SwComponentType]
        +connections: List[PortConnection]
        +add_component_type(component: SwComponentType)
    }
    
    class PortPrototype {
        +short_name: str
        +port_type: PortType
        +interface_ref: str
        +connect_to(other_port: PortPrototype): bool
    }
    
    ARXMLEditorApp --> MainWindow : uses
    ARXMLEditorApp --> ARXMLDocument : contains
    ARXMLEditorApp --> ARXMLParser : uses
    ARXMLEditorApp --> ValidationService : uses
    ARXMLEditorApp --> SchemaService : uses
    MainWindow --> TreeNavigator : contains
    MainWindow --> PropertyEditor : contains
    MainWindow --> ValidationList : contains
    MainWindow --> DiagramView : contains
    ARXMLDocument --> SwComponentType : manages
    ARXMLDocument --> PortInterface : manages
    ARXMLDocument --> Composition : manages
    ARXMLDocument --> PortPrototype : manages
    '''
    
    sequence_diagram = '''
sequenceDiagram
    participant User
    participant MainWindow
    participant ARXMLEditorApp
    participant ARXMLParser
    participant SchemaService
    participant ARXMLDocument
    participant ValidationService
    participant TreeNavigator
    participant PropertyEditor
    
    User->>MainWindow: Select "Open File"
    MainWindow->>ARXMLEditorApp: load_document(file_path)
    ARXMLEditorApp->>ARXMLParser: parse_arxml_file(file_path)
    ARXMLParser->>SchemaService: detect_schema_version()
    SchemaService-->>ARXMLParser: schema_version
    ARXMLParser->>ARXMLDocument: load_from_element(root)
    ARXMLDocument-->>ARXMLParser: document_loaded
    ARXMLParser-->>ARXMLEditorApp: parsed_document
    ARXMLEditorApp->>ValidationService: validate_document(document)
    ValidationService->>ARXMLDocument: validate_elements()
    ARXMLDocument-->>ValidationService: validation_results
    ValidationService-->>ARXMLEditorApp: validation_complete
    ARXMLEditorApp->>MainWindow: document_changed signal
    MainWindow->>TreeNavigator: update_tree()
    MainWindow->>PropertyEditor: update_properties()
    TreeNavigator-->>User: Display tree structure
    PropertyEditor-->>User: Display properties panel
    '''
    
    dfd_diagram = '''
flowchart TD
    User[User] -->|File Path| LoadFile[1.0 Load File]
    LoadFile -->|ARXML Content| ParseARXML[2.0 Parse ARXML]
    ParseARXML -->|Parsed Data| Validate[3.0 Validate]
    Validate -->|Validated Data| DocumentModel[(D1 Document Model)]
    DocumentModel -->|Display Data| DisplayUI[4.0 Display UI]
    DisplayUI -->|User Input| EditElements[5.0 Edit Elements]
    EditElements -->|Modified Data| SaveChanges[6.0 Save Changes]
    SaveChanges -->|ARXML Output| ARXMLFile[ARXML File]
    
    SchemaDefs[(D3 Schema Definitions)] -->|Schema Info| ParseARXML
    ValidationRules[(D2 Validation Rules)] -->|Validation Rules| Validate
    DocumentModel -->|Document Data| Validate
    
    classDef process fill:#E1F5FE,stroke:#01579B,stroke-width:2px
    classDef datastore fill:#E8F5E8,stroke:#2E7D32,stroke-width:2px
    classDef external fill:#FFCDD2,stroke:#C62828,stroke-width:2px
    
    class LoadFile,ParseARXML,Validate,DisplayUI,EditElements,SaveChanges process
    class DocumentModel,SchemaDefs,ValidationRules datastore
    class User,ARXMLFile external
    '''
    
    return class_diagram, sequence_diagram, dfd_diagram

def create_plantuml_diagrams():
    """Create PlantUML diagrams that can be converted to Visio"""
    
    class_diagram = '''
@startuml ARXML_Editor_Class_Diagram
!theme plain

package "UI Layer" {
    class MainWindow {
        -app: ARXMLEditorApp
        -tree_navigator: TreeNavigator
        -property_editor: PropertyEditor
        -validation_list: ValidationList
        -diagram_view: DiagramView
        +_setup_ui()
        +_connect_signals()
    }
    
    class TreeNavigator {
        -app: ARXMLEditorApp
        +refresh()
        +_add_component_type_item(component: SwComponentType)
    }
    
    class PropertyEditor {
        -app: ARXMLEditorApp
        -current_element: Any
        +set_element(element: Any)
        +_create_sw_component_type_properties(component: SwComponentType)
    }
    
    class ValidationList {
        -app: ARXMLEditorApp
        +update_validation_results()
    }
    
    class DiagramView {
        -app: ARXMLEditorApp
        +update_diagram()
    }
}

package "Application Layer" {
    class ARXMLEditorApp {
        -current_document: ARXMLDocument
        -validation_service: ValidationService
        -command_service: CommandService
        -schema_service: SchemaService
        -arxml_parser: ARXMLParser
        +load_document(file_path: str): bool
        +save_document(file_path: str): bool
        +new_document(): ARXMLDocument
    }
}

package "Domain Layer" {
    class ARXMLDocument {
        -sw_component_types: List[SwComponentType]
        -compositions: List[Composition]
        -port_interfaces: List[PortInterface]
        -service_interfaces: List[ServiceInterface]
        -ecuc_elements: List[dict]
        +add_sw_component_type(component: SwComponentType)
        +add_port_interface(interface: PortInterface)
        +save_document(file_path: str): bool
    }
    
    class SwComponentType {
        +short_name: str
        +category: SwComponentTypeCategory
        +ports: List[PortPrototype]
        +add_port(port: PortPrototype)
        +validate_invariants(): List[str]
    }
    
    class PortInterface {
        +short_name: str
        +is_service: bool
        +data_elements: List[DataElement]
        +add_data_element(element: DataElement)
        +validate_invariants(): List[str]
    }
    
    class Composition {
        +short_name: str
        +component_types: List[SwComponentType]
        +connections: List[PortConnection]
        +add_component_type(component: SwComponentType)
    }
    
    class PortPrototype {
        +short_name: str
        +port_type: PortType
        +interface_ref: str
        +connect_to(other_port: PortPrototype): bool
    }
}

package "Infrastructure Layer" {
    class ARXMLParser {
        -namespaces: Dict[str, str]
        -schema_service: SchemaService
        +parse_arxml_file(file_path: str): Element
        +extract_sw_component_types(root: Element): List[SwComponentType]
        +serialize_to_arxml(document: ARXMLDocument): str
    }
    
    class ValidationService {
        -issues: List[ValidationIssue]
        -schema_service: SchemaService
        +validate_document(document: ARXMLDocument): List[ValidationIssue]
        +validate_element(element: Any): List[ValidationIssue]
    }
    
    class SchemaService {
        -current_version: str
        -current_schema: XMLSchema
        -available_versions: List[SchemaVersion]
        +detect_schema_version_from_file(file_path: str): str
        +validate_arxml_file(file_path: str): List[str]
        +set_version(version: str): bool
    }
}

' Relationships
ARXMLEditorApp --> MainWindow : uses
ARXMLEditorApp --> ARXMLDocument : contains
ARXMLEditorApp --> ARXMLParser : uses
ARXMLEditorApp --> ValidationService : uses
ARXMLEditorApp --> SchemaService : uses
MainWindow --> TreeNavigator : contains
MainWindow --> PropertyEditor : contains
MainWindow --> ValidationList : contains
MainWindow --> DiagramView : contains
ARXMLDocument --> SwComponentType : manages
ARXMLDocument --> PortInterface : manages
ARXMLDocument --> Composition : manages
ARXMLDocument --> PortPrototype : manages

@enduml
    '''
    
    sequence_diagram = '''
@startuml ARXML_Editor_Sequence_Diagram
!theme plain

actor User
participant "MainWindow" as MW
participant "ARXMLEditorApp" as App
participant "ARXMLParser" as Parser
participant "SchemaService" as Schema
participant "ARXMLDocument" as Doc
participant "ValidationService" as Validation
participant "TreeNavigator" as Tree
participant "PropertyEditor" as Props

User -> MW: Select "Open File"
MW -> App: load_document(file_path)
App -> Parser: parse_arxml_file(file_path)
Parser -> Schema: detect_schema_version()
Schema --> Parser: schema_version
Parser -> Doc: load_from_element(root)
Doc --> Parser: document_loaded
Parser --> App: parsed_document
App -> Validation: validate_document(document)
Validation -> Doc: validate_elements()
Doc --> Validation: validation_results
Validation --> App: validation_complete
App -> MW: document_changed signal
MW -> Tree: update_tree()
MW -> Props: update_properties()
Tree --> User: Display tree structure
Props --> User: Display properties panel

@enduml
    '''
    
    return class_diagram, sequence_diagram

def main():
    """Generate all diagram formats"""
    print("Generating ARXML Editor Architecture Diagrams...")
    
    # Create Visio XML
    visio_xml = create_visio_xml()
    with open("ARXML_Editor_Diagrams.vsdx", "w", encoding="utf-8") as f:
        f.write(visio_xml)
    print("✓ Created ARXML_Editor_Diagrams.vsdx")
    
    # Create Mermaid diagrams
    class_diagram, sequence_diagram, dfd_diagram = create_mermaid_diagrams()
    
    with open("ARXML_Editor_Class_Diagram.md", "w", encoding="utf-8") as f:
        f.write("# ARXML Editor - Class Diagram\n\n```mermaid\n" + class_diagram + "\n```")
    print("✓ Created ARXML_Editor_Class_Diagram.md")
    
    with open("ARXML_Editor_Sequence_Diagram.md", "w", encoding="utf-8") as f:
        f.write("# ARXML Editor - Sequence Diagram\n\n```mermaid\n" + sequence_diagram + "\n```")
    print("✓ Created ARXML_Editor_Sequence_Diagram.md")
    
    with open("ARXML_Editor_DFD_Diagram.md", "w", encoding="utf-8") as f:
        f.write("# ARXML Editor - Data Flow Diagram\n\n```mermaid\n" + dfd_diagram + "\n```")
    print("✓ Created ARXML_Editor_DFD_Diagram.md")
    
    # Create PlantUML diagrams
    class_puml, sequence_puml = create_plantuml_diagrams()
    
    with open("ARXML_Editor_Class_Diagram.puml", "w", encoding="utf-8") as f:
        f.write(class_puml)
    print("✓ Created ARXML_Editor_Class_Diagram.puml")
    
    with open("ARXML_Editor_Sequence_Diagram.puml", "w", encoding="utf-8") as f:
        f.write(sequence_puml)
    print("✓ Created ARXML_Editor_Sequence_Diagram.puml")
    
    # Create comprehensive documentation
    with open("ARXML_Editor_Architecture_Diagrams.md", "w", encoding="utf-8") as f:
        f.write(f"""# ARXML Editor Architecture Diagrams

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Overview

This document contains the complete architecture diagrams for the ARXML Editor project, including:

1. **Class Diagram** - Shows the object-oriented structure and relationships
2. **Sequence Diagram** - Illustrates the document loading workflow
3. **Data Flow Diagram (DFD)** - Maps data flow through the system

## Class Diagram

The class diagram shows the layered architecture of the ARXML Editor:

- **UI Layer**: MainWindow, TreeNavigator, PropertyEditor, ValidationList, DiagramView
- **Application Layer**: ARXMLEditorApp (main controller)
- **Domain Layer**: ARXMLDocument and AUTOSAR element models
- **Infrastructure Layer**: ARXMLParser, ValidationService, SchemaService

### Key Relationships:
- ARXMLEditorApp orchestrates all components
- MainWindow contains all UI components
- ARXMLDocument manages AUTOSAR element collections
- Services provide specialized functionality

## Sequence Diagram

The sequence diagram illustrates the document loading workflow:

1. User selects "Open File"
2. MainWindow calls ARXMLEditorApp.load_document()
3. ARXMLParser parses the file with schema detection
4. ARXMLDocument loads the parsed content
5. ValidationService validates the document
6. UI components are updated with the loaded data

## Data Flow Diagram

The DFD shows how data flows through the system:

- **External Entities**: User, ARXML File
- **Processes**: Load File, Parse ARXML, Validate, Display UI, Edit Elements, Save Changes
- **Data Stores**: Document Model, Validation Rules, Schema Definitions

### Data Flows:
- File Path → Load File
- ARXML Content → Parse ARXML
- Parsed Data → Validate
- Validated Data → Document Model
- Display Data → Display UI
- User Input → Edit Elements
- Modified Data → Save Changes
- ARXML Output → ARXML File

## Files Generated

1. `ARXML_Editor_Diagrams.vsdx` - Visio-compatible XML file
2. `ARXML_Editor_Class_Diagram.md` - Mermaid class diagram
3. `ARXML_Editor_Sequence_Diagram.md` - Mermaid sequence diagram
4. `ARXML_Editor_DFD_Diagram.md` - Mermaid data flow diagram
5. `ARXML_Editor_Class_Diagram.puml` - PlantUML class diagram
6. `ARXML_Editor_Sequence_Diagram.puml` - PlantUML sequence diagram

## Usage

- **Visio**: Open the .vsdx file in Microsoft Visio
- **Mermaid**: View the .md files in any Markdown viewer that supports Mermaid
- **PlantUML**: Use PlantUML tools to generate images from .puml files
- **Online**: Copy Mermaid code to https://mermaid.live/ for interactive viewing

## Architecture Notes

The ARXML Editor follows a clean architecture pattern with clear separation of concerns:

- **Dependency Injection**: Services are injected via DIContainer
- **Event-Driven**: Uses Qt signals and domain events for loose coupling
- **Repository Pattern**: Data access is abstracted through repositories
- **Command Pattern**: User actions are encapsulated as commands
- **Observer Pattern**: UI components observe model changes

This architecture ensures maintainability, testability, and extensibility.
""")
    print("✓ Created ARXML_Editor_Architecture_Diagrams.md")
    
    print("\n🎉 All diagrams generated successfully!")
    print("\nTo view the diagrams:")
    print("1. Open ARXML_Editor_Diagrams.vsdx in Microsoft Visio")
    print("2. View the .md files in any Markdown viewer with Mermaid support")
    print("3. Use PlantUML tools to generate images from .puml files")
    print("4. Visit https://mermaid.live/ to view Mermaid diagrams online")

if __name__ == "__main__":
    main()