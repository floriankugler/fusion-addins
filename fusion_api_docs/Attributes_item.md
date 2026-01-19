# Attributes.item Method

Parent Object: [Attributes](Attributes.md)  

## Description

Returns the specified attribute using an index into the collection.

## Syntax

"attributes_var" is a variable referencing an [Attributes](Attributes.md) object.

```python
returnValue = attributes_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Attribute](Attribute.md) | Returns the specified attribute or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the attribute within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version May 2016  

