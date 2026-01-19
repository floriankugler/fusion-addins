# LoftSections.item Method

Parent Object: [LoftSections](LoftSections.md)  

## Description

Function that returns the specified LoftSection using an index into the collection. They are returned in the same order that they are used in the loft. Their order can be modified using the reorder method of the LoftSection object.

## Syntax

"loftSections_var" is a variable referencing a [LoftSections](LoftSections.md) object.

```python
returnValue = loftSections_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [LoftSection](LoftSection.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | integer | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2016  

