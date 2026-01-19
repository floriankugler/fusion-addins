# CustomGraphicsCoordinates.create Method

Parent Object: [CustomGraphicsCoordinates](CustomGraphicsCoordinates.md)  

## Description

Static method that creates a CustomGraphicsCoordinates object which can be used as input to various custom graphics methods.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.CustomGraphicsCoordinates.create(coordinates)
```

## Return Value

| Type | Description |
|----|----|
| [CustomGraphicsCoordinates](CustomGraphicsCoordinates.md) | Returns the created CustomGraphicsCoordinates object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| coordinates | double\[\] | An array of doubles where the values are the x, y, z components of each coordinate where the unit of measure is centimeters. |

## Version

Introduced in version September 2017  

