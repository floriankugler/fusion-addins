# SketchRadialDimension.entityToken Property

Parent Object: [SketchRadialDimension](SketchRadialDimension.md)  

## Description

Returns a token for the SketchDimension object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same sketch dimension.  

When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them.

## Syntax

"sketchRadialDimension_var" is a variable referencing a SketchRadialDimension object.  

```python
# Get the value of the property.
propertyValue = sketchRadialDimension_var.entityToken
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version September 2020  

