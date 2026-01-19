# OperationStates Enumerator

## Description

The possible states of an operation. Some operations do not generate toolpaths, their state ignores the potential toolpath states.  

## Methods

| Name | Value | Description |
|----|----|----|
| IsInvalidOperationState | 1 | Indicates the state where the operation or its toolpath is invalid. |
| IsValidOperationState | 0 | Indicates the state where the operation is valid and is up to date and the toolpath exists if applicable. |
| NoToolpathOperationState | 3 | Indicates the state where the toolpath does not exist for an operation. Not applicable for operations that do not generate toolpaths. |
| SuppressedOperationState | 2 | Indicates the state where the operation is suppressed. Toolpaths do not exist for suppressed operations. |

## Version

Introduced in version January 2016  

