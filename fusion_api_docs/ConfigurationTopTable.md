# ConfigurationTopTable Object

Derived from: [ConfigurationTable](ConfigurationTable.md) Object  

## Description

API object representing the top configuration table associated with a configured design.  

When obtained from the DataFile object of a configured design, the functionality is limited because it's not loaded in Fusion, and there is no access to the Fusion objects represented in the table. For example, any properties that return a Component or Parameter will return null because those objects aren't available.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationTopTable_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [getCell](ConfigurationTopTable_getCell.md) | Returns the cell at the specified row and column. |
| [moveColumns](ConfigurationTopTable_moveColumns.md) | Moves the specified columns from one table to another. |

## Properties

| Name | Description |
| --- | --- |
| [activeRow](ConfigurationTopTable_activeRow.md) | Returns the row that is currently active. To set the active row, use the activate method on the ConfigurationRow object. |
| [appearanceTable](ConfigurationTopTable_appearanceTable.md) | Returns the appearance table associated with this top table. The returned table can be empty and not have any columns. In this case, the table is not displayed in the user interface. Use the returned table to add columns. |
| [columns](ConfigurationTopTable_columns.md) | Returns the columns defined for this table and provides the functionality to create new columns. |
| [customThemeTables](ConfigurationTopTable_customThemeTables.md) | Returns any custom theme tables associated with this top table. |
| [id](ConfigurationTopTable_id.md) | Returns the unique ID of this table. |
| [isValid](ConfigurationTopTable_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [materialTable](ConfigurationTopTable_materialTable.md) | Returns the material table associated with this top table. The returned table can be empty and not have any columns. In this case, the table is not displayed in the user interface. Use the returned table to add columns. |
| [name](ConfigurationTopTable_name.md) | Gets the name of the table as seen in the user interface. |
| [objectType](ConfigurationTopTable_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [plasticRuleTable](ConfigurationTopTable_plasticRuleTable.md) | Returns the plastic rule table associated with this top table. The returned table can be empty and not have any columns. In this case, the table is not displayed in the user interface. Use the returned table to add columns. |
| [rows](ConfigurationTopTable_rows.md) | Returns the rows (configurations) defined for this table and provides the functionality to create new rows. |
| [sheetMetalRuleTable](ConfigurationTopTable_sheetMetalRuleTable.md) | Returns the sheet metal rule table associated with this top table. The returned table can be empty and not have any columns. In this case, the table is not displayed in the user interface. Use the returned table to add columns. |

## Accessed From

[Design.configurationTopTable](Design_configurationTopTable.md), [Design.createConfiguredDesign](Design_createConfiguredDesign.md), [FlatPatternProduct.configurationTopTable](FlatPatternProduct_configurationTopTable.md), [FlatPatternProduct.createConfiguredDesign](FlatPatternProduct_createConfiguredDesign.md), [WorkingModel.configurationTopTable](WorkingModel_configurationTopTable.md), [WorkingModel.createConfiguredDesign](WorkingModel_createConfiguredDesign.md)

## Version

Introduced in version January 2024  

