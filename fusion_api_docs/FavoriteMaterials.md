# FavoriteMaterials Object

Derived from: [Base](Base.md) Object  

## Description

Collection of the favorite materials.

## Methods

| Name | Description |
|----|----|
| [add](FavoriteMaterials_add.md) | Adds an existing material to the Favorites list |
| [classType](FavoriteMaterials_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](FavoriteMaterials_item.md) | Returns the specified Material using an index into the collection. |
| [itemById](FavoriteMaterials_itemById.md) | Returns the Material by it's internal unique ID. |
| [itemByName](FavoriteMaterials_itemByName.md) | Returns the specified Material using the name as seen in the user interface. This often isn't a reliable way of accessing a specific material because materials are not required to be unique. |

## Properties

| Name | Description |
| --- | --- |
| [count](FavoriteMaterials_count.md) | The number of Materials in the collection. |
| [isValid](FavoriteMaterials_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](FavoriteMaterials_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Application.favoriteMaterials](Application_favoriteMaterials.md)

## Version

Introduced in version August 2014  

