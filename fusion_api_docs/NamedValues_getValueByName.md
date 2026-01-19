# NamedValues.getValueByName Method

Parent Object: [NamedValues](NamedValues.md)  

## Description

Function that returns the ValueInput object of a name value pair by specifying its name

## Syntax

"namedValues_var" is a variable referencing a [NamedValues](NamedValues.md) object.  

```python
(returnValue, value) = namedValues_var.getValueByName(name)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the name value pair to return the ValueInput object from |
| value | [ValueInput](ValueInput.md) | The ValueInput object |

## Version

Introduced in version August 2014  

