# ConfigurationInsertCell Object

Derived from: [ConfigurationCell](ConfigurationCell.md) Object  

## Description

Represents a single cell within a top or custom theme configuration table that controls which configuration is used for an inserted configured design. Use the parent column to get the feature being suppressed.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationInsertCell_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConfigurationInsertCell_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationInsertCell_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentColumn](ConfigurationInsertCell_parentColumn.md) | Returns the column this cell is in. |
| [parentRow](ConfigurationInsertCell_parentRow.md) | Returns the row this cell is in. |
| [row](ConfigurationInsertCell_row.md) | Gets and sets which row of the configured design is used for this cell. When setting this property, the row must come from the configured design used by the occurrence associated with the parent column of this cell. |

## Accessed From

[ConfigurationInsertColumn.getCell](ConfigurationInsertColumn_getCell.md), [ConfigurationInsertColumn.getCellByRowId](ConfigurationInsertColumn_getCellByRowId.md), [ConfigurationInsertColumn.getCellByRowName](ConfigurationInsertColumn_getCellByRowName.md)

## Version

Introduced in version January 2024  

