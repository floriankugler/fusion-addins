# ConfigurationThemeCell Object

Derived from: [ConfigurationCell](ConfigurationCell.md) Object  

## Description

Represents an individual cell within a top configuration table that specifies which row in the custom theme table should be used.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationThemeCell_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConfigurationThemeCell_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationThemeCell_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentColumn](ConfigurationThemeCell_parentColumn.md) | Returns the column this cell is in. |
| [parentRow](ConfigurationThemeCell_parentRow.md) | Returns the row this cell is in. |
| [referencedTableRow](ConfigurationThemeCell_referencedTableRow.md) | Gets and sets the row to use from the referenced table. |

## Accessed From

[ConfigurationThemeColumn.getCell](ConfigurationThemeColumn_getCell.md), [ConfigurationThemeColumn.getCellByRowId](ConfigurationThemeColumn_getCellByRowId.md), [ConfigurationThemeColumn.getCellByRowName](ConfigurationThemeColumn_getCellByRowName.md)

## Version

Introduced in version January 2024  

