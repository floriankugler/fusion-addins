# ConfigurationPropertyCell Object

Derived from: [ConfigurationCell](ConfigurationCell.md) Object  

## Description

Represents an individual cell within a configuration table that defines the value of a property.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationPropertyCell_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConfigurationPropertyCell_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationPropertyCell_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentColumn](ConfigurationPropertyCell_parentColumn.md) | Returns the column this cell is in. |
| [parentRow](ConfigurationPropertyCell_parentRow.md) | Returns the row this cell is in. |
| [value](ConfigurationPropertyCell_value.md) | Gets and sets the value of the property associated with the parent column of this cell. |

## Accessed From

[ConfigurationPropertyColumn.getCell](ConfigurationPropertyColumn_getCell.md), [ConfigurationPropertyColumn.getCellByRowId](ConfigurationPropertyColumn_getCellByRowId.md), [ConfigurationPropertyColumn.getCellByRowName](ConfigurationPropertyColumn_getCellByRowName.md)

## Version

Introduced in version January 2024  

