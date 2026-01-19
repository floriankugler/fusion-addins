# ShellFeature.setThicknesses Method

Parent Object: [ShellFeature](ShellFeature.md)  

## Description

Method that sets the inside and outside thicknesses of the shell.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"shellFeature_var" is a variable referencing a [ShellFeature](ShellFeature.md) object.

```python
returnValue = shellFeature_var.setThicknesses(insideThickness, outsideThickness)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| insideThickness | [ValueInput](ValueInput.md) | ValueInput object that defines the inside thickness. If set to null, the inside thickness is removed. |
| outsideThickness | [ValueInput](ValueInput.md) | ValueInput object that defines the outside thickness. If set to null, the outside thickness is removed. |

## Version

Introduced in version November 2014  

