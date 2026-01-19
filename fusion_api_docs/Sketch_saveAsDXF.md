# Sketch.saveAsDXF Method

Parent Object: [Sketch](Sketch.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Saves the contents of the sketch to a specified DXF file.

## Remarks

This method has been replaced by using the ExportManager.createDXFSketchExportOptions method, which provides additional capabilities.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.saveAsDXF(fullFilename)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| fullFilename | string | The full filename, including the path, of the DXF file. |

## Version

Introduced in version August 2014  
Retired in version July 2025  

