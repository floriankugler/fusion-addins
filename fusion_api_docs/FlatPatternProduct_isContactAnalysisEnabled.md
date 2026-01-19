# FlatPatternProduct.isContactAnalysisEnabled Property

Parent Object: [FlatPatternProduct](FlatPatternProduct.md)  

## Description

Gets and sets whether contact analysis is enabled for all components. This is the equivalent of the "Disable Contact / Enable Contact" command. If this if True then any contact analysis defined (either all or contact sets) is enabled. if False, then no contact analysis is performed.

## Syntax

"flatPatternProduct_var" is a variable referencing a FlatPatternProduct object.  

```python
# Get the value of the property.
propertyValue = flatPatternProduct_var.isContactAnalysisEnabled

# Set the value of the property.
flatPatternProduct_var.isContactAnalysisEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version October 2022  

