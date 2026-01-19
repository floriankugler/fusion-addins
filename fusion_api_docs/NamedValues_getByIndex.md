# NamedValues.getByIndex Method

Parent Object: [NamedValues](NamedValues.md)  

## Description

Function that returns the name and ValueInput object of a name value pair by specifying an index number

## Syntax

"namedValues_var" is a variable referencing a [NamedValues](NamedValues.md) object.  

```python
(returnValue, name, value) = namedValues_var.getByIndex(index)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | integer | The index of the name value pair to return. The first pair in the collection has an index of 0. |
| name | string | The name |
| value | [ValueInput](ValueInput.md) | The ValueInput object |

## Version

Introduced in version August 2014  

