# Sketch.importSVG Method

Parent Object: [Sketch](Sketch.md)  

## Description

Imports the contents of an SVG file into the active sketch.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.importSVG(fullFilename, xPosition, yPosition, scale)
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the import was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| fullFilename | string | The full filename, including the path, of the SVG file. |
| xPosition | double | The X offset in centimeters in the sketch for the origin of the SVG data relative to the sketch origin. |
| yPosition | double | The Y offset in centimeters in the sketch for the origin of the SVG data relative to the sketch origin. |
| scale | double | The scale value to apply to the imported SVG data. |

## Version

Introduced in version August 2014  

