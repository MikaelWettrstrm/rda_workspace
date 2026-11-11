# Person

**Completion:** ████░░░░░░ 42%

## Status overview

| Status | Count |
| --- | --- |
| Total | 25 |
| Active | 10 |
| Deferred | 14 |
| Deprecated | 0 |

## Properties

| Property | Label | Status | Mapping | Mandatory | Repeatable |
| --- | --- | --- | --- | --- | --- |
| [name](name.md) | Namn | active | closeMatch | TRUE | FALSE |
| [familyName](familyName.md) | Efternamn | active | exactMatch | TRUE | FALSE |
| [givenName](givenName.md) | Förnamn | active | exactMatch | TRUE | FALSE |
| [birthDate](birthDate.md) | Födelsedatum | active | exactMatch | FALSE | FALSE |
| [deathDate](deathDate.md) | Dödsdatum | active | exactMatch | FALSE | FALSE |
| [lifeSpan](lifeSpan.md) | Födelsetid och/eller dödstid | deferred |  | FALSE | FALSE |
| [activityStartDate](activityStartDate.md) | Verksamhetens starttid | deferred | closeMatch | FALSE | FALSE |
| [activityEndDate](activityEndDate.md) | Verksamhetens sluttid | deferred | closeMatch | FALSE | FALSE |
| [fieldOfActivity](fieldOfActivity.md) | Verksamhetsområde | active | exactMatch |  |  |
| [fullerFormOfName](fullerFormOfName.md) | Fullständig namnform | active | exactMatch | FALSE | TRUE |
| [hasOccupation](hasOccupation.md) | Yrke eller sysselsättning | deferred | exactMatch | FALSE | TRUE |
| [hasAffiliation](hasAffiliation.md) | Organisatorisk tillhörighet |  |  | FALSE | TRUE |
| [identifiedBy](identifiedBy.md) | Identifikator | deferred | closeMatch | FALSE | TRUE |
| [description](description.md) | Beskrivning | active | closeMatch | FALSE | TRUE |
| [titlesAndOtherWordsAssociatedWithAName](titlesAndOtherWordsAssociatedWithAName.md) | Titel eller övrig beteckning | deferred | exactMatch | FALSE | TRUE |
| [hasOtherAttributes](hasOtherAttributes.md) | Övrig beteckning | deferred |  |  |  |
| [titleOfPerson](titleOfPerson.md) | Titel/officiell rang för kunglig, adlig eller religiös person | deferred |  |  |  |
| [nationality](nationality.md) | Nationalitet/Verksamhetsland | deferred |  | FALSE | TRUE |
| [birthPlace](birthPlace.md) | Födelseplats | deferred | exactMatch | FALSE | FALSE |
| [deathPlace](deathPlace.md) | Dödsplats | deferred | exactMatch | FALSE | FALSE |
| [associatedLanguage](associatedLanguage.md) | Språk | active | exactMatch | FALSE | TRUE |
| [seeAlso](seeAlso.md) | Se även | active | closeMatch | FALSE | TRUE |
| [variant](variant.md) | Variantnamn | deferred | closeMatch | FALSE | TRUE |
| [cataloguersNote](cataloguersNote.md) | Katalogisatörens anmärkning | deferred |  | TRUE | TRUE |
| [sourceConsulted](sourceConsulted.md) | Konsulterad källa | deferred |  |  |  |
