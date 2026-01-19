# ToolLibrary.createFromJson Method

Parent Object: [ToolLibrary](ToolLibrary.md)  

## Description

Creates a ToolLibrary by given JSON-string. Raises an error if the given JSON is invalid.

## Syntax

This is a static method.  

```python

returnValue = adsk.cam.ToolLibrary.createFromJson(json)
```

## Return Value

| Type                           | Description                            |
|--------------------------------|----------------------------------------|
| [ToolLibrary](ToolLibrary.md) | Returns the newly created ToolLibrary. |

## Parameters

| Name | Type | Description |
|----|----|----|
| json | string | The JSON contains all tools that should be added to the new ToolLibrary |

## Version

Introduced in version April 2023  

