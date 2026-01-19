# PhysicalProperties.getPrincipalAxes Method

Parent Object: [PhysicalProperties](PhysicalProperties.md)  

## Description

Method that returns the principal axes.

## Syntax

"physicalProperties_var" is a variable referencing a [PhysicalProperties](PhysicalProperties.md) object.  

```python
(returnValue, xAxis, yAxis, zAxis) = physicalProperties_var.getPrincipalAxes()
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| xAxis | [Vector3D](Vector3D.md) | The output Vector3D object that indicates the direction of the x axis. |
| yAxis | [Vector3D](Vector3D.md) | The output Vector3D object that indicates the direction of the y axis. |
| zAxis | [Vector3D](Vector3D.md) | The output Vector3D object that indicates the direction of the z axis. |

## Samples

| Name | Description |
|----|----|
| [Get Physical Properties API Sample](GetPhysicalProperties_Sample.md) | Script that demonstrates getting physical properties using the API. When this script is run it will create a new document, build a simple model, and get the various physical properties from the model. |

## Version

Introduced in version May 2016  

