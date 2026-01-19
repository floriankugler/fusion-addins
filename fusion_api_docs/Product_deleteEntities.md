# Product.deleteEntities Method

Parent Object: [Product](Product.md)  

## Description

Deletes the specified set of entities that are associated with this product.

## Syntax

"product_var" is a variable referencing a [Product](Product.md) object.

```python
returnValue = product_var.deleteEntities(entities)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns True if any of the entities provided in the list were deleted. If entities were specified that can't be deleted or aren't owned by this product, they are ignored. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entities | [ObjectCollection](ObjectCollection.md) | An ObjectCollection containing the list of entities to delete. |

## Version

Introduced in version January 2017  

