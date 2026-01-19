# PDFExportOptions.sheetRange Property

Parent Object: [PDFExportOptions](PDFExportOptions.md)  

## Description

Defines the range of sheets to export. This can be a string like "1-3" or "1-2,5" where you can define a range of sheets and also specific sheets. Setting this property will automatically set the sheetsToExport setting to SelectedPDFSheets.

## Syntax

"pDFExportOptions_var" is a variable referencing a PDFExportOptions object.  

```python
# Get the value of the property.
propertyValue = pDFExportOptions_var.sheetRange

# Set the value of the property.
pDFExportOptions_var.sheetRange = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version December 2020  

