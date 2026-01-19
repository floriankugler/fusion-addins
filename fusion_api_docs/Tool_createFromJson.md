# Tool.createFromJson Method

Parent Object: [Tool](Tool.md)  

## Description

Creates a Tool object from given JSON string.

## Syntax

This is a static method.  

```python

returnValue = adsk.cam.Tool.createFromJson(json)
```

## Return Value

| Type             | Description                     |
|------------------|---------------------------------|
| [Tool](Tool.md) | Returns the newly created Tool. |

## Parameters

| Name | Type | Description |
|----|----|----|
| json | string | The JSON should fully define the tool and contain all tool parameters. If the JSON contains more than one tool, only the first Tool is loaded. |

## Version

Introduced in version April 2023  

