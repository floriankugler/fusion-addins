# ConfigurationParameterColumn.deleteMe Method

Parent Object: [ConfigurationParameterColumn](ConfigurationParameterColumn.md)  

## Description

Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail.

## Syntax

"configurationParameterColumn_var" is a variable referencing a [ConfigurationParameterColumn](ConfigurationParameterColumn.md) object.

```python
returnValue = configurationParameterColumn_var.deleteMe()
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns true if the deletion was successful. |

## Version

Introduced in version March 2024  

