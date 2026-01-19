# ConstructionAxes.itemByName Method

Parent Object: [ConstructionAxes](ConstructionAxes.md)  

## Description

Returns the specified construction axis using the name of the construction axis as it is displayed in the browser.

## Syntax

"constructionAxes_var" is a variable referencing a [ConstructionAxes](ConstructionAxes.md) object.

```python
returnValue = constructionAxes_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [ConstructionAxis](ConstructionAxis.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type   | Description                                            |
|------|--------|--------------------------------------------------------|
| name | string | The name of the axis as it is displayed in the browser |

## Version

Introduced in version August 2014  

