# FloatProperty.isPercentage Property

Parent Object: [FloatProperty](FloatProperty.md)  

## Description

Gets the boolean flag that indicates that this property represents a percentage value so the valid values must be in the range of 0.0 to 1.0 unless they’re further limited by additional limits which can be determined with the HasLimits property.  

This is most commonly used for properties associated with materials and appearances.

## Syntax

"floatProperty_var" is a variable referencing a FloatProperty object.  

```python
# Get the value of the property.
propertyValue = floatProperty_var.isPercentage
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version August 2014  

