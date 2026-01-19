# ParameterList.find Method

Parent Object: [ParameterList](ParameterList.md)  

## Description

Finds the specified parameter in the list. The search can be started at a specified index rather than from the beginning of the list. If not found, -1 is returned.

## Syntax

"parameterList_var" is a variable referencing a [ParameterList](ParameterList.md) object.

```python
# Uses no optional arguments.
returnValue = parameterList_var.find(parameter)

# Uses optional arguments.
returnValue = parameterList_var.find(parameter, startIndex)
```

## Return Value

| Type    | Description                                           |
|---------|-------------------------------------------------------|
| integer | Returns the index of the parameter found in the list. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| parameter | [Parameter](Parameter.md) | The parameter to find |
| startIndex | uinteger | the index in the list to start the search from This is an optional argument whose default value is 0. |

## Version

Introduced in version August 2014  

