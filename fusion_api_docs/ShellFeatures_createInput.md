# ShellFeatures.createInput Method

Parent Object: [ShellFeatures](ShellFeatures.md)  

## Description

Creates a ShellFeatureInput object. Use properties and methods on this object to define the shell you want to create and then use the Add method, passing in the ShellFeatureInput object.

## Syntax

"shellFeatures_var" is a variable referencing a [ShellFeatures](ShellFeatures.md) object.

```python
# Uses no optional arguments.
returnValue = shellFeatures_var.createInput(inputEntities)

# Uses optional arguments.
returnValue = shellFeatures_var.createInput(inputEntities, isTangentChain)
```

## Return Value

| Type | Description |
|----|----|
| [ShellFeatureInput](ShellFeatureInput.md) | Returns the newly created ShellFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| inputEntities | [ObjectCollection](ObjectCollection.md) | The collection contains the faces to remove and the bodies to perform shell. Fails if any faces are input, and the owning bodies of the faces are also input. |
| isTangentChain | boolean | A boolean value for setting whether or not faces that are tangentially connected to the input faces (if any) will also be included. It defaults to true. This is an optional argument whose default value is True. |

## Samples

| Name | Description |
|----|----|
| [shellFeatures.add](shelFeatures_add_Sample.md) | Demonstrates creating a shell feature. |
| [Shell Feature API Sample](ShellFeatureSample_Sample.md) | Demonstrates creating a new shell feature. |

## Version

Introduced in version November 2014  

