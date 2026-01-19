# ShellFeature.setInputEntities Method

Parent Object: [ShellFeature](ShellFeature.md)  

## Description

Method that sets faces to remove and bodies to preform shell. Return false if any faces are input, and the owning bodies of the faces are also input.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"shellFeature_var" is a variable referencing a [ShellFeature](ShellFeature.md) object.

```python
# Uses no optional arguments.
returnValue = shellFeature_var.setInputEntities(inputEntities)

# Uses optional arguments.
returnValue = shellFeature_var.setInputEntities(inputEntities, isTangentChain)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| inputEntities | [ObjectCollection](ObjectCollection.md) | The collection contains the faces to remove and the bodies to perform shell. Fails if any faces are input, and the owning bodies of the faces are also input. |
| isTangentChain | boolean | A boolean value for setting whether or not faces that are tangentially connected to the input faces (if any) will also be included. It defaults to true. This is an optional argument whose default value is True. |

## Version

Introduced in version November 2014  

