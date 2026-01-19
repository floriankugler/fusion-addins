# ContactSets.add Method

Parent Object: [ContactSets](ContactSets.md)  

## Description

Creates a new contact set for the provided occurrences and/or bodies.

## Syntax

"contactSets_var" is a variable referencing a [ContactSets](ContactSets.md) object.

```python
returnValue = contactSets_var.add(occurrencesAndBodies)
```

## Return Value

| Type | Description |
|----|----|
| [ContactSet](ContactSet.md) | Returns the newly created ContactSet or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrencesAndBodies | Base\[\] | An array of Occurrence or BRepBody objects that will be included in the contact set. All occurrences and bodies must be in the context of the root component. |

## Samples

| Name | Description |
|----|----|
| [SliderJointMotion API Sample](SliderJointMotionSample_Sample.md) | Demonstrates creating a joint with slider joint motion. |

## Version

Introduced in version September 2016  

