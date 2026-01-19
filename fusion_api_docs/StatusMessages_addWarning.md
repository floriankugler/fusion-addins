# StatusMessages.addWarning Method

Parent Object: [StatusMessages](StatusMessages.md)  

## Description

Adds a new warning status message to the list of warning and error messages.

## Syntax

"statusMessages_var" is a variable referencing a [StatusMessages](StatusMessages.md) object.

```python
# Uses no optional arguments.
returnValue = statusMessages_var.addWarning()

# Uses optional arguments.
returnValue = statusMessages_var.addWarning(messageId, message)
```

## Return Value

| Type | Description |
|----|----|
| [StatusMessage](StatusMessage.md) | Returns true if the warning message was successfully added. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| messageId | string | The ID of a predefined message or if an empty string is provided, the default error message will be used. The displayed message is localized based on the current default language in Fusion. Below is a list of some valid message ID's and the corresponding English message. "API_COMPUTE_ERROR" - "Cannot compute this feature." "API_COMPUTE_WARNING" - "This feature computed with warnings." "CFLANGE_INVALID_GEOM" - "Invalid input sketch curve." "DRAFT_MISSING_FACE_REFERENCES" - "Missing face references" "DRAFT_MISSING_REFERENCE_PLANE" - "Missing reference plane" "FEATURE_ENTITY_TYPE_INVALID" - "Entity type is invalid" "FEATURE_FAILED_TO_CREATE" - "Failed to create feature" "FEATURE_MISSING_INPUTS" - "Missing inputs" "FEATURE_REFERENCE_LOST" - "Reference is lost" "Feature_Compute_Error" - "Compute Failed" "Feature_Input_Compute_Error" - "Reference Failures" "InvalidWPntInput" - "Invalid input" "NO_TARGET_BODY" - "No target body!" "ORIGIN_SELECTION_MISSING" - "Origin geometry is missing." "DRPOINT_COMPUTE_FAILED" - "Failed to evaluate the point due to the invalid input" This is an optional argument whose default value is "". |
| message | string | This is not currently supported for custom feature compute errors and will be ignored. This is an optional argument whose default value is "". |

## Version

Introduced in version July 2021  

