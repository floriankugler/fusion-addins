# ProjectedTextureMapControl Object

Derived from: [TextureMapControl](TextureMapControl.md) Object  

## Description

Provides access to the various settings that control how a projected texture is applied to a body.

## Methods

| Name | Description |
|----|----|
| [classType](ProjectedTextureMapControl_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [reset](ProjectedTextureMapControl_reset.md) | Resets the texture map back to its original default settings. |

## Properties

| Name | Description |
| --- | --- |
| [isCapped](ProjectedTextureMapControl_isCapped.md) | When a cylindrical projected texture map is being used this property gets and sets if a cap is use for the cylindrical projection. This property is only valid in the case when the projectedTextureMapType returns CylindricalTextureMapProjection. The value of this property should be ignored in all other cases and setting the property will have no effect. |
| [isValid](ProjectedTextureMapControl_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ProjectedTextureMapControl_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [projectedTextureMapType](ProjectedTextureMapControl_projectedTextureMapType.md) | Gets and sets how the texture map is being applied onto the body. |
| [transform](ProjectedTextureMapControl_transform.md) | Gets and sets the transform that defines the position and orientation of how the texture is projected onto the body. The Z axis of the transform corresponds to the axis that is specified in the user-interface and is the primary direction of the texture. |

## Version

Introduced in version March 2022  

