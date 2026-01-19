# CommandTerminationReason Enumerator

## Description

Defines the termination reason for a command. Commands can be terminated for a number of different reasons, and based on the reason commands have to do different things during termination so this enum defines various reasons for termination  

## Methods

| Name | Value | Description |
|----|----|----|
| AbortedTerminationReason | 3 | The command is terminated by clicking OK button, and executed failed. |
| CancelledTerminationReason | 2 | The command is terminated by clicking Cancel button. |
| CompletedTerminationReason | 1 | The command is terminated by clicking OK button, and executed successfully. |
| PreEmptedTerminationReason | 4 | The command is terminated by activating another command. |
| SessionEndingTerminationReason | 5 | The command is terminated by closing the document. |
| UnknownTerminationReason | 0 | The command is terminated out of the reasons list below. |

## Version

Introduced in version June 2015  

