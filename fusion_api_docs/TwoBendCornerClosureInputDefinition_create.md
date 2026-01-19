# TwoBendCornerClosureInputDefinition.create Method

Parent Object: [TwoBendCornerClosureInputDefinition](TwoBendCornerClosureInputDefinition.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a TwoBendCornerClosureParameters object that can be used to define parameters for a two-bend corner closure. Use properties on this object to set the relief shape, relief size, relief placement, miter gap, alignment settings, and bend transition type before passing it to the setTwoBendCornerClosure method.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.TwoBendCornerClosureInputDefinition.create()
```

## Return Value

| Type | Description |
|----|----|
| [TwoBendCornerClosureInputDefinition](TwoBendCornerClosureInputDefinition.md) | Returns the newly created TwoBendCornerClosureParameters object or null if the creation failed. |

## Version

Introduced in version January 2026  

