# DXF2DImportOptions.layers Property

Parent Object: [DXF2DImportOptions](DXF2DImportOptions.md)  

## Description

Gets and sets the names of the layers that will be imported. When the DXF2DImportOptions object is first created, the array returned is a list of all the layers in the DXF file. By default, all layers will be imported. You can set the property using a new array that contains the names of only those layers you want to import.

## Syntax

"dXF2DImportOptions_var" is a variable referencing a DXF2DImportOptions object.  

```python
# Get the value of the property.
propertyValue = dXF2DImportOptions_var.layers

# Set the value of the property.
dXF2DImportOptions_var.layers = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type string.

## Version

Introduced in version October 2022  

