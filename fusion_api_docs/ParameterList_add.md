# ParameterList.add Method

Parent Object: [ParameterList](ParameterList.md)  

## Description

Adds a parameter to the list. This does not create a new parameter, it adds an existing parameter to the list. Note that duplicates can exist in the list.

## Syntax

"parameterList_var" is a variable referencing a [ParameterList](ParameterList.md) object.

```python
returnValue = parameterList_var.add(parameter)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if successful. This method will fail if the list is read-only |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameter | [Parameter](Parameter.md) | The existing parameter to add to the list |

## Version

Introduced in version August 2014  

