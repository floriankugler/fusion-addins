# WorkingModel.computeAll Method

Parent Object: [WorkingModel](WorkingModel.md)  

## Description

Forces a recompute of the entire design. This is the equivalent of the "Compute All" command.

## Syntax

"workingModel_var" is a variable referencing a [WorkingModel](WorkingModel.md) object.

```python
returnValue = workingModel_var.computeAll()
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the compute completed. This doesn't indicate if all the items in the timeline successfully computed or not. You need to check the health state of each item in the timeline to determine if everything successfully computed or not. |

## Version

Introduced in version January 2024  

