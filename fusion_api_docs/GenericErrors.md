# GenericErrors Enumerator

## Description

Errors that every API call can return via Application::GetLastError. These can be augmented with class and function specific errors.  

## Methods

| Name | Value | Description |
|----|----|----|
| BadApiCallError | 3 | The client made some sort of mistake calling the API object |
| ClassSpecificError | 100 | Errors reserved for several functions in a class. |
| ExpressionError | 6 | e.g. Errors related to bad value expressions or units - e.g. "1 in + 1 Kg" is an invalid expression |
| FunctionSpecificError | 200 | Errors reserved for a specific function in a class. |
| InternalValidationError | 2 | Internal API validation failed |
| InvalidGeometryError | 7 | When creating or changing an object via reference geometry, the geometry wasn't specified correctly (e.g. an Occurrence needs to be specified). |
| Ok | 0 | No error occurred. |
| OperationFailed | 5 | The API operation failed with the supplied error message. |
| UnderlyingObjectDeletedError | 4 | The API object is referencing a Neutron object that has been deleted. |
| UnexpectedError | 1 | An internal error occurred - e.g. a library function throw an exception. |

## Version

Introduced in version August 2014  

