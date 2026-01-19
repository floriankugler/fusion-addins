# ProgressBar.showBusy Method

Parent Object: [ProgressBar](ProgressBar.md)  

## Description

This method displays a message in the busy bar in the lower-right corner of the Fusion window. The busy bar can be used to display a continually updated message indicating the progress of a process. The busy bar is different from the progress bar, because it does not show a meter indicating the current progress. Instead is shows a continually moving bar to indicate processing without showing the current progress. This is useful in cases where the length of the process is unknown.

## Syntax

"progressBar_var" is a variable referencing a [ProgressBar](ProgressBar.md) object.

```python
# Uses no optional arguments.
returnValue = progressBar_var.showBusy(message)

# Uses optional arguments.
returnValue = progressBar_var.showBusy(message, isModal)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| message | string | Specifies the message that will be displayed in the busy bar. An empty string can be specified if you don't want a message and use only the busy meter. |
| isModal | boolean | Specifies if the busy bar should be modal or not. If modal, the busy bar takes over the UI of Fusion, and the user cannot interact with any of the Fusion user interface. You need to be careful when using a modal dialog to make sure you hide the busy bar when you're finished or have an error condition that causes you to abort because otherwise, the user will need to kill the Fusion process. This is an optional argument whose default value is False. |

## Version

Introduced in version May 2024  

