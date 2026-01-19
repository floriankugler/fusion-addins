# FromEntityStartDefinition.create Method

Parent Object: [FromEntityStartDefinition](FromEntityStartDefinition.md)  

## Description

Statically creates a new FromEntityStartDefinition object. This is used as input when create a new feature and defining the starting condition.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.FromEntityStartDefinition.create(entity, offset)
```

## Return Value

| Type | Description |
|----|----|
| [FromEntityStartDefinition](FromEntityStartDefinition.md) | Returns the newly created FromEntityStartDefinition or null in the case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entity | [Base](Base.md) | An input construction plane or face that defines the start of the feature. If a face is specified it must be large enough to completely contain the projected profile. |
| offset | [ValueInput](ValueInput.md) | An input ValueInput objects that defines the offset distance from the specified entity. The offset can be positive or negative. A positive value indicates an offset in the same direction as the positive normal direction of the face. |

## Samples

| Name | Description |
|----|----|
| [Extrude Feature API Sample](ExtrudeFeatureSample_Sample.md) | Demonstrates creating a new extrude feature. |

## Version

Introduced in version November 2016  

