# ConstructionPoints.itemByName Method

Parent Object: [ConstructionPoints](ConstructionPoints.md)  

## Description

Returns the specified construction point using the name of the construction point as it is displayed in the browser.

## Syntax

"constructionPoints_var" is a variable referencing a [ConstructionPoints](ConstructionPoints.md) object.

```python
returnValue = constructionPoints_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [ConstructionPoint](ConstructionPoint.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the construction point as it is displayed in the browser. |

## Version

Introduced in version August 2014  

