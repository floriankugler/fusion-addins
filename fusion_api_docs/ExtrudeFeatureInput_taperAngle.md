# ExtrudeFeatureInput.taperAngle Property

Parent Object: [ExtrudeFeatureInput](ExtrudeFeatureInput.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets the taper angle of the extrusion. This is used to define the taper angle for a single sided and symmetric and defines the angle for side one of a two sided extrusion. This property is initialized with a taper angle of zero. A negative angle will taper the extrusion inward while a positive value will taper the extrusion outward. This property is valid for both parametric and non-parametric extrusions.

## Remarks

This property has been retired and is replaced by getting the extent definition for each direction and using it to set the taper angle.

## Syntax

"extrudeFeatureInput_var" is a variable referencing an ExtrudeFeatureInput object.  

```python
# Get the value of the property.
propertyValue = extrudeFeatureInput_var.taperAngle

# Set the value of the property.
extrudeFeatureInput_var.taperAngle = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version August 2014  
Retired in version November 2016  

