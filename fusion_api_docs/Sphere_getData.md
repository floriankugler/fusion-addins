# Sphere.getData Method

Parent Object: [Sphere](Sphere.md)  

## Description

Gets all of the data defining the sphere.

## Syntax

"sphere_var" is a variable referencing a [Sphere](Sphere.md) object.  

```python
(returnValue, origin, radius) = sphere_var.getData()
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point3D](Point3D.md) | The output origin point (center) of the sphere. |
| radius | double | The output radius of the sphere. |

## Version

Introduced in version August 2014  

