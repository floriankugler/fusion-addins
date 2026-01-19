# MaterialLibrary.unload Method

Parent Object: [MaterialLibrary](MaterialLibrary.md)  

## Description

Unloads this material from Fusion. Only non-native material libraries can be unloaded. You can determine this by checking the isNative property.

## Syntax

"materialLibrary_var" is a variable referencing a [MaterialLibrary](MaterialLibrary.md) object.

```python
returnValue = materialLibrary_var.unload()
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns True if the library was successfully unloaded. |

## Samples

| Name | Description |
| --- | --- |
| [Material API Sample](MaterialSample_Sample.md) | Demonstrates using materials and appearance using the API. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. The sample also used an external appearance library which you can get [here](../ExtraFiles/APISampleMaterialLibrary2.adsklib). Copy that to any location on your computer and edit the path in the script. When running the script, have a design open that contains a body in the root component. |

## Version

Introduced in version March 2017  

