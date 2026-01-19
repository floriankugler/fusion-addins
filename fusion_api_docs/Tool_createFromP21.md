# Tool.createFromP21 Method

Parent Object: [Tool](Tool.md)  

## Description

Creates a Tool object given a string containing a tool defined using the P21 format. Throws an error if the given string does not conform to the P21 format.

## Syntax

This is a static method.  

```python

returnValue = adsk.cam.Tool.createFromP21(p21)
```

## Return Value

| Type             | Description                     |
|------------------|---------------------------------|
| [Tool](Tool.md) | Returns the newly created Tool. |

## Parameters

| Name | Type   | Description                                      |
|------|--------|--------------------------------------------------|
| p21  | string | Creates a Tool object from the given P21 string. |

## Version

Introduced in version September 2024  

