# Properties Object

Derived from: [Base](Base.md) Object  

## Description

A collection of properties that are associated with a material or appearance.

## Methods

| Name | Description |
|----|----|
| [classType](Properties_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](Properties_item.md) | Returns the specified property from the collection using an index into the collection. |
| [itemById](Properties_itemById.md) | Returns the specified property from the collection using the unique ID of the property. |
| [itemByName](Properties_itemByName.md) | Returns the specified Property using the name of the property. |

## Properties

| Name | Description |
| --- | --- |
| [count](Properties_count.md) | Returns the number of properties within the collection. |
| [isValid](Properties_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Properties_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Appearance.appearanceProperties](Appearance_appearanceProperties.md), [AppearanceTexture.properties](AppearanceTexture_properties.md), [Material.materialProperties](Material_materialProperties.md)

## Version

Introduced in version August 2014  

