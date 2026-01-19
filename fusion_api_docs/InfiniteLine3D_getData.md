# InfiniteLine3D.getData Method

Parent Object: [InfiniteLine3D](InfiniteLine3D.md)  

## Description

Gets all of the data defining the infinite line.

## Syntax

"infiniteLine3D_var" is a variable referencing an [InfiniteLine3D](InfiniteLine3D.md) object.  

```python
(returnValue, origin, direction) = infiniteLine3D_var.getData()
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name      | Type                     | Description                          |
|-----------|--------------------------|--------------------------------------|
| origin    | [Point3D](Point3D.md)   | The output origin point of the line. |
| direction | [Vector3D](Vector3D.md) | The output direction of the line.    |

## Version

Introduced in version August 2014  

