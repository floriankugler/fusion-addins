# CustomGraphicsGroup.addCurve Method

Parent Object: [CustomGraphicsGroup](CustomGraphicsGroup.md)  

## Description

Adds a new CustomGraphicsCurve entity to this group. A CustomGraphicsCurve is a wireframe graphic that is based on any object derived from Curve3D (except InfiniteLine3D). This is useful when drawing curved geometry where the alternative is to stroke the smooth curve and draw it as a series of lines. Using this you can directly use the curve and Fusion will automatically take care of creating the correct display for the current level of detail.

## Syntax

"customGraphicsGroup_var" is a variable referencing a [CustomGraphicsGroup](CustomGraphicsGroup.md) object.

```python
returnValue = customGraphicsGroup_var.addCurve(curve)
```

## Return Value

| Type | Description |
|----|----|
| [CustomGraphicsCurve](CustomGraphicsCurve.md) | Returns the newly created CustomGraphicsCurve object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| curve | [Curve3D](Curve3D.md) | The curve that defines the shape of the graphics entity. Any of the curve types derived from Curve3D are valid except for InfiniteLine3D. |

## Samples

| Name | Description |
| --- | --- |
| [Custom Graphics Sample](CustomGraphicsSample_Sample.md) | A sample demonstrating how to create custom graphics entities. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/GraphicsSampleResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version September 2017  

