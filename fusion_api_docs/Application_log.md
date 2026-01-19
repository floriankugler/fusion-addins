# Application.log Method

Parent Object: [Application](Application.md)  

## Description

Logs messages to either the TEXT COMMAND window or the Fusion app log file.

## Syntax

This is a static method.  

```python

# Uses no optional arguments.
returnValue = adsk.core.Application.log(message)

# Uses optional arguments.
returnValue = adsk.core.Application.log(message, level, type)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| message | string | The message to write to the log. |
| level | [LogLevels](LogLevels.md) | The log level. Default value is InfoLogLevel. This is only used when the log type is FileLogType where the log message will include the log level. This is an optional argument whose default value is LogLevels.InfoLogLevel. |
| type | [LogTypes](LogTypes.md) | The log type. The default value is ConsoleLogType to write the message to the TEXT COMMAND window. When the type is FileLogType, the message is written to Fusion's app log file which is the same file where Fusion writes all of its log messages. You can get the path and filename of the current log file by using the TEXT COMMAND window. In the lower-right corner you can choose "Txt", "Py", or "Js". Choose the "Txt" option and type "paths.get" in the input field and press return. A list of all of the various paths used by Fusion will be displayed in the TEXT COMMAND window. The line for "AppLogFilePath" has the full path to the log file. This is an optional argument whose default value is LogTypes.ConsoleLogType. |

## Version

Introduced in version July 2021  

