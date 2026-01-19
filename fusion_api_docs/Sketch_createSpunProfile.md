# Sketch.createSpunProfile Method

Parent Object: [Sketch](Sketch.md)  

## Description

Creates sketch geometry that represents the spun profile. The spun profile is the silhouette of the entities as if they were spinning around an axis. The created spun profile is based on the information provided by the SpunProfileInput object.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.createSpunProfile(input)
```

## Return Value

| Type | Description |
|----|----|
| [SketchEntity](SketchEntity.md)\[\] | An array of sketch entities that were created as a result of the spun profile. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [SpunProfileInput](SpunProfileInput.md) | The SpunProfileInput object that specifies the input needed to create the spun profile. |

## Version

Introduced in version November 2024  

