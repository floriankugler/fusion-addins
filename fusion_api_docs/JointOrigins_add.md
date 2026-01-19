# JointOrigins.add Method

Parent Object: [JointOrigins](JointOrigins.md)  

## Description

Create a new joint origin.

## Syntax

"jointOrigins_var" is a variable referencing a [JointOrigins](JointOrigins.md) object.

```python
returnValue = jointOrigins_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [JointOrigin](JointOrigin.md) | Returns a JointOrigin object if successfully created and null if it fails. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [JointOriginInput](JointOriginInput.md) | A JointOriginInput object that full defines all of the information needed to create a joint origin. You create a JointOriginInput by using the createInput method of the JointOrigins object. |

## Samples

| Name | Description |
|----|----|
| [Joint Origin Between Two Faces Sample](JointOrigin2Planes_Sample.md) | Demonstrates creating a new Joint Origin between two planes. |
| [Joint Origin Sample](JointOriginSample_Sample.md) | Demonstrates creating a new Joint Origin. |

## Version

Introduced in version September 2015  

