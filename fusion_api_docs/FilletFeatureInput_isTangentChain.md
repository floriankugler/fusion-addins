# FilletFeatureInput.isTangentChain Property

Parent Object: [FilletFeatureInput](FilletFeatureInput.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets if any edges that are tangentially connected to any of filleted edges will also be included in the fillet.

## Remarks

This property is obsolete. You should now use the FilletEdgeSet object to define if the tangency chaining should be used for entities in that edge set.

## Syntax

"filletFeatureInput_var" is a variable referencing a FilletFeatureInput object.  

```python
# Get the value of the property.
propertyValue = filletFeatureInput_var.isTangentChain

# Set the value of the property.
filletFeatureInput_var.isTangentChain = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2014  
Retired in version November 2022  

