# ConfigurationReplaceDesigns Object

Derived from: [Base](Base.md) Object  

## Description

Collection object that provides access to all the ConfigurationReplaceDesign objects that have been defined for a ConfigurationReplaceDesignColumn. You can also use this collection to define new replace designs that will then be available when specifying which design to use in a cell.

## Methods

| Name | Description |
|----|----|
| [add](ConfigurationReplaceDesigns_add.md) | Adds a new ConfigurationReplaceDesign object to the column. The ConfigurationReplaceDesign objects associated with the column can be used in the cells in the column. |
| [classType](ConfigurationReplaceDesigns_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](ConfigurationReplaceDesigns_item.md) | A method that returns the specified ConfigurationReplaceDesign object using an index into the collection. |
| [itemByName](ConfigurationReplaceDesigns_itemByName.md) | A method that returns the ConfigurationReplaceDesign object with the specified name. |

## Properties

| Name | Description |
| --- | --- |
| [count](ConfigurationReplaceDesigns_count.md) | Returns the number of ConfigurationReplaceDesign objects defined for the column. |
| [isValid](ConfigurationReplaceDesigns_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationReplaceDesigns_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[ConfigurationInsertStandardDesignColumn.replaceDesigns](ConfigurationInsertStandardDesignColumn_replaceDesigns.md)

## Version

Introduced in version September 2025  

