# WorkingModel.createConfiguredDesign Method

Parent Object: [WorkingModel](WorkingModel.md)  

## Description

Converts this design into a configured design. The returned ConfigurationTable has a single row and no columns. You can use it to add columns and rows to define the configuration.

## Syntax

"workingModel_var" is a variable referencing a [WorkingModel](WorkingModel.md) object.

```python
returnValue = workingModel_var.createConfiguredDesign()
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationTopTable](ConfigurationTopTable.md) | Returns the ConfigurationTable that defines the configurations for this design. |

## Version

Introduced in version January 2024  

