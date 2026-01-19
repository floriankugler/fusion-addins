# FlatPatternProduct.designType Property

Parent Object: [FlatPatternProduct](FlatPatternProduct.md)  

## Description

Gets and sets the current design type (DirectDesignType or ParametricDesignType) Changing an existing design from ParametricDesignType to DirectDesignType will result in the timeline and all design history being removed and further operations will not be captured in the timeline.

## Syntax

"flatPatternProduct_var" is a variable referencing a FlatPatternProduct object.  

```python
# Get the value of the property.
propertyValue = flatPatternProduct_var.designType

# Set the value of the property.
flatPatternProduct_var.designType = propertyValue
```

## Property Value

This is a read/write property whose value is a [DesignTypes](DesignTypes.md).

## Version

Introduced in version October 2022  

