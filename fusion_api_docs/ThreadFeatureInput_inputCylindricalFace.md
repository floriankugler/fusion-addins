# ThreadFeatureInput.inputCylindricalFace Property

Parent Object: [ThreadFeatureInput](ThreadFeatureInput.md)  

## Description

Gets and sets the threaded face. In the case where there are multiple faces, only the first one is returned. Setting this results in a thread being applied to only a single face. It is recommended that you use the inputCylindricalfaces property in order to have full access to the collection of faces to be threaded.

## Syntax

"threadFeatureInput_var" is a variable referencing a ThreadFeatureInput object.  

```python
# Get the value of the property.
propertyValue = threadFeatureInput_var.inputCylindricalFace

# Set the value of the property.
threadFeatureInput_var.inputCylindricalFace = propertyValue
```

## Property Value

This is a read/write property whose value is a [BRepFace](BRepFace.md).

## Version

Introduced in version November 2015  

