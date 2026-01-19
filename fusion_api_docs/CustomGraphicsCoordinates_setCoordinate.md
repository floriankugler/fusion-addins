# CustomGraphicsCoordinates.setCoordinate Method

Parent Object: [CustomGraphicsCoordinates](CustomGraphicsCoordinates.md)  

## Description

Sets the coordinate at the specified index.

## Syntax

"customGraphicsCoordinates_var" is a variable referencing a [CustomGraphicsCoordinates](CustomGraphicsCoordinates.md) object.

```python
returnValue = customGraphicsCoordinates_var.setCoordinate(index, coordinate)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true if setting the coordinate was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | integer | The index of the coordinate to set. The first coordinate has an index of 0. |
| coordinate | [Point3D](Point3D.md) | The coordinate value as a Point3D object. |

## Version

Introduced in version September 2017  

