# ConfigurationSheetMetalRuleCell Object

Derived from: [ConfigurationCell](ConfigurationCell.md) Object  

## Description

Represents a single cell within a configuration table that controls which sheet metal rule is assigned to a component.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationSheetMetalRuleCell_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConfigurationSheetMetalRuleCell_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationSheetMetalRuleCell_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentColumn](ConfigurationSheetMetalRuleCell_parentColumn.md) | Returns the column this cell is in. |
| [parentRow](ConfigurationSheetMetalRuleCell_parentRow.md) | Returns the row this cell is in. |
| [sheetMetalRule](ConfigurationSheetMetalRuleCell_sheetMetalRule.md) | Gets and sets the sheet metal rule defined for this cell. |

## Accessed From

[ConfigurationSheetMetalRuleColumn.getCell](ConfigurationSheetMetalRuleColumn_getCell.md), [ConfigurationSheetMetalRuleColumn.getCellByRowId](ConfigurationSheetMetalRuleColumn_getCellByRowId.md), [ConfigurationSheetMetalRuleColumn.getCellByRowName](ConfigurationSheetMetalRuleColumn_getCellByRowName.md)

## Version

Introduced in version January 2024  

