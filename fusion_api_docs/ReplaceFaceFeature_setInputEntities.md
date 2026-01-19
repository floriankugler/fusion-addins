# ReplaceFaceFeature.setInputEntities Method

Parent Object: [ReplaceFaceFeature](ReplaceFaceFeature.md)  

## Description

Method that sets faces to replace.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"replaceFaceFeature_var" is a variable referencing a [ReplaceFaceFeature](ReplaceFaceFeature.md) object.

```python
returnValue = replaceFaceFeature_var.setInputEntities(sourceFaces, isTangentChain)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| sourceFaces | [ObjectCollection](ObjectCollection.md) | The collection can contain the faces from a solid and/or from features. All the faces must be on the same body. |
| isTangentChain | boolean | A boolean value for setting whether or not faces that are tangentially connected to the input faces (if any) will also be included. A value of true indicates that tangent faces will be included. |

## Version

Introduced in version March 2015  

