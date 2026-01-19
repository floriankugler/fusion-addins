# FeatureList.item Method

Parent Object: [FeatureList](FeatureList.md)  

## Description

Returns the specified folder.

## Syntax

"featureList_var" is a variable referencing a [FeatureList](FeatureList.md) object.

```python
returnValue = featureList_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Feature](Feature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the feature to return. The first feature in the list has an index of 0. |

## Version

Introduced in version November 2014  

