# Design.deleteEntities Method

Parent Object: [Design](Design.md)  

## Description

Deletes the specified set of entities that are associated with this product.

## Syntax

"design_var" is a variable referencing a [Design](Design.md) object.

```python
returnValue = design_var.deleteEntities(entities)
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

