# ParameterList.removeByItem Method

Parent Object: [ParameterList](ParameterList.md)  

## Description

Method that removes a parameter from the list by specifying the parameter (item) to remove

## Syntax

"parameterList_var" is a variable referencing a [ParameterList](ParameterList.md) object.

```python
returnValue = parameterList_var.removeByItem(item)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if successful. This method will fail if the list is read-only |

## Parameters

| Name | Type                       | Description                                |
|------|----------------------------|--------------------------------------------|
| item | [Parameter](Parameter.md) | The parameter item to remove from the list |

## Version

Introduced in version August 2014  

