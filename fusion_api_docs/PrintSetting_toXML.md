# PrintSetting.toXML Method

Parent Object: [PrintSetting](PrintSetting.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Generates and returns the print setting xml content string.

## Syntax

"printSetting_var" is a variable referencing a [PrintSetting](PrintSetting.md) object.

```python
returnValue = printSetting_var.toXML()
```

## Return Value

| Type   | Description                               |
|--------|-------------------------------------------|
| string | Returns print setting xml content string. |

## Version

Introduced in version January 2026  

