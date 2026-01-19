# FlatPatternProduct.isContactSetAnalysis Property

Parent Object: [FlatPatternProduct](FlatPatternProduct.md)  

## Description

Gets and sets whether contact analysis is done using contact sets or between all bodies, independent of any contact sets. If True and the isContactAnalysisEnabled property is True then contact analysis is performed using contact sets. If False and isContactAnalysisEnabled is True, then contact analysis is performed between all bodies. If isContactAnalysisEnabled is False then no contact analysis is performed.

## Syntax

"flatPatternProduct_var" is a variable referencing a FlatPatternProduct object.  

```python
# Get the value of the property.
propertyValue = flatPatternProduct_var.isContactSetAnalysis

# Set the value of the property.
flatPatternProduct_var.isContactSetAnalysis = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version October 2022  

