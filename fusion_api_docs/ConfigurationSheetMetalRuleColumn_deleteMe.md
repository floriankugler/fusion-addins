# ConfigurationSheetMetalRuleColumn.deleteMe Method

Parent Object: [ConfigurationSheetMetalRuleColumn](ConfigurationSheetMetalRuleColumn.md)  

## Description

Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail.

## Syntax

"configurationSheetMetalRuleColumn_var" is a variable referencing a [ConfigurationSheetMetalRuleColumn](ConfigurationSheetMetalRuleColumn.md) object.

```python
returnValue = configurationSheetMetalRuleColumn_var.deleteMe()
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns true if the deletion was successful. |

## Version

Introduced in version March 2024  

