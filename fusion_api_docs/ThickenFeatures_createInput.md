# ThickenFeatures.createInput Method

Parent Object: [ThickenFeatures](ThickenFeatures.md)  

## Description

Creates a ThickenFeatureInput object. Use properties and methods on this object to define the Thicken feature you want to create and then use the Add method, passing in the ThickenFeatureInput object to create the feature.

## Syntax

"thickenFeatures_var" is a variable referencing a [ThickenFeatures](ThickenFeatures.md) object.

```python
# Uses no optional arguments.
returnValue = thickenFeatures_var.createInput(inputFaces, thickness, isSymmetric, operation)

# Uses optional arguments.
returnValue = thickenFeatures_var.createInput(inputFaces, thickness, isSymmetric, operation, isChainSelection)
```

## Return Value

| Type | Description |
|----|----|
| [ThickenFeatureInput](ThickenFeatureInput.md) | Returns the newly created ThickenFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| inputFaces | [ObjectCollection](ObjectCollection.md) | The faces or patch bodies to thicken. Faces need not be from the same component or body, nor do they need to be connected or touching one another. |
| thickness | [ValueInput](ValueInput.md) | ValueInput object that defines the thickness. |
| isSymmetric | boolean | A boolean value for setting whether to add thickness symmetrically or only on one side of the face/s to thicken |
| operation | [FeatureOperations](FeatureOperations.md) | The feature operation to perform. |
| isChainSelection | boolean | A boolean value for setting whether or not faces that are tangentially connected to the input faces (if any) will be included in the thicken. The default value is true. This is an optional argument whose default value is True. |

## Samples

| Name | Description |
|----|----|
| [thickenFeatures.add](thickenFeatures_add_Sample.md) | Demonstrates the thickenFeatures.add method. |
| [Thicken Feature API Sample](ThickenFeatureSample_Sample.md) | Demonstrates creating a new thiken feature. |

## Version

Introduced in version June 2015  

