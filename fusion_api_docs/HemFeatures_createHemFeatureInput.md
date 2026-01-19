# HemFeatures.createHemFeatureInput Method

Parent Object: [HemFeatures](HemFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a HemFeatureInput object. Use methods on this object to define the hem you want to create and then use the add method, passing in the HemFeatureInput object.

## Syntax

"hemFeatures_var" is a variable referencing a [HemFeatures](HemFeatures.md) object.

```python
returnValue = hemFeatures_var.createHemFeatureInput()
```

## Return Value

| Type | Description |
|----|----|
| [HemFeatureInput](HemFeatureInput.md) | Returns the newly created HemFeatureInput object or null if the creation failed. |

## Version

Introduced in version September 2025  

