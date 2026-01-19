# DXF2DImportOptions.results Property

Parent Object: [DXF2DImportOptions](DXF2DImportOptions.md)  

## Description

Returns a collection of Sketch objects. A sketch is created for each layer in the DXF file that contains 2D geometry. Any 3D geometry contained in the DXF file is ignored. The names of the resulting sketches correspond to the layer names in the DXF file. Currently, the only way to get a single sketch as a result is to supply a DXF file that only has 2D geometry on a single layer.

## Syntax

"dXF2DImportOptions_var" is a variable referencing a DXF2DImportOptions object.  

```python
# Get the value of the property.
propertyValue = dXF2DImportOptions_var.results
```

## Property Value

This is a read only property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version November 2015  

