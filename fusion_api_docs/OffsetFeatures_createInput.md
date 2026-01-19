# OffsetFeatures.createInput Method

Parent Object: [OffsetFeatures](OffsetFeatures.md)  

## Description

Creates an OffsetFeatureInput object. Use properties and methods on this object to define the offset feature you want to create and then use the Add method, passing in the OffsetFeatureInput object to create the feature.

## Syntax

"offsetFeatures_var" is a variable referencing an [OffsetFeatures](OffsetFeatures.md) object.

```python
# Uses no optional arguments.
returnValue = offsetFeatures_var.createInput(entities, distance, operation)

# Uses optional arguments.
returnValue = offsetFeatures_var.createInput(entities, distance, operation, isChainSelection)
```

## Return Value

| Type | Description |
|----|----|
| [OffsetFeatureInput](OffsetFeatureInput.md) | Returns the newly created OffsetFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| entities | [ObjectCollection](ObjectCollection.md) | An ObjectCollection containing the BRepFace objects to offset. Additional faces may be automatically used depending on the value of the isChainSelection argument. Input faces need not be from the same body. |
| distance | [ValueInput](ValueInput.md) | ValueInput object that defines the offset distance. A positive value is in the positive normal direction of the face being offset. |
| operation | [FeatureOperations](FeatureOperations.md) | The feature operation to perform. 'NewBodyFeatureOperation' and 'NewComponentFeatureOperation' are the options supported. |
| isChainSelection | boolean | A boolean value for setting whether or not faces that are tangentially connected to the input faces (if any) will be included in the offset. The default value is true. This is an optional argument whose default value is True. |

## Samples

| Name | Description |
|----|----|
| [offsetFeatures.add](offsetFeatures_add_Sample.md) | Demonstrates the offsetFeatures.add method. This is the equivalent of the Offset command in the SURFACE tab. |
| [Offset Feature API Sample](OffsetFeatureSample_Sample.md) | Demonstrates creating a new offset feature |

## Version

Introduced in version June 2015  

