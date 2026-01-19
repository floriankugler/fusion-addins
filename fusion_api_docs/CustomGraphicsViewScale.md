# CustomGraphicsViewScale Object

Derived from: [Base](Base.md) Object  

## Description

Specifies that custom graphics are to be scaled relative to the view (pixels) and not model space. If this is applied to some custom graphics then they will stat the same size on the screen regardless of the user zooming in or out. This is commonly used for glyphs and other interactive widgets so they don't don't get too large or too small.

## Methods

| Name | Description |
|----|----|
| [classType](CustomGraphicsViewScale_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](CustomGraphicsViewScale_create.md) | Creates a new CustomGraphicsViewScale object that can be used when setting the viewScale property of a custom graphics entity to specify the scaling behavior. |

## Properties

| Name | Description |
| --- | --- |
| [anchorPoint](CustomGraphicsViewScale_anchorPoint.md) | Gets and sets the point in the graphics that defines the origin of the scaling. The graphics will be scaled up or down relative to that point. |
| [isValid](CustomGraphicsViewScale_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CustomGraphicsViewScale_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [pixelScale](CustomGraphicsViewScale_pixelScale.md) | Gets and sets the scale of the custom graphics relative to the view. If a custom graphics line is defined to be 100 units long it would usually display as 100 cm long. When it is view scaled with a pixel scale of 1 it will display as 100 pixels long. |

## Accessed From

[CustomGraphicsBRepBody.viewScale](CustomGraphicsBRepBody_viewScale.md), [CustomGraphicsCurve.viewScale](CustomGraphicsCurve_viewScale.md), [CustomGraphicsEntity.viewScale](CustomGraphicsEntity_viewScale.md), [CustomGraphicsGroup.viewScale](CustomGraphicsGroup_viewScale.md), [CustomGraphicsLines.viewScale](CustomGraphicsLines_viewScale.md), [CustomGraphicsMesh.viewScale](CustomGraphicsMesh_viewScale.md), [CustomGraphicsPointSet.viewScale](CustomGraphicsPointSet_viewScale.md), [CustomGraphicsText.viewScale](CustomGraphicsText_viewScale.md), [CustomGraphicsViewScale.create](CustomGraphicsViewScale_create.md)

## Version

Introduced in version September 2017  

