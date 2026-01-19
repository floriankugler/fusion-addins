# ConfigurationInsertStandardDesignCell Object

Derived from: [ConfigurationCell](ConfigurationCell.md) Object  

## Description

Represents a single cell within a top or custom theme configuration table that controls which design is used for an inserted standard design. Use the parent column to get the occurrence being modified.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationInsertStandardDesignCell_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConfigurationInsertStandardDesignCell_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationInsertStandardDesignCell_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentColumn](ConfigurationInsertStandardDesignCell_parentColumn.md) | Returns the column this cell is in. |
| [parentRow](ConfigurationInsertStandardDesignCell_parentRow.md) | Returns the row this cell is in. |
| [replaceDesign](ConfigurationInsertStandardDesignCell_replaceDesign.md) | Gets and sets which ConfigurationReplaceDesign object will be used when the row this cell is in is active. When setting this property, only ConfigurationReplaceDesign objects defined for the parent column of this cell can be used. |

## Accessed From

[ConfigurationInsertStandardDesignColumn.getCell](ConfigurationInsertStandardDesignColumn_getCell.md), [ConfigurationInsertStandardDesignColumn.getCellByRowId](ConfigurationInsertStandardDesignColumn_getCellByRowId.md), [ConfigurationInsertStandardDesignColumn.getCellByRowName](ConfigurationInsertStandardDesignColumn_getCellByRowName.md)

## Version

Introduced in version September 2025  

