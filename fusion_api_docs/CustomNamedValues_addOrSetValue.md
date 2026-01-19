# CustomNamedValues.addOrSetValue Method

Parent Object: [CustomNamedValues](CustomNamedValues.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Adds or updates a value. If the specified ID does not exist, a new named value is added. If the ID does exist, the named value is updated with the specified value.

## Syntax

"customNamedValues_var" is a variable referencing a [CustomNamedValues](CustomNamedValues.md) object.

```python
returnValue = customNamedValues_var.addOrSetValue(id, value)
```

## Return Value

| Type    | Description                                        |
|---------|----------------------------------------------------|
| boolean | Returns true is successful and false if it failed. |

## Parameters

| Name  | Type   | Description                              |
|-------|--------|------------------------------------------|
| id    | string | The ID of the value to create or change. |
| value | string | The string to assign to the value.       |

## Version

Introduced in version July 2021  

