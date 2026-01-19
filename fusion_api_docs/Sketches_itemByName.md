# Sketches.itemByName Method

Parent Object: [Sketches](Sketches.md)  

## Description

Returns the sketch with the specified name.

## Syntax

"sketches_var" is a variable referencing a [Sketches](Sketches.md) object.

```python
returnValue = sketches_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [Sketch](Sketch.md) | Returns the sketch or null if there isn't a sketch with that name. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the sketch as seen in the browser and the timeline. |

## Version

Introduced in version August 2014  

