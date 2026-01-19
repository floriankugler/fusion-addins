# ConfigurationRows Object

Derived from: [Base](Base.md) Object  

## Description

Returns a collection of the rows in the table. The header row is not included in this list.

## Methods

| Name | Description |
|----|----|
| [add](ConfigurationRows_add.md) | Adds a new row to the table. For the top table, this creates a new configuration. For theme tables, this creates a new theme. The new row is added to the bottom of the table, and the cell values are copied from the row above it. You can also use the ConfigurationRow.copy method to create a new row by copying any existing row. |
| [classType](ConfigurationRows_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](ConfigurationRows_item.md) | A method that returns the specified row using an index into the collection. These are returned in the same order as in the table; the first row is the default row. |
| [itemById](ConfigurationRows_itemById.md) | A method that returns the row with the specified ID. |
| [itemByName](ConfigurationRows_itemByName.md) | A method that returns the row with the specified name. |

## Properties

| Name | Description |
| --- | --- |
| [count](ConfigurationRows_count.md) | Returns the number of rows in the table where the header row is not included. |
| [isValid](ConfigurationRows_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationRows_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[ConfigurationAppearanceTable.rows](ConfigurationAppearanceTable_rows.md), [ConfigurationCustomThemeTable.rows](ConfigurationCustomThemeTable_rows.md), [ConfigurationMaterialTable.rows](ConfigurationMaterialTable_rows.md), [ConfigurationPlasticRuleTable.rows](ConfigurationPlasticRuleTable_rows.md), [ConfigurationSheetMetalRuleTable.rows](ConfigurationSheetMetalRuleTable_rows.md), [ConfigurationTable.rows](ConfigurationTable_rows.md), [ConfigurationTopTable.rows](ConfigurationTopTable_rows.md)

## Version

Introduced in version January 2024  

