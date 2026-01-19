# Application.getLastError Method

Parent Object: [Application](Application.md)  

## Description

Returns information about the last error that occurred.

## Syntax

"application_var" is a variable referencing an [Application](Application.md) object.  

```python
# Uses no optional arguments.
(returnValue, description) = application_var.getLastError()

# Uses optional arguments.
(returnValue, description) = application_var.getLastError()
```

## Return Value

| Type    | Description                               |
|---------|-------------------------------------------|
| integer | Returns the number of the specific error. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| description | string | A description of the last error in English. This is an optional argument whose default value is "". |

## Version

Introduced in version August 2014  

