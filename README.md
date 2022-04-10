# burp-exporter
A simple Python script to extract files from a Burp export XML (Right-Click > Save Item).

## Usage
I have found this script to be enormously helpful when exporting content from Burp for out-of-Burp analysis.

 * Right-Click on any item or folder e.g. in Site map "Save Selected Items"
 * Save the document as an XML document, e.g. `burp.xml`
 * Run this script on the XML document to save each of the files as a separate file with content.

```
python -u burp_xml_parser.py -f burp.xml
```

![Asciinema demo](burp_export.gif)

## Requirements
This simple script requires Python 3.
