# DocumentReferences.item Method

Parent Object: [DocumentReferences](DocumentReferences.md)  

## Description

Returns the specified DocumentReference.

## Syntax

"documentReferences_var" is a variable referencing a [DocumentReferences](DocumentReferences.md) object.

```python
returnValue = documentReferences_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [DocumentReference](DocumentReference.md) | Returns the specified DocumentReference or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the object to return where the first one in the collection has an index of 0. |

## Version

Introduced in version June 2017  

