# SheetMetalRule.twoBendReliefShape Property

Parent Object: [SheetMetalRule](SheetMetalRule.md)  

## Description

Gets and sets the relief shape to use when two bends intersect.  

When set to square or round relief shape, the value of the twoBendReliefPlacement property will be set to IntersectionTwoBendReliefPlacement. For a round relief shape you can change the twoBendReliefPlacment property to TangentTwoBendReliefPlacement.

## Syntax

"sheetMetalRule_var" is a variable referencing a SheetMetalRule object.  

```python
# Get the value of the property.
propertyValue = sheetMetalRule_var.twoBendReliefShape

# Set the value of the property.
sheetMetalRule_var.twoBendReliefShape = propertyValue
```

## Property Value

This is a read/write property whose value is a [TwoBendReliefShapes](TwoBendReliefShapes.md).

## Version

Introduced in version November 2022  

