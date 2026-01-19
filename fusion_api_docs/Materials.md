# Materials Object

Derived from: [Base](Base.md) Object  

## Description

Collection of materials within a Library or Design.

## Methods

| Name | Description |
|----|----|
| [addByCopy](Materials_addByCopy.md) | Add a Material to a Design by copying an existing Material from Favorites, a Library or from the Materials stored in the Design. This method currently only applies to the Materials collection from a Design and cannot be used to copy a Material to a library. |
| [classType](Materials_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](Materials_item.md) | Returns the specified Material using an index into the collection. |
| [itemById](Materials_itemById.md) | Returns the Material by it's internal unique ID. |
| [itemByName](Materials_itemByName.md) | Returns the specified Material using the name as seen in the user interface. This often isn't a reliable way of accessing a specific material because materials are not required to be unique. |

## Properties

| Name | Description |
| --- | --- |
| [count](Materials_count.md) | The number of Materials in the collection. |
| [isValid](Materials_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Materials_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Design.materials](Design_materials.md), [FlatPatternProduct.materials](FlatPatternProduct_materials.md), [MaterialLibrary.materials](MaterialLibrary_materials.md), [WorkingModel.materials](WorkingModel_materials.md)

## Version

Introduced in version August 2014  

