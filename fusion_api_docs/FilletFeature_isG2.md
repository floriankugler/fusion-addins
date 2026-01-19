# FilletFeature.isG2 Property

Parent Object: [FilletFeature](FilletFeature.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets if the fillet uses the G2 (curvature-continuity) surface quality option.

## Remarks

This property is obsolete. You should now use the continuity property on the FilletEdgeSet object to control the continuity.

## Syntax

"filletFeature_var" is a variable referencing a FilletFeature object.  

```python
# Get the value of the property.
propertyValue = filletFeature_var.isG2

# Set the value of the property.
filletFeature_var.isG2 = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2014  
Retired in version November 2022  

