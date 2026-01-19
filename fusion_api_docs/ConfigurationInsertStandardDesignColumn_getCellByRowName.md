# ConfigurationInsertStandardDesignColumn.getCellByRowName Method

Parent Object: [ConfigurationInsertStandardDesignColumn](ConfigurationInsertStandardDesignColumn.md)  

## Description

Gets the cell in this column at the row specified by its name.

## Syntax

"configurationInsertStandardDesignColumn_var" is a variable referencing a [ConfigurationInsertStandardDesignColumn](ConfigurationInsertStandardDesignColumn.md) object.

```python
returnValue = configurationInsertStandardDesignColumn_var.getCellByRowName(rowName)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationInsertStandardDesignCell](ConfigurationInsertStandardDesignCell.md) | Returns the specified cell if successful and null if the name is not found. |

## Parameters

| Name    | Type   | Description                                 |
|---------|--------|---------------------------------------------|
| rowName | string | The name of the row to return the cell for. |

## Version

Introduced in version September 2025  

