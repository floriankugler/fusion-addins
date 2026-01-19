# Analyses.isLightBulbOn Property

Parent Object: [Analyses](Analyses.md)  

## Description

A property that gets and sets if the display is enabled for all Analysis objects in the design. If this is false, all Analysis results will be hidden. If this is true, the Analysis objects whose isLightBulbOn property is also true will be visible.

## Syntax

"analyses_var" is a variable referencing an Analyses object.  

```python
# Get the value of the property.
propertyValue = analyses_var.isLightBulbOn

# Set the value of the property.
analyses_var.isLightBulbOn = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2023  

