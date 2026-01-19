# TextureMapControl3D Object

Derived from: [TextureMapControl](TextureMapControl.md) Object  

## Description

Provides access to the various settings that control how a 3D texture is applied to a body.

## Methods

| Name | Description |
|----|----|
| [bestFit](TextureMapControl3D_bestFit.md) | Reorients the transform to best fit the geometry of the body. |
| [classType](TextureMapControl3D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [reset](TextureMapControl3D_reset.md) | Resets the texture map back to its original default settings. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](TextureMapControl3D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](TextureMapControl3D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [transform](TextureMapControl3D_transform.md) | Gets and sets the transform that defines the position and orientation of how the texture is applied to the body. For wood grain, the Z direction of the defined coordinate system is the direction of the grain. |

## Version

Introduced in version March 2022  

