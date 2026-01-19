# FlatPatternProduct.createConfiguredDesign Method

Parent Object: [FlatPatternProduct](FlatPatternProduct.md)  

## Description

Converts this design into a configured design. The returned ConfigurationTable has a single row and no columns. You can use it to add columns and rows to define the configuration.

## Syntax

"flatPatternProduct_var" is a variable referencing a [FlatPatternProduct](FlatPatternProduct.md) object.

```python
returnValue = flatPatternProduct_var.createConfiguredDesign()
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationTopTable](ConfigurationTopTable.md) | Returns the ConfigurationTable that defines the configurations for this design. |

## Version

Introduced in version January 2024  

