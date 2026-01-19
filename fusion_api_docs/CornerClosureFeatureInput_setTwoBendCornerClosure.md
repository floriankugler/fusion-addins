# CornerClosureFeatureInput.setTwoBendCornerClosure Method

Parent Object: [CornerClosureFeatureInput](CornerClosureFeatureInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Sets the corner closure input with the values to be used to create a two-bend corner closure feature. Before using this method, the definitionType property should be examined to determine whether the corner is two-bend or three-bend, as this method is only applicable for two-bend corner closures.

## Syntax

"cornerClosureFeatureInput_var" is a variable referencing a [CornerClosureFeatureInput](CornerClosureFeatureInput.md) object.

```python
returnValue = cornerClosureFeatureInput_var.setTwoBendCornerClosure(parameters)
```

## Return Value

| Type    | Description                                                |
|---------|------------------------------------------------------------|
| boolean | Returns true if defining the corner closure is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameters | [TwoBendCornerClosureInputDefinition](TwoBendCornerClosureInputDefinition.md) | A TwoBendCornerClosureParameters object that encapsulates all the required parameters for creating a two-bend corner closure feature. This includes miter gap, alignment settings, bend transition type, relief shape, relief size, and relief placement options. |

## Version

Introduced in version January 2026  

