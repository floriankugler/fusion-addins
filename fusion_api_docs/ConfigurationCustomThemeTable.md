# ConfigurationCustomThemeTable Object

Derived from: [ConfigurationTable](ConfigurationTable.md) Object  

## Description

API object representing a custom theme configuration table associated with a top table.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationCustomThemeTable_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](ConfigurationCustomThemeTable_deleteMe.md) | Deletes this custom theme table from the configuration. |
| [getCell](ConfigurationCustomThemeTable_getCell.md) | Returns the cell at the specified row and column. |
| [moveColumns](ConfigurationCustomThemeTable_moveColumns.md) | Moves the specified columns from one table to another. |

## Properties

| Name | Description |
| --- | --- |
| [columns](ConfigurationCustomThemeTable_columns.md) | Returns the columns in this table. |
| [id](ConfigurationCustomThemeTable_id.md) | Returns the unique ID of this table. |
| [isValid](ConfigurationCustomThemeTable_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](ConfigurationCustomThemeTable_name.md) | Gets and sets the name of the table as seen in the user interface. |
| [objectType](ConfigurationCustomThemeTable_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentTableColumn](ConfigurationCustomThemeTable_parentTableColumn.md) | Returns the column in the top table that references this custom theme table. |
| [rows](ConfigurationCustomThemeTable_rows.md) | Returns the rows (configurations) defined for this table and provides the functionality to create new rows. |

## Accessed From

[ConfigurationCustomThemeTables.add](ConfigurationCustomThemeTables_add.md), [ConfigurationCustomThemeTables.item](ConfigurationCustomThemeTables_item.md)

## Version

Introduced in version January 2024  

