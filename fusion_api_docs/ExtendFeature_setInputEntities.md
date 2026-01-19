# ExtendFeature.setInputEntities Method

Parent Object: [ExtendFeature](ExtendFeature.md)  

## Description

Sets the edges for the extend feature.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"extendFeature_var" is a variable referencing an [ExtendFeature](ExtendFeature.md) object.

```python
# Uses no optional arguments.
returnValue = extendFeature_var.setInputEntities(edges)

# Uses optional arguments.
returnValue = extendFeature_var.setInputEntities(edges, isChainingEnabled)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| edges | [ObjectCollection](ObjectCollection.md) | The surface edges to extend. Only the surface edges from an open body can be extended. The edges must all be from the same open body. |
| isChainingEnabled | boolean | An optional boolean argument whose default is true. If this argument is set to true, all edges that are tangent or curvature continuous, and end point connected, will be found automatically and extended. This is an optional argument whose default value is True. |

## Version

Introduced in version June 2015  

