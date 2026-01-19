# Decal Object

Derived from: [Base](Base.md) Object  

## Description

Represents a Decal within a component.

## Methods

| Name | Description |
| --- | --- |
| [classType](Decal_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](Decal_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](Decal_deleteMe.md) | Deletes the decal from the component. |
| [redefine](Decal_redefine.md) | Redefines the position, orientation, and how the decal is applied to the body. To call this method, you need to position the timeline marker to immediately before this decal. This can be accomplished using the following code: thisDecal.timelineObject.rollTo(True) |
| [saveImage](Decal_saveImage.md) | Saves the image associated with the decal to the specified file. This is useful in cases where the original image file is no longer available but you need the image for some other purpose. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](Decal_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [deriveFeature](Decal_deriveFeature.md) | Returns the DeriveFeature if this decal is derived from another design. This property returns null if the decal is not derived from another design (i.e. isDerived property returns false). |
| [entityToken](Decal_entityToken.md) | Returns a token for the Decal object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same Decal. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [faces](Decal_faces.md) | Gets the faces the decal is associated with. Typically, this is an array containing a single face. If the isChainFaces property is true, this will return the primary face. If the isChainFaces property is false, the decal is limited to the faces in this list. If multiple faces have been provided, the first face in the list is the primary face, which is used to position and orient the decal. To set the faces, use the redefine method. |
| [imageFilename](Decal_imageFilename.md) | Gets and sets the filename of the image used for the decal. When getting this property, the filename returned is the file that was used when the decal was initially created. it's possible the file may no longer exist. When setting this property, it is the full filename to the image to use for the decal. PNG, JPEG, and TIFF files are supported. |
| [isChainFaces](Decal_isChainFaces.md) | Returns if the decal is limited to a specified set of faces or wraps onto all faces in the body. If this property is True, a single face has been specified and the decal can wrap onto other faces of the body. If False, the decal is limited to the set of specified faces. To change this setting, use the redefine method. |
| [isDerived](Decal_isDerived.md) | Returns if this decal is derived from another design. If true, the canvas cannot be deleted. You should not attempt to make any edits to the derived decal. Any edits made to this derived decal will be lost when the derive updates. |
| [isLightBulbOn](Decal_isLightBulbOn.md) | Gets and sets if the light bulb of this decal as displayed in the browser is on or off. A decal will only be visible if the light bulb is switched on. However, the light bulb can be on and the decal still invisible if the visibility of a higher level occurrence has its light bulb off or if the light bulb for the Decals folder is off to turn off all decals in a component. |
| [isValid](Decal_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](Decal_isVisible.md) | Returns if the decal is currently visible in the graphics window. The isLightBulbOn property of the decal controls if the decal should be displayed or not, but even when true, the decal may not be visible because the occurrence that references the component may not be visible. It's also possible to turn off the visibility of all the decals in a component. This property takes all of that into account when reporting if the decal is visible or not. |
| [name](Decal_name.md) | Gets and sets the name of the decal. This is the name seen in the browser and timeline. |
| [nativeObject](Decal_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of it's parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](Decal_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [opacity](Decal_opacity.md) | Gets and sets the opacity of the decal where 0 is completely transparent and 1.0 is completely opaque. Setting this property to a value outside the range of 0-1 will result in the value being set to the closest valid value. Defaults to 1.0 when the input is created. |
| [timelineObject](Decal_timelineObject.md) | Returns the timeline object associated with the creation of this decal. |
| [transform](Decal_transform.md) | Gets the transform of the decal. The returned matrix defines the position, rotation, scaling, and flipping. This is done by providing a 3D matrix which defines a 3D coordinate system in model space. The origin of the matrix defines the center of the decal and must lie somewhere on the first face. The normal of the face defines the Z axis of the matrix and the X and Y axes define the orientation of the decal and must be both perpendicular to the Z axis and to each other. Reversing the direction of the X or Y axis will flip the decal in that direction. The magnitude of the X and Y axes controls the scale and the scale can be non-uniform, meaning the length of the X and Y vectors do not need to be the same. To set the transform, use the redefine method. |

## Accessed From

[Decal.createForAssemblyContext](Decal_createForAssemblyContext.md), [Decal.nativeObject](Decal_nativeObject.md), [Decals.add](Decals_add.md), [Decals.item](Decals_item.md), [Decals.itemByName](Decals_itemByName.md)

## Version

Introduced in version September 2024  

