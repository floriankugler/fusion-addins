# ConfigurationInsertStandardDesignColumn Object

Derived from: [ConfigurationColumn](ConfigurationColumn.md) Object  

## Description

This object represents a column in the table that controls which design should be referenced by an occurrence. The column contains a list of designs that have been specified for that column. One of the designs is specified for each cell in the column. That design will be referenced by the occurrence when the row that cell is in is active.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationInsertStandardDesignColumn_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](ConfigurationInsertStandardDesignColumn_deleteMe.md) | Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail. |
| [getCell](ConfigurationInsertStandardDesignColumn_getCell.md) | Gets the cell in this column at the specified row. The first row has an index of 0 and does not include the header row. |
| [getCellByRowId](ConfigurationInsertStandardDesignColumn_getCellByRowId.md) | Gets the cell in this column at the row specified by its ID. |
| [getCellByRowName](ConfigurationInsertStandardDesignColumn_getCellByRowName.md) | Gets the cell in this column at the row specified by its name. |

## Properties

| Name | Description |
| --- | --- |
| [id](ConfigurationInsertStandardDesignColumn_id.md) | The id of the column. This is constant and cannot be changed by the user. |
| [index](ConfigurationInsertStandardDesignColumn_index.md) | The index position of this column within the table. The first column is at index 0 and does not include the "Name" column. |
| [isValid](ConfigurationInsertStandardDesignColumn_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationInsertStandardDesignColumn_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [occurrence](ConfigurationInsertStandardDesignColumn_occurrence.md) | Returns the occurrence being controlled by this column. This property returns null when the table being queried was obtained from a DataFile object. |
| [parentTable](ConfigurationInsertStandardDesignColumn_parentTable.md) | Returns the parent table this column is in. |
| [replaceDesigns](ConfigurationInsertStandardDesignColumn_replaceDesigns.md) | Provides access to the list of replace designs that have been defined for this column. Using the returned collection you can define new ConfigurationReplaceDesign objects. Use the cells in the column to specify which one of the defined replace designs is used for a specific row. |
| [rowCount](ConfigurationInsertStandardDesignColumn_rowCount.md) | Returns the number of rows in this column. |
| [title](ConfigurationInsertStandardDesignColumn_title.md) | The title of this column. In a top table, this can only be edited for suppression, visibility, parameter, and theme table columns. It behaves as read-only for all other types. In a theme table, the title of all the columns can be modified except for the column that represents the root component for materials and appearances. If the table was obtained from a DataFile, this property behaves as read-only for all the columns. |

## Accessed From

[ConfigurationColumns.addInsertStandardDesignColumn](ConfigurationColumns_addInsertStandardDesignColumn.md), [ConfigurationInsertStandardDesignCell.parentColumn](ConfigurationInsertStandardDesignCell_parentColumn.md)

## Version

Introduced in version September 2025  

