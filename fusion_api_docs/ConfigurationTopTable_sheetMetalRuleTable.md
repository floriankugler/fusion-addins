# ConfigurationTopTable.sheetMetalRuleTable Property

Parent Object: [ConfigurationTopTable](ConfigurationTopTable.md)  

## Description

Returns the sheet metal rule table associated with this top table. The returned table can be empty and not have any columns. In this case, the table is not displayed in the user interface. Use the returned table to add columns.

## Syntax

"configurationTopTable_var" is a variable referencing a ConfigurationTopTable object.  

```python
# Get the value of the property.
propertyValue = configurationTopTable_var.sheetMetalRuleTable
```

## Property Value

This is a read only property whose value is a [ConfigurationSheetMetalRuleTable](ConfigurationSheetMetalRuleTable.md).

## Version

Introduced in version January 2024  

