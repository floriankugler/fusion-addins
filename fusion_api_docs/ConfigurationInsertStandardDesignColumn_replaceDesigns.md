# ConfigurationInsertStandardDesignColumn.replaceDesigns Property

Parent Object: [ConfigurationInsertStandardDesignColumn](ConfigurationInsertStandardDesignColumn.md)  

## Description

Provides access to the list of replace designs that have been defined for this column. Using the returned collection you can define new ConfigurationReplaceDesign objects. Use the cells in the column to specify which one of the defined replace designs is used for a specific row.

## Syntax

"configurationInsertStandardDesignColumn_var" is a variable referencing a ConfigurationInsertStandardDesignColumn object.  

```python
# Get the value of the property.
propertyValue = configurationInsertStandardDesignColumn_var.replaceDesigns
```

## Property Value

This is a read only property whose value is a [ConfigurationReplaceDesigns](ConfigurationReplaceDesigns.md).

## Version

Introduced in version September 2025  

