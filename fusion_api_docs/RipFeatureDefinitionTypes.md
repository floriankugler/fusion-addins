# RipFeatureDefinitionTypes Enumerator

## Description

Specifies the different ways a Rip feature can be defined.  

## Methods

| Name | Value | Description |
|----|----|----|
| AlongEdgeRipFeatureDefinitionType | 2 | Rips along an edge. |
| BetweenPointsRipFeatureDefinitionType | 3 | Rips between two points on a face. The points may be defined either by vertices, or by an edge and an offset along that edge. |
| FaceRipFeatureDefinitionType | 1 | Rips an entire face. |
| UndefinedRipFeatureDefinitionType | 0 | The rip type is undefined. This occurs when a new RipFeatureInput is created and before a specific type has been defined. |

## Version

Introduced in version September 2023  

