# ProgressBar.show Method

Parent Object: [ProgressBar](ProgressBar.md)  

## Description

This method displays a message in the progress bar in the lower-right corner of the Fusion window. The progress bar can be used to display a continually updated message indicating the progress of a process. The progress is determined by comparing the current progress value with the minimum and maximum values.

## Syntax

"progressBar_var" is a variable referencing a [ProgressBar](ProgressBar.md) object.

```python
# Uses no optional arguments.
returnValue = progressBar_var.show(message, minimumValue, maximumValue)

# Uses optional arguments.
returnValue = progressBar_var.show(message, minimumValue, maximumValue, isModal)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| message | string | Specifies the message that will be displayed in the progress bar. The following symbols can be used to display values. "%p" is replaced by the percentage completed. "%v" is replaced by the current value. "%m" is replaced by the total number of steps. For example, the message "Processing section %v of %m." will result in the message "Processing section 1 of 10." to be displayed if the maximum value is 10 and the current value is 1. An empty string can be specified if you don't want a message and use only the progress meter. |
| minimumValue | integer | Specifies the minimum value of the progress. This value and the maximum and progress values to compute the current percentage complete. This is the initial progress value when the progress bar is first displayed. |
| maximumValue | integer | Specifies the maximum value of the progress. This value and the minimum and progress values are used to compute the current percentage completion. |
| isModal | boolean | Specifies if the progress bar should be modal or not. If modal, the progress bar takes over the UI of Fusion, and the user cannot interact with any of the Fusion user interface. You need to be careful when using a modal dialog to make sure you hide the progress bar when you're finished or have an error condition that causes you to abort because otherwise, the user will need to kill the Fusion process. This is an optional argument whose default value is False. |

## Version

Introduced in version May 2024  

