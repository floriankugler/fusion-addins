# Command.doExecutePreview Method

Parent Object: [Command](Command.md)  

## Description

Causes the executePreview event of this command to be fired. This is most useful when there is no command dialog (no command inputs where created) and the isAutoExecute property has been set to False. This allows you to force the preview to be generated instead of relying on changing command inputs.

## Syntax

"command_var" is a variable referencing a [Command](Command.md) object.

```python
returnValue = command_var.doExecutePreview()
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the execute Preview event was successfully fired.. |

## Version

Introduced in version April 2017  

