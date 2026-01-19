# Point3D.isEqualTo Method

Parent Object: [Point3D](Point3D.md)  

## Description

Checks to see if this point and another point are equal (have identical coordinates). The comparison is done within the modeling tolerance which can be found with the Application.pointTolerance property. If you want to compare two points with any other tolerance you can use the isEqualToByTolerance method.

## Syntax

"point3D_var" is a variable referencing a [Point3D](Point3D.md) object.

```python
returnValue = point3D_var.isEqualTo(point)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the points are equal (have identical coordinates). |

## Parameters

| Name  | Type                   | Description                        |
|-------|------------------------|------------------------------------|
| point | [Point3D](Point3D.md) | The point to compare for equality. |

## Version

Introduced in version August 2014  

