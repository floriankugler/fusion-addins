# CommandDefinition.deleteMe Method

Parent Object: [CommandDefinition](CommandDefinition.md)  

## Description

Deletes this command definition. This is only valid for API created command definitions and will fail if the isNative property is true.

## Syntax

"commandDefinition_var" is a variable referencing a [CommandDefinition](CommandDefinition.md) object.

```python
returnValue = commandDefinition_var.deleteMe()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns true or false indicating if the deletion was successful. |

## Version

Introduced in version August 2014  

