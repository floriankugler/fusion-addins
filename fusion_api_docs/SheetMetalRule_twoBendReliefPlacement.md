# SheetMetalRule.twoBendReliefPlacement Property

Parent Object: [SheetMetalRule](SheetMetalRule.md)  

## Description

Gets and sets the relief placement for a two-bend relief shape. When the relief shape is round, both intersection and tangent are valid placements. For square shape, only intersection is valid. For all other shapes, this property will return NoTwoBendReliefPlacement because the placement option is not used.

## Syntax

"sheetMetalRule_var" is a variable referencing a SheetMetalRule object.  

```python
# Get the value of the property.
propertyValue = sheetMetalRule_var.twoBendReliefPlacement

# Set the value of the property.
sheetMetalRule_var.twoBendReliefPlacement = propertyValue
```

## Property Value

This is a read/write property whose value is a [TwoBendReliefPlacements](TwoBendReliefPlacements.md).

## Version

Introduced in version November 2022  

