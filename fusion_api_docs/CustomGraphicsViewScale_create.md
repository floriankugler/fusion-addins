# CustomGraphicsViewScale.create Method

Parent Object: [CustomGraphicsViewScale](CustomGraphicsViewScale.md)  

## Description

Creates a new CustomGraphicsViewScale object that can be used when setting the viewScale property of a custom graphics entity to specify the scaling behavior.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.CustomGraphicsViewScale.create(pixelScale, anchorPoint)
```

## Return Value

| Type | Description |
|----|----|
| [CustomGraphicsViewScale](CustomGraphicsViewScale.md) | Returns the newly created CustomGraphicsViewScale object or null in the case of failure. This can then be assigned to any custom graphics entity using its viewScale property. |

## Parameters

| Name | Type | Description |
|----|----|----|
| pixelScale | double | Defines the scale of the custom graphics relative to the view. If a custom graphics line is defined to be 100 units long it would usually display as 100 cm long. When it is view scaled with a pixel scale of 1 it will display as 100 pixels long. |
| anchorPoint | [Point3D](Point3D.md) | Defines the point in the graphics that defines the origin of the scaling. The graphics will be scaled up or down relative to that point. |

## Version

Introduced in version September 2017  

