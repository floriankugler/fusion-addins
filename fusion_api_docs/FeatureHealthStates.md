# FeatureHealthStates Enumerator

## Description

The various states that a feature can be in. This is used for the states of modeling features, construction geometry, and sketches.  

## Methods

| Name | Value | Description |
|----|----|----|
| ErrorFeatureHealthState | 2 | The feature, construction geometry, or sketch has an error. Use the errorOrWarningMessage property to get the message. |
| HealthyFeatureHealthState | 0 | The feature, construction geometry, or sketch is successfully computed. |
| RolledBackFeatureHealthState | 4 | The feature, construction geometry, or sketch is rolled back so it has not computed. |
| SuppressedFeatureHealthState | 3 | The feature, construction geometry, or sketch is suppressed so it has not computed. |
| UnknownFeatureHealthState | 5 | The state of the object is unknown. This can occur in the case where the object being queried is a TimelineObject whose associated entity does not have a health state. For example, if it is a TimelineGroup or an position snapshot. |
| WarningFeatureHealthState | 1 | The feature, construction geometry, or sketch has a warning. Use the errorOrWarningMessage property to get the message. |

## Version

Introduced in version August 2016  

