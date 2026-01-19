# ConfigurationVisibilityCell Object

Derived from: [ConfigurationCell](ConfigurationCell.md) Object  

## Description

Represents a single cell within a configuration table that controls whether an entity is visible. Get the parent column to get the entity.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationVisibilityCell_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConfigurationVisibilityCell_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](ConfigurationVisibilityCell_isVisible.md) | Specifies if the entity is visible or not. This property behaves as read-only when the table is obtained from a DataFile. |
| [objectType](ConfigurationVisibilityCell_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentColumn](ConfigurationVisibilityCell_parentColumn.md) | Returns the column this cell is in. |
| [parentRow](ConfigurationVisibilityCell_parentRow.md) | Returns the row this cell is in. |

## Accessed From

[ConfigurationVisibilityColumn.getCell](ConfigurationVisibilityColumn_getCell.md), [ConfigurationVisibilityColumn.getCellByRowId](ConfigurationVisibilityColumn_getCellByRowId.md), [ConfigurationVisibilityColumn.getCellByRowName](ConfigurationVisibilityColumn_getCellByRowName.md)

## Version

Introduced in version January 2024  

