# AreaProperties.getPrincipalAxes Method

Parent Object: [AreaProperties](AreaProperties.md)  

## Description

Method that returns the principal axes.

## Syntax

"areaProperties_var" is a variable referencing an [AreaProperties](AreaProperties.md) object.  

```python
(returnValue, xAxis, yAxis) = areaProperties_var.getPrincipalAxes()
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

## Samples

| Name | Description |
|----|----|
| [API Sample for AreaProperties](AreaPropertiesSample_Sample.md) | Demonstrates how to use AreaProperties |

## Version

Introduced in version March 2016  

