# ConfigurationCell Object

Derived from: [Base](Base.md) Object  

## Description

Represents a single cell within a configuration table. This is the base class for the type-specific cell objects.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationCell_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConfigurationCell_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationCell_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentRow](ConfigurationCell_parentRow.md) | Returns the row this cell is in. |

## Accessed From

[ConfigurationAppearanceTable.getCell](ConfigurationAppearanceTable_getCell.md), [ConfigurationCustomThemeTable.getCell](ConfigurationCustomThemeTable_getCell.md), [ConfigurationFeatureAspectColumn.getCell](ConfigurationFeatureAspectColumn_getCell.md), [ConfigurationFeatureAspectColumn.getCellByRowId](ConfigurationFeatureAspectColumn_getCellByRowId.md), [ConfigurationFeatureAspectColumn.getCellByRowName](ConfigurationFeatureAspectColumn_getCellByRowName.md), [ConfigurationJointSnapColumn.getCell](ConfigurationJointSnapColumn_getCell.md), [ConfigurationJointSnapColumn.getCellByRowId](ConfigurationJointSnapColumn_getCellByRowId.md), [ConfigurationJointSnapColumn.getCellByRowName](ConfigurationJointSnapColumn_getCellByRowName.md), [ConfigurationMaterialTable.getCell](ConfigurationMaterialTable_getCell.md), [ConfigurationPlasticRuleTable.getCell](ConfigurationPlasticRuleTable_getCell.md), [ConfigurationRow.getCellByColumnId](ConfigurationRow_getCellByColumnId.md), [ConfigurationRow.getCellByColumnIndex](ConfigurationRow_getCellByColumnIndex.md), [ConfigurationSheetMetalRuleTable.getCell](ConfigurationSheetMetalRuleTable_getCell.md), [ConfigurationTable.getCell](ConfigurationTable_getCell.md), [ConfigurationTopTable.getCell](ConfigurationTopTable_getCell.md)

## Derived Classes

[ConfigurationAppearanceCell](ConfigurationAppearanceCell.md), [ConfigurationFeatureAspectBooleanCell](ConfigurationFeatureAspectBooleanCell.md), [ConfigurationFeatureAspectStringCell](ConfigurationFeatureAspectStringCell.md), [ConfigurationInsertCell](ConfigurationInsertCell.md), [ConfigurationInsertStandardDesignCell](ConfigurationInsertStandardDesignCell.md), [ConfigurationJointSnapCell](ConfigurationJointSnapCell.md), [ConfigurationMaterialCell](ConfigurationMaterialCell.md), [ConfigurationParameterCell](ConfigurationParameterCell.md), [ConfigurationPlasticRuleCell](ConfigurationPlasticRuleCell.md), [ConfigurationPropertyCell](ConfigurationPropertyCell.md), [ConfigurationSheetMetalRuleCell](ConfigurationSheetMetalRuleCell.md), [ConfigurationSuppressCell](ConfigurationSuppressCell.md), [ConfigurationThemeCell](ConfigurationThemeCell.md), [ConfigurationVisibilityCell](ConfigurationVisibilityCell.md)

## Version

Introduced in version January 2024  

