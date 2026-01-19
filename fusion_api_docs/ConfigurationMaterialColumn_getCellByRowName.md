# ConfigurationMaterialColumn.getCellByRowName Method

Parent Object: [ConfigurationMaterialColumn](ConfigurationMaterialColumn.md)  

## Description

Gets the cell in this column at the row specified by its name.

## Syntax

"configurationMaterialColumn_var" is a variable referencing a [ConfigurationMaterialColumn](ConfigurationMaterialColumn.md) object.

```python
returnValue = configurationMaterialColumn_var.getCellByRowName(rowName)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationMaterialCell](ConfigurationMaterialCell.md) | Returns the specified cell if successful and null if the name is not found. |

## Parameters

| Name    | Type   | Description                                 |
|---------|--------|---------------------------------------------|
| rowName | string | The name of the row to return the cell for. |

## Version

Introduced in version January 2024  

