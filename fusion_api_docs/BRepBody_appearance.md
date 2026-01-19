# BRepBody.appearance Property

Parent Object: [BRepBody](BRepBody.md)  

## Description

Read-write property that gets and sets the current appearance of the body. Setting this property will result in applying an override appearance to the body and the AppearanceSourceType property will return OverrideAppearanceSource. Setting this property to null will remove any override.  

This property is only valid if the IsTransient property is false.

## Syntax

"bRepBody_var" is a variable referencing a BRepBody object.  

```python
# Get the value of the property.
propertyValue = bRepBody_var.appearance

# Set the value of the property.
bRepBody_var.appearance = propertyValue
```

## Property Value

This is a read/write property whose value is an [Appearance](Appearance.md).

## Samples

| Name | Description |
| --- | --- |
| [Material API Sample](MaterialSample_Sample.md) | Demonstrates using materials and appearance using the API. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. The sample also used an external appearance library which you can get [here](../ExtraFiles/APISampleMaterialLibrary2.adsklib). Copy that to any location on your computer and edit the path in the script. When running the script, have a design open that contains a body in the root component. |

## Version

Introduced in version August 2014  

