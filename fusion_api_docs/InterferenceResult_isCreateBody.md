# InterferenceResult.isCreateBody Property

Parent Object: [InterferenceResult](InterferenceResult.md)  

## Description

Gets and sets if this interference volume should be created as a model body. Setting this to true doesn't create the body just indicates that a body is desired. Calling the createBodies method on the interferenceResults object will result in the creation of the model body if this property is true.

## Syntax

"interferenceResult_var" is a variable referencing an InterferenceResult object.  

```python
# Get the value of the property.
propertyValue = interferenceResult_var.isCreateBody

# Set the value of the property.
interferenceResult_var.isCreateBody = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2015  

