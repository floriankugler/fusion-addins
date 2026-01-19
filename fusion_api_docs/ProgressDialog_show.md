# ProgressDialog.show Method

Parent Object: [ProgressDialog](ProgressDialog.md)  

## Description

Displays the progress dialog that includes a progress bar that can be used to display a continually updated message indicating the progress of a process that will take more than a few seconds. The progress is determined by comparing the current progress value with the minimum and maximum values.

## Syntax

"progressDialog_var" is a variable referencing a [ProgressDialog](ProgressDialog.md) object.

```python
# Uses no optional arguments.
returnValue = progressDialog_var.show(title, message, minimumValue, maximumValue)

# Uses optional arguments.
returnValue = progressDialog_var.show(title, message, minimumValue, maximumValue, delay)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| title | string | Sets the title for the progress dialog |
| message | string | The message to display along with the progress bar. The following symbols can be used to display values. "%p" is replaced by the percentage completed. "%v" is replaced by the current value. %m is replaced by the total number of steps. For example, the message "Processing section %v of %m." will result in the message "Processing section 1 of 10." to be displayed if the maximum value is 10 and the current value is 1. |
| minimumValue | integer | The minimum value of the progress bar. This is used along with the maximum value and the progress value to compute the current percentage complete. This is also the initial progress value when the progress bar is first displayed. |
| maximumValue | integer | The maximum value of the progress bar. This is used along with the minimum value and the progress value to compute the current percentage complete. |
| delay | integer | Specifies the time interval in seconds to delay displaying the Progress Dialog. This provides a way to hide the progress dialog before it actually gets displayed, which is useful for cases where the progress of the operation being tracked completes quickly and there is no need to indicate progress to the user. This is an optional argument whose default value is 0. |

## Samples

| Name | Description |
|----|----|
| [Generate Toolpaths API Sample](GenerateToolpaths_Sample_Sample.md) | Demonstrates generating the toolpaths in the active document. |
| [Progress Dialog API Sample](ProgressDialogSample_Sample.md) | Demonstrates how to use progress dialog |

## Version

Introduced in version January 2016  

