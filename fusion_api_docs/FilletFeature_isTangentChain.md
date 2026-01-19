# FilletFeature.isTangentChain Property

Parent Object: [FilletFeature](FilletFeature.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets whether or not edges that are tangentially connected to the input edges (if any) will also be filleted.

## Remarks

This property is obsolete. You should now use the isTangentChain property on the FilletEdgeSet object.

## Syntax

"filletFeature_var" is a variable referencing a FilletFeature object.  

```python
# Get the value of the property.
propertyValue = filletFeature_var.isTangentChain

# Set the value of the property.
filletFeature_var.isTangentChain = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version March 2021  
Retired in version November 2022  

