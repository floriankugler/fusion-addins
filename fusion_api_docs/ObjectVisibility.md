# ObjectVisibility Object

Derived from: [Base](Base.md) Object  

## Description

An object that provides control over which objects are displayed in the graphics window. This is the equivalent of the "Object Visibility" settings in the Display Settings drop-down in the navigation toolbar at the bottom of the Fusion graphics window.

## Methods

| Name | Description |
|----|----|
| [classType](ObjectVisibility_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isAllObjectsVisible](ObjectVisibility_isAllObjectsVisible.md) | Sets if all objects are visible or hidden. When setting this property it will set the value of all other properties of this object to true or false. When getting this property, if it is true, then all other properties are true. If false, one or more other properties are false. |
| [isJointOriginAxesVisible](ObjectVisibility_isJointOriginAxesVisible.md) | Gets and sets if the axes lines shown in the glyphs for joint origins in all components, local or referenced by this design, are visible in the graphics window. |
| [isJointOriginsVisible](ObjectVisibility_isJointOriginsVisible.md) | Gets and sets if the glyphs for joint origins in all components, local or referenced by this design, are visible in the graphics window. |
| [isJointsVisible](ObjectVisibility_isJointsVisible.md) | Gets and sets if the glyphs for joints in all components, local or referenced by this design, are visible. |
| [isOriginAxesVisible](ObjectVisibility_isOriginAxesVisible.md) | Gets and sets if the origin construction axes of all components, local or referenced by this design, are visible in the graphics window. |
| [isOriginPlanesVisible](ObjectVisibility_isOriginPlanesVisible.md) | Gets and sets if the origin construction planes of all components, local or referenced by this design, are visible in the graphics window. |
| [isOriginPointsVisible](ObjectVisibility_isOriginPointsVisible.md) | Gets and sets if the origin construction points of all components, local or referenced by this design, are visible in the graphics window. |
| [isSketchesVisible](ObjectVisibility_isSketchesVisible.md) | Gets and sets if the sketches in all components, local or referenced by this design, are visible in the graphics window. |
| [isUserWorkAxesVisible](ObjectVisibility_isUserWorkAxesVisible.md) | Gets and sets if the user created construction axes of all components, local or referenced by this design, are visible in the graphics window. |
| [isUserWorkPlanesVisible](ObjectVisibility_isUserWorkPlanesVisible.md) | Gets and sets if the user created construction planes of all components, local or referenced by this design, are visible in the graphics window. |
| [isUserWorkPointsVisible](ObjectVisibility_isUserWorkPointsVisible.md) | Gets and sets if the user created construction points of all components, local or referenced by this design, are visible in the graphics window. |
| [isValid](ObjectVisibility_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ObjectVisibility_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Design.objectVisibility](Design_objectVisibility.md), [FlatPatternProduct.objectVisibility](FlatPatternProduct_objectVisibility.md), [WorkingModel.objectVisibility](WorkingModel_objectVisibility.md)

## Version

Introduced in version November 2025  

