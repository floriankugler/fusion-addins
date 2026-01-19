# Sketch.revisionId Property

Parent Object: [Sketch](Sketch.md)  

## Description

Returns the current revision ID of the sketch. This ID changes any time the sketch is modified in any way. By getting and saving the ID when you create any data that is dependent on the sketch, you can then compare the saved ID with the current ID to determine if the sketch has changed to know if you should update your data.

## Syntax

"sketch_var" is a variable referencing a Sketch object.  

```python
# Get the value of the property.
propertyValue = sketch_var.revisionId
```

## Property Value

This is a read only property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Sketch Sample API Sample](SketchSample_Sample.md) | Sketch related functions |

## Version

Introduced in version September 2017  

