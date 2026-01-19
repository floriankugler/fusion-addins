# DXF2DImportOptions.isSingleSketchResult Property

Parent Object: [DXF2DImportOptions](DXF2DImportOptions.md)  

## Description

Gets and sets if importing the DXF file should create a new sketch for each layer or if the entire contents of the DXF file should be merged into a single layer. If true a single sketch will be created. If false a new sketch for each layer will be created where the sketch name will be the name of the layer. The default value for this property is false, resulting in a sketch for each layer.

## Syntax

"dXF2DImportOptions_var" is a variable referencing a DXF2DImportOptions object.  

```python
# Get the value of the property.
propertyValue = dXF2DImportOptions_var.isSingleSketchResult

# Set the value of the property.
dXF2DImportOptions_var.isSingleSketchResult = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version June 2020  

