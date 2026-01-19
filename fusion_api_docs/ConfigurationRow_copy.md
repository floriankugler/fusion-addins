# ConfigurationRow.copy Method

Parent Object: [ConfigurationRow](ConfigurationRow.md)  

## Description

Creates a new row by copying this row.

## Syntax

"configurationRow_var" is a variable referencing a [ConfigurationRow](ConfigurationRow.md) object.

```python
returnValue = configurationRow_var.copy(name)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationRow](ConfigurationRow.md) | Returns the newly created row or null in the case of failure. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| name | string | The name to use for the new row. An empty string indicates that Fusion should use the default naming scheme. Names must be unique with respect to other rows in this table. If you specify a name that exists, Fusion will append a counter to ensure uniqueness. For example, if "Small" is already used and you name another row "Small", you will end up with "Small (1)". |

## Version

Introduced in version March 2024  

