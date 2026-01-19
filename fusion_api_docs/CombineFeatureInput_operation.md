# CombineFeatureInput.operation Property

Parent Object: [CombineFeatureInput](CombineFeatureInput.md)  

## Description

Gets and sets the type of operation performed by the combine. The valid values are JoinFeatureOperation, CutFeatureOperation and IntersectFeatureOperation. The default value is JoinFeatureOperation.

## Syntax

"combineFeatureInput_var" is a variable referencing a CombineFeatureInput object.  

```python
# Get the value of the property.
propertyValue = combineFeatureInput_var.operation

# Set the value of the property.
combineFeatureInput_var.operation = propertyValue
```

## Property Value

This is a read/write property whose value is a [FeatureOperations](FeatureOperations.md).

## Samples

| Name | Description |
|----|----|
| [combineFeatures.add](combineFeatures_add_Sample.md) | Demonstrates the combineFeatures.add method. To use this sample, have a design open that contains at least two bodies. When you run the sample, you will be prompted to select the bodies and they will joined. |

## Version

Introduced in version November 2014  

