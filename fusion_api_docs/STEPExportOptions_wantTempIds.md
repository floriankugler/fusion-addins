# STEPExportOptions.wantTempIds Property

Parent Object: [STEPExportOptions](STEPExportOptions.md)  

## Description

Indicates if the STEP file should include the Fusion temporary IDs for faces and edges. Outside services can use these IDs with the findByTempId method of the BRepBody, which will return the given entity. The default is false.

## Syntax

"sTEPExportOptions_var" is a variable referencing a STEPExportOptions object.  

```python
# Get the value of the property.
propertyValue = sTEPExportOptions_var.wantTempIds

# Set the value of the property.
sTEPExportOptions_var.wantTempIds = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version October 2022  

