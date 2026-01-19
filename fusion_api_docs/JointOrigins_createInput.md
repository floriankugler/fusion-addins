# JointOrigins.createInput Method

Parent Object: [JointOrigins](JointOrigins.md)  

## Description

Creates a JointOriginInput object which is used to collect all of the information needed to create a simple joint origin. The creation of the input object takes the required input as the geometry argument and you can optionally use methods and properties on the created JointOriginInput to set other optional settings. The JointOrigin is created by calling the add method of the JointOrigins object and passing it the JointOriginInput object.

## Syntax

"jointOrigins_var" is a variable referencing a [JointOrigins](JointOrigins.md) object.

```python
returnValue = jointOrigins_var.createInput(geometry)
```

## Return Value

| Type | Description |
|----|----|
| [JointOriginInput](JointOriginInput.md) | Returns a JointOriginInput object if successfully created and null if it fails. |

## Parameters

| Name | Type | Description |
|----|----|----|
| geometry | [JointGeometry](JointGeometry.md) | A JointGeometry object that defines the geometry the joint origin will be created on. |

## Samples

| Name | Description |
|----|----|
| [Joint Origin Between Two Faces Sample](JointOrigin2Planes_Sample.md) | Demonstrates creating a new Joint Origin between two planes. |
| [Joint Origin Sample](JointOriginSample_Sample.md) | Demonstrates creating a new Joint Origin. |

## Version

Introduced in version September 2015  

