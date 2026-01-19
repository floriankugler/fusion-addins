# ConfigurationInsertColumn Object

Derived from: [ConfigurationColumn](ConfigurationColumn.md) Object  

## Description

Represents a column where a configured design has been inserted in this design.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationInsertColumn_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](ConfigurationInsertColumn_deleteMe.md) | Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail. |
| [getCell](ConfigurationInsertColumn_getCell.md) | Gets the cell in this column at the specified row. The first row has an index of 0 and does not include the header row. |
| [getCellByRowId](ConfigurationInsertColumn_getCellByRowId.md) | Gets the cell in this column at the row specified by its ID. |
| [getCellByRowName](ConfigurationInsertColumn_getCellByRowName.md) | Gets the cell in this column at the row specified by its name. |

## Properties

| Name | Description |
| --- | --- |
| [id](ConfigurationInsertColumn_id.md) | The id of the column. This is constant and cannot be changed by the user. |
| [index](ConfigurationInsertColumn_index.md) | The index position of this column within the table. The first column is at index 0 and does not include the "Name" column. |
| [isValid](ConfigurationInsertColumn_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationInsertColumn_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [occurrence](ConfigurationInsertColumn_occurrence.md) | Returns the occurrence that is associated with this configuration insertion. This property returns null when the table being queried was obtained from a DataFile object. |
| [parentTable](ConfigurationInsertColumn_parentTable.md) | Returns the parent table, either top or custom theme table, this column is in. |
| [rowCount](ConfigurationInsertColumn_rowCount.md) | Returns the number of rows in this column. |
| [title](ConfigurationInsertColumn_title.md) | The title of this column. In a top table, this can only be edited for suppression, visibility, parameter, and theme table columns. It behaves as read-only for all other types. In a theme table, the title of all the columns can be modified except for the column that represents the root component for materials and appearances. If the table was obtained from a DataFile, this property behaves as read-only for all the columns. |

## Accessed From

[ConfigurationColumns.addInsertColumn](ConfigurationColumns_addInsertColumn.md), [ConfigurationInsertCell.parentColumn](ConfigurationInsertCell_parentColumn.md)

## Version

Introduced in version January 2024  

