# PDFExportOptions.sheetsToExport Property

Parent Object: [PDFExportOptions](PDFExportOptions.md)  

## Description

Defines which sheets to export. Defaults to AllPDFSheets which will create a single PDF file containing all sheets in the drawing.  

the SelectedPDFSheets and CurrentPDFSheet options are dependent on the current selections in the user interface.  

To set this to RangePDFSheets, use the sheetRange property to define the range of sheets to print.

## Syntax

"pDFExportOptions_var" is a variable referencing a PDFExportOptions object.  

```python
# Get the value of the property.
propertyValue = pDFExportOptions_var.sheetsToExport

# Set the value of the property.
pDFExportOptions_var.sheetsToExport = propertyValue
```

## Property Value

This is a read/write property whose value is a [PDFSheetsExport](PDFSheetsExport.md).

## Version

Introduced in version December 2020  

