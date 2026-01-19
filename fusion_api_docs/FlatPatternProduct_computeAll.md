# FlatPatternProduct.computeAll Method

Parent Object: [FlatPatternProduct](FlatPatternProduct.md)  

## Description

Forces a recompute of the entire design. This is the equivalent of the "Compute All" command.

## Syntax

"flatPatternProduct_var" is a variable referencing a [FlatPatternProduct](FlatPatternProduct.md) object.

```python
returnValue = flatPatternProduct_var.computeAll()
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the compute completed. This doesn't indicate if all the items in the timeline successfully computed or not. You need to check the health state of each item in the timeline to determine if everything successfully computed or not. |

## Version

Introduced in version October 2022  

