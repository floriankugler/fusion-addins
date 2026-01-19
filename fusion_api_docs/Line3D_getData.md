# Line3D.getData Method

Parent Object: [Line3D](Line3D.md)  

## Description

Gets all of the data defining the line segment.

## Syntax

"line3D_var" is a variable referencing a [Line3D](Line3D.md) object.  

```python
(returnValue, startPoint, endPoint) = line3D_var.getData()
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name       | Type                   | Description                         |
|------------|------------------------|-------------------------------------|
| startPoint | [Point3D](Point3D.md) | The output start point of the line. |
| endPoint   | [Point3D](Point3D.md) | The output end point of the line.   |

## Version

Introduced in version August 2014  

