# RGB Protocol Documentation

RGB is a protocol developed in order to enforce digital rights in form of contracts and assets in a scalable and private manner leveraging Bitcoin consensus rules and operations.

This guide targets the broader technical audience willing to understand in depth the RGB protocol, from its theoretical foundations rooted in [Client-side Validation](annexes/glossary.md#client-side-validation) and [Single-use Seals](annexes/glossary.md#single-use-seal) to the more core features of [State Transitions](annexes/glossary.md#state-transition) and Contract Structure. The relevant terms and concepts will be introduced step by step and they will be referenced to external material in case more detailed study by non computer science audience is needed.

{% hint style="info" %}
RGB Protocol on Bitcoin — not to be confused with:
- The RGB color model (Red, Green, Blue — unrelated)
- RGB v0.12 (unfinished proposal do rewrite the protocol, promoted by the owner of the RGB-WG organization)
- RGB++ (a separate protocol on the Nervos/CKB blockchain — different team, different architecture)

For general information and education visit [rgb.info](https://rgb.info).
{% endhint %}

## Credits

The production of this documentation has been sponsored by [Bitfinex](https://www.bitfinex.com/) and the material provided is mostly based on a 3-day full-immersion seminar on RGB Protocol held by [Maxim Orlovsky](https://twitter.com/dr\_orlovsky) at the Tuscany Lightning Bootcamp in October 2023.

Videos: [https://planb.academy/courses/3ce1d37c-05ba-4f54-aa15-7586d37b2bb7](https://planb.academy/courses/3ce1d37c-05ba-4f54-aa15-7586d37b2bb7)

***
