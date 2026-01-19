# FilletFeatureInput.isG2 Property

Parent Object: [FilletFeatureInput](FilletFeatureInput.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets if the fillet uses the G2 (curvature-continuity) surface quality option.

## Remarks

This property is obsolete. You should now use the continuity property on the EdgeSetInput object to control the continuity. define new fillets.

## Syntax

"filletFeatureInput_var" is a variable referencing a FilletFeatureInput object.  

```python
# Get the value of the property.
propertyValue = filletFeatureInput_var.isG2

# Set the value of the property.
filletFeatureInput_var.isG2 = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2014  
Retired in version November 2022  

