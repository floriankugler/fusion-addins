# PostCapabilities Enumerator

## Description

List of capabilities a post configuration can support. These capabilities represent either a class of operations (milling, turning, etc.) or some additional functionality (e.g. machine simulation).  

## Methods

| Name | Value | Description |
|----|----|----|
| Additive | 64 | Post supports additive operations. |
| Cascading | 32 | Post configuration is intended to run as a complement to another post that produces NC code to pass additional data to an external application. |
| Inspection | 128 | Post supports surface inspection operations. |
| Intermediate | 8 | Post outputs data in an intermediate format intended for processing by another application rather than NC code for a machine. |
| Jet | 16 | Post supports jet cutting operations (e.g. water jet, plasma, or laser). |
| MachineSimulation | 256 | Post configuration provides additional data to support machine simulation. |
| Milling | 1 | Post supports milling operations. |
| SetupSheet | 4 | Post creates a setup sheet rather than NC code. |
| Turning | 2 | Post supports turning operations. |
| Undefined | 0 | Undefined, default when query is created. |

## Version

Introduced in version April 2023  

