# ConfigurationSheetMetalRuleColumn Object

Derived from: [ConfigurationColumn](ConfigurationColumn.md) Object  

## Description

Represents a sheet metal rule column in a configuration table. This defines the sheet metal rule to use for a specific component.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationSheetMetalRuleColumn_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](ConfigurationSheetMetalRuleColumn_deleteMe.md) | Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail. |
| [getCell](ConfigurationSheetMetalRuleColumn_getCell.md) | Gets the cell in this column at the specified row. The first row has an index of 0 and does not include the header row. |
| [getCellByRowId](ConfigurationSheetMetalRuleColumn_getCellByRowId.md) | Gets the cell in this column at the row specified by its ID. |
| [getCellByRowName](ConfigurationSheetMetalRuleColumn_getCellByRowName.md) | Gets the cell in this column at the row specified by its name. |

## Properties

| Name | Description |
| --- | --- |
| [component](ConfigurationSheetMetalRuleColumn_component.md) | Returns the Component being modified by this column. This property returns null when the table being queried was obtained from a DataFile object. |
| [componentName](ConfigurationSheetMetalRuleColumn_componentName.md) | Returns the name of the component associated with this column. This is useful when the table is obtained from a DataFile object, and the component object is unavailable. |
| [id](ConfigurationSheetMetalRuleColumn_id.md) | The id of the column. This is constant and cannot be changed by the user. |
| [index](ConfigurationSheetMetalRuleColumn_index.md) | The index position of this column within the table. The first column is at index 0 and does not include the "Name" column. |
| [isValid](ConfigurationSheetMetalRuleColumn_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationSheetMetalRuleColumn_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentSheetMetalRuleTable](ConfigurationSheetMetalRuleColumn_parentSheetMetalRuleTable.md) | Returns the parent sheet metal rule table this column is in. |
| [rowCount](ConfigurationSheetMetalRuleColumn_rowCount.md) | Returns the number of rows in this column. |
| [title](ConfigurationSheetMetalRuleColumn_title.md) | The title of this column. In a top table, this can only be edited for suppression, visibility, parameter, and theme table columns. It behaves as read-only for all other types. In a theme table, the title of all the columns can be modified except for the column that represents the root component for materials and appearances. If the table was obtained from a DataFile, this property behaves as read-only for all the columns. |

## Accessed From

[ConfigurationSheetMetalRuleCell.parentColumn](ConfigurationSheetMetalRuleCell_parentColumn.md), [ConfigurationSheetMetalRuleColumns.add](ConfigurationSheetMetalRuleColumns_add.md), [ConfigurationSheetMetalRuleColumns.item](ConfigurationSheetMetalRuleColumns_item.md), [ConfigurationSheetMetalRuleColumns.itemById](ConfigurationSheetMetalRuleColumns_itemById.md)

## Version

Introduced in version January 2024  

