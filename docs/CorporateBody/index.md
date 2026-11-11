# CorporateBody

**Completion:** █████████░ 90%

## Status overview

| Status | Count |
| --- | --- |
| Total | 11 |
| Active | 9 |
| Deferred | 1 |
| Deprecated | 1 |

## Properties

| Property | Label | Status | Mapping | Mandatory | Repeatable |
| --- | --- | --- | --- | --- | --- |
| [name](name.md) | Namn | active | closeMatch | TRUE | FALSE |
| [activityStartDate](activityStartDate.md) | Verksamhetens starttid | active | closeMatch | FALSE | FALSE |
| [activityEndDate](activityEndDate.md) | Verksamhetens sluttid | active | closeMatch | FALSE | FALSE |
| [establishmentDate](establishmentDate.md) | Tid för grundande | active | exactMatch | FALSE | FALSE |
| [terminationDate](terminationDate.md) | Tid för upphörande | active | exactMatch | FALSE | FALSE |
| [description](description.md) | Beskrivning | active | closeMatch | FALSE | TRUE |
| [Jurisdiction](Jurisdiction.md) | Geografisk jurisdiction | active |  | FALSE | FALSE |
| [fieldOfActivity](fieldOfActivity.md) | Verksamhetsområde | deprecated | exactMatch | FALSE | TRUE |
| [seeAlso](seeAlso.md) | Se även | active | closeMatch | FALSE | TRUE |
| [variant](variant.md) | Variantnamn | deferred | closeMatch | FALSE | TRUE |
| [cataloguersNote](cataloguersNote.md) | Katalogisatörens anmärkning | active | closeMatch | TRUE | TRUE |
