# ParameterList.removeByIndex Method

Parent Object: [ParameterList](ParameterList.md)  

## Description

Method that removes a parameter from the list using the index of the item in the list Will fail if the list is read only.

## Syntax

"parameterList_var" is a variable referencing a [ParameterList](ParameterList.md) object.

```python
returnValue = parameterList_var.removeByIndex(index)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if successful. This method will fail if the list is read-only |

## Parameters

| Name  | Type     | Description                                            |
|-------|----------|--------------------------------------------------------|
| index | uinteger | The index of the parameter to be removed from the list |

## Version

Introduced in version August 2014  

