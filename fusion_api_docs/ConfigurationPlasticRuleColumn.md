# ConfigurationPlasticRuleColumn Object

Derived from: [ConfigurationColumn](ConfigurationColumn.md) Object  

## Description

Represents a plastic rule column in a configuration table. This defines the plastic rule to use for a specific component.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationPlasticRuleColumn_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](ConfigurationPlasticRuleColumn_deleteMe.md) | Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail. |
| [getCell](ConfigurationPlasticRuleColumn_getCell.md) | Gets the cell in this column at the specified row. The first row has an index of 0 and does not include the header row. |
| [getCellByRowId](ConfigurationPlasticRuleColumn_getCellByRowId.md) | Gets the cell in this column at the row specified by its ID. |
| [getCellByRowName](ConfigurationPlasticRuleColumn_getCellByRowName.md) | Gets the cell in this column at the row specified by its name. |

## Properties

| Name | Description |
| --- | --- |
| [component](ConfigurationPlasticRuleColumn_component.md) | Returns the Component being modified by this column. This property returns null when the table being queried was obtained from a DataFile object. |
| [id](ConfigurationPlasticRuleColumn_id.md) | The id of the column. This is constant and cannot be changed by the user. |
| [index](ConfigurationPlasticRuleColumn_index.md) | The index position of this column within the table. The first column is at index 0 and does not include the "Name" column. |
| [isValid](ConfigurationPlasticRuleColumn_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationPlasticRuleColumn_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentPlasticRuleTable](ConfigurationPlasticRuleColumn_parentPlasticRuleTable.md) | Returns the parent plastic rule table this column is in. |
| [rowCount](ConfigurationPlasticRuleColumn_rowCount.md) | Returns the number of rows in this column. |
| [title](ConfigurationPlasticRuleColumn_title.md) | The title of this column. In a top table, this can only be edited for suppression, visibility, parameter, and theme table columns. It behaves as read-only for all other types. In a theme table, the title of all the columns can be modified except for the column that represents the root component for materials and appearances. If the table was obtained from a DataFile, this property behaves as read-only for all the columns. |

## Accessed From

[ConfigurationPlasticRuleCell.parentColumn](ConfigurationPlasticRuleCell_parentColumn.md), [ConfigurationPlasticRuleColumns.add](ConfigurationPlasticRuleColumns_add.md), [ConfigurationPlasticRuleColumns.item](ConfigurationPlasticRuleColumns_item.md), [ConfigurationPlasticRuleColumns.itemById](ConfigurationPlasticRuleColumns_itemById.md)

## Version

Introduced in version January 2024  

