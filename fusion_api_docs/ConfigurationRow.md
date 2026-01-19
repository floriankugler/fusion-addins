# ConfigurationRow Object

Derived from: [Base](Base.md) Object  

## Description

Represents a row in a configuration table. The header row is not considered a standard row but is information associated with each column.  

For a top table, each row represents a configuration, and for a theme table, each row represents a theme.

## Methods

| Name | Description |
|----|----|
| [activate](ConfigurationRow_activate.md) | Causes this row to become the active row in the table. |
| [classType](ConfigurationRow_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](ConfigurationRow_copy.md) | Creates a new row by copying this row. |
| [deleteMe](ConfigurationRow_deleteMe.md) | Deletes this row from the table. The first row of the top table cannot be deleted, and this method will fail. |
| [generate](ConfigurationRow_generate.md) | Causes this row to be generated. |
| [getCellByColumnId](ConfigurationRow_getCellByColumnId.md) | Gets the cell in this row at the column with the specified ID. |
| [getCellByColumnIndex](ConfigurationRow_getCellByColumnIndex.md) | Gets the cell in this row at the specified column index. The first column has an index of 0 and does not include the name column. |

## Properties

| Name | Description |
| --- | --- |
| [id](ConfigurationRow_id.md) | Gets the unique ID that identifies this row. The ID remains constant for this row as long as the row exists. This is different than the name, which the user can change. |
| [index](ConfigurationRow_index.md) | The index position of this row within the table. The first row is at index 0 and does not include the header row. |
| [isValid](ConfigurationRow_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](ConfigurationRow_name.md) | Gets and sets the name of this row. Names must be unique with respect to other rows in this table. If you specify a name that exists, Fusion will append a counter to ensure uniqueness. For example, if "Small" is already used and you name another row "Small", you will end up with "Small (1)". |
| [objectType](ConfigurationRow_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentTable](ConfigurationRow_parentTable.md) | Returns the configuration table this row is a member of. |

## Accessed From

[ConfigurationAppearanceCell.parentRow](ConfigurationAppearanceCell_parentRow.md), [ConfigurationCell.parentRow](ConfigurationCell_parentRow.md), [ConfigurationFeatureAspectBooleanCell.parentRow](ConfigurationFeatureAspectBooleanCell_parentRow.md), [ConfigurationFeatureAspectStringCell.parentRow](ConfigurationFeatureAspectStringCell_parentRow.md), [ConfigurationInsertCell.parentRow](ConfigurationInsertCell_parentRow.md), [ConfigurationInsertCell.row](ConfigurationInsertCell_row.md), [ConfigurationInsertStandardDesignCell.parentRow](ConfigurationInsertStandardDesignCell_parentRow.md), [ConfigurationJointSnapCell.parentRow](ConfigurationJointSnapCell_parentRow.md), [ConfigurationMaterialCell.parentRow](ConfigurationMaterialCell_parentRow.md), [ConfigurationParameterCell.parentRow](ConfigurationParameterCell_parentRow.md), [ConfigurationPlasticRuleCell.parentRow](ConfigurationPlasticRuleCell_parentRow.md), [ConfigurationPropertyCell.parentRow](ConfigurationPropertyCell_parentRow.md), [ConfigurationRow.copy](ConfigurationRow_copy.md), [ConfigurationRows.add](ConfigurationRows_add.md), [ConfigurationRows.item](ConfigurationRows_item.md), [ConfigurationRows.itemById](ConfigurationRows_itemById.md), [ConfigurationRows.itemByName](ConfigurationRows_itemByName.md), [ConfigurationSheetMetalRuleCell.parentRow](ConfigurationSheetMetalRuleCell_parentRow.md), [ConfigurationSuppressCell.parentRow](ConfigurationSuppressCell_parentRow.md), [ConfigurationThemeCell.parentRow](ConfigurationThemeCell_parentRow.md), [ConfigurationThemeCell.referencedTableRow](ConfigurationThemeCell_referencedTableRow.md), [ConfigurationTopTable.activeRow](ConfigurationTopTable_activeRow.md), [ConfigurationVisibilityCell.parentRow](ConfigurationVisibilityCell_parentRow.md), [Occurrence.configurationRow](Occurrence_configurationRow.md)

## Version

Introduced in version January 2024  

