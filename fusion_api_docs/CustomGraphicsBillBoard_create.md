# CustomGraphicsBillBoard.create Method

Parent Object: [CustomGraphicsBillBoard](CustomGraphicsBillBoard.md)  

## Description

Creates a new CustomGraphicsBillBoard object that can be used when calling the billBoarding property of the CustomGraphicsEntity object to specify the billboarding behavior of some custom graphics. Once created you can assign it to a custom graphics entity using its billBoarding property.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.CustomGraphicsBillBoard.create(anchorPoint)
```

## Return Value

| Type | Description |
|----|----|
| [CustomGraphicsBillBoard](CustomGraphicsBillBoard.md) | Returns the newly created CustomGraphicsBillBoard object or null in the case of failure. This can be assigned to a custom graphics entity using its billBoarding property. |

## Parameters

| Name | Type | Description |
|----|----|----|
| anchorPoint | [Point3D](Point3D.md) | The parameter must be input and can be null but the value is ignored. Use of the anchor point has been retired and it is no longer used. |

## Version

Introduced in version September 2017  

