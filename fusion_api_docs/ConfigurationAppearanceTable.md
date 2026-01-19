# ConfigurationAppearanceTable Object

Derived from: [ConfigurationTable](ConfigurationTable.md) Object  

## Description

Represents a configuration table that defines the appearances assigned to bodies and components.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationAppearanceTable_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [clear](ConfigurationAppearanceTable_clear.md) | Clears the content of the appearance table, removes the reference from the top table, and hides it in the user interface. |
| [getCell](ConfigurationAppearanceTable_getCell.md) | Returns the cell at the specified row and column. |

## Properties

| Name | Description |
| --- | --- |
| [columns](ConfigurationAppearanceTable_columns.md) | Returns the collection that provides access to this table's columns and the ability to create new columns. |
| [id](ConfigurationAppearanceTable_id.md) | Returns the unique ID of this table. |
| [isValid](ConfigurationAppearanceTable_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](ConfigurationAppearanceTable_name.md) | Returns the name of the table as seen in the user interface. |
| [objectType](ConfigurationAppearanceTable_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentTableColumn](ConfigurationAppearanceTable_parentTableColumn.md) | Returns the column in the top table that references this appearance table. |
| [rows](ConfigurationAppearanceTable_rows.md) | Returns the rows (configurations) defined for this table and provides the functionality to create new rows. |

## Accessed From

[ConfigurationAppearanceColumn.parentAppearanceTable](ConfigurationAppearanceColumn_parentAppearanceTable.md), [ConfigurationTopTable.appearanceTable](ConfigurationTopTable_appearanceTable.md)

## Version

Introduced in version January 2024  

