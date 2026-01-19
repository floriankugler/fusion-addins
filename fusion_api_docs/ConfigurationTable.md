# ConfigurationTable Object

Derived from: [Base](Base.md) Object  

## Description

The base class of all configuration tables.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationTable_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [getCell](ConfigurationTable_getCell.md) | Returns the cell at the specified row and column. |

## Properties

| Name | Description |
| --- | --- |
| [id](ConfigurationTable_id.md) | Returns the unique ID of this table. |
| [isValid](ConfigurationTable_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationTable_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [rows](ConfigurationTable_rows.md) | Returns the rows (configurations) defined for this table and provides the functionality to create new rows. |

## Accessed From

[ConfigurationFeatureAspectColumn.parentTable](ConfigurationFeatureAspectColumn_parentTable.md), [ConfigurationInsertColumn.parentTable](ConfigurationInsertColumn_parentTable.md), [ConfigurationInsertStandardDesignColumn.parentTable](ConfigurationInsertStandardDesignColumn_parentTable.md), [ConfigurationJointSnapColumn.parentTable](ConfigurationJointSnapColumn_parentTable.md), [ConfigurationParameterColumn.parentTable](ConfigurationParameterColumn_parentTable.md), [ConfigurationPropertyColumn.parentTable](ConfigurationPropertyColumn_parentTable.md), [ConfigurationRow.parentTable](ConfigurationRow_parentTable.md), [ConfigurationSuppressColumn.parentTable](ConfigurationSuppressColumn_parentTable.md), [ConfigurationThemeColumn.parentTable](ConfigurationThemeColumn_parentTable.md), [ConfigurationThemeColumn.referencedTable](ConfigurationThemeColumn_referencedTable.md), [ConfigurationVisibilityColumn.parentTable](ConfigurationVisibilityColumn_parentTable.md)

## Derived Classes

[ConfigurationAppearanceTable](ConfigurationAppearanceTable.md), [ConfigurationCustomThemeTable](ConfigurationCustomThemeTable.md), [ConfigurationMaterialTable](ConfigurationMaterialTable.md), [ConfigurationPlasticRuleTable](ConfigurationPlasticRuleTable.md), [ConfigurationSheetMetalRuleTable](ConfigurationSheetMetalRuleTable.md), [ConfigurationTopTable](ConfigurationTopTable.md)

## Version

Introduced in version January 2024  

