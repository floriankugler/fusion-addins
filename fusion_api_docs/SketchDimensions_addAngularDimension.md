# SketchDimensions.addAngularDimension Method

Parent Object: [SketchDimensions](SketchDimensions.md)  

## Description

Creates a new angular dimension constraint between the two input lines. The position of the text controls which of the four quadrants will be dimensioned.

## Syntax

"sketchDimensions_var" is a variable referencing a [SketchDimensions](SketchDimensions.md) object.

```python
# Uses no optional arguments.
returnValue = sketchDimensions_var.addAngularDimension(lineOne, lineTwo, textPoint)

# Uses optional arguments.
returnValue = sketchDimensions_var.addAngularDimension(lineOne, lineTwo, textPoint, isDriving)
```

## Return Value

| Type | Description |
|----|----|
| [SketchAngularDimension](SketchAngularDimension.md) | Returns the newly created dimension or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| lineOne | [SketchLine](SketchLine.md) | The first SketchLine to dimension to. |
| lineTwo | [SketchLine](SketchLine.md) | The second SketchLine to dimension to. |
| textPoint | [Point3D](Point3D.md) | A Point3D object that defines the position of the dimension text. The position of the text also defines which quadrant will be dimensioned. |
| isDriving | boolean | Optional argument that specifies if a driving (the dimension controls the geometry) or a driven (the geometry controls the dimension) dimension is created. If not provided a driving dimension will be created. This is an optional argument whose default value is True. |

## Samples

| Name | Description |
|----|----|
| [SketchDimensions.addAngularDimension](SketchDimension_addAngularDimension_Sample.md) | Demonstrates the SketchDimension.addAngularDimension method. |

## Version

Introduced in version August 2014  

