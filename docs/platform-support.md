# Platform support

This table records only compatibility that NetCalcKit has directly verified or documented from authoritative product material.

| Platform | Status | Notes |
| --- | --- | --- |
| AdGuard Home | Verified for DNS enforcement | The 13-rule subscription loaded, refreshed, blocked every listed hostname, and allowed an unrelated control domain in an isolated v0.107.79 test. Application-level testing remains ongoing. |
| Pi-hole | Verified for DNS enforcement | Pi-hole Core v6.4.3 Gravity parsed 13 exact domains with zero invalid entries; all 13 blocked and an unrelated control domain resolved normally. |
| NextDNS | Pending | No NetCalcKit installation guide is published yet. |
| Control D | Pending | No NetCalcKit installation guide is published yet. |

“Verified for DNS enforcement” does not mean that every app or website has been tested. See `false-positive-testing.md` for the application-level protocol.
