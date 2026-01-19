# Products.item Method

Parent Object: [Products](Products.md)  

## Description

Function that returns the specified product using an index into the collection.

## Syntax

"products_var" is a variable referencing a [Products](Products.md) object.

```python
returnValue = products_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Product](Product.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

