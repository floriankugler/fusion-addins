# ConfigurationMaterialTable Object

Derived from: [ConfigurationTable](ConfigurationTable.md) Object  

## Description

Represents a configuration table that defines materials assigned to bodies and components.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationMaterialTable_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [clear](ConfigurationMaterialTable_clear.md) | Clears the content of the material table, removes the reference from the top table, and hides it in the user interface. |
| [getCell](ConfigurationMaterialTable_getCell.md) | Returns the cell at the specified row and column. |

## Properties

| Name | Description |
| --- | --- |
| [columns](ConfigurationMaterialTable_columns.md) | Returns the collection that provides access to the columns in this table. |
| [id](ConfigurationMaterialTable_id.md) | Returns the unique ID of this table. |
| [isValid](ConfigurationMaterialTable_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](ConfigurationMaterialTable_name.md) | Returns the name of the table as seen in the user interface. |
| [objectType](ConfigurationMaterialTable_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentTableColumn](ConfigurationMaterialTable_parentTableColumn.md) | Returns the column in the top table that references this material table. |
| [rows](ConfigurationMaterialTable_rows.md) | Returns the rows (configurations) defined for this table and provides the functionality to create new rows. |

## Accessed From

[ConfigurationMaterialColumn.parentMaterialTable](ConfigurationMaterialColumn_parentMaterialTable.md), [ConfigurationTopTable.materialTable](ConfigurationTopTable_materialTable.md)

## Version

Introduced in version January 2024  

