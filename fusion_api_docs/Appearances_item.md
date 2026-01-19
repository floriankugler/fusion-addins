# Appearances.item Method

Parent Object: [Appearances](Appearances.md)  

## Description

Returns the specified Appearance using an index into the collection.

## Syntax

"appearances_var" is a variable referencing an [Appearances](Appearances.md) object.

```python
returnValue = appearances_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Appearance](Appearance.md) | Returns the specified appearance or null if an invalid index is specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | integer | The index of the appearance to return where the first item in the collection is 0. |

## Samples

| Name | Description |
| --- | --- |
| [Material API Sample](MaterialSample_Sample.md) | Demonstrates using materials and appearance using the API. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. The sample also used an external appearance library which you can get [here](../ExtraFiles/APISampleMaterialLibrary2.adsklib). Copy that to any location on your computer and edit the path in the script. When running the script, have a design open that contains a body in the root component. |

## Version

Introduced in version August 2014  

