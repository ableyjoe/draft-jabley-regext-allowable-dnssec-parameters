---
title: "Acceptance of DNSSEC Parameters in EPP"
#abbrev: "TODO - Abbreviation"
category: bcp

docname: draft-jabley-regext-allowable-dnssec-parameters-latest
submissiontype: IETF  # also: "independent", "editorial", "IAB", or "IRTF"
number:
date:
consensus: true
v: 3
area: "Operations and Management"
workgroup: "Registration Protocols Extensions"
keyword:
 - dnssec
 - epp
venue:
  group: "Registration Protocols Extensions"
  type: "Working Group"
  mail: "regext@ietf.org"
  arch: "https://mailarchive.ietf.org/arch/browse/regext/"
  github: "ableyjoe/draft-jabley-regext-allowable-dnssec-parameters"
  latest: "https://ableyjoe.github.io/draft-jabley-regext-allowable-dnssec-parameters/draft-jabley-regext-allowable-dnssec-parameters.html"

author:
 -
    fullname: Joe Abley
    organization: Cloudflare
    email: jabley@cloudflare.com

normative:
  DNSKEY-IANA:
    title: DNS Security Algorithm Numbers
    author:
      org: IANA
    target: https://www.iana.org/assignments/dns-sec-alg-numbers

  DS-IANA:
    title: Digest Algorithms
    author:
      org: IANA
    target: https://www.iana.org/assignments/ds-rr-types

informative:

--- abstract

The Extensible Provisioning Protocol (EPP) is used to submit DNSSEC
parameters for domain names to domain name registries. Registries
and registrars often restrict the values they accept, and those
restrictions vary from registry to registry. The resulting uncertainty
makes it difficult for DNS operators to adopt new algorithms.  This
document recommends that registries and registrars base their
acceptance policies on the IANA registries for DNSSEC algorithms
and digest types.

--- middle

# Introduction {#intro}

DNS Security Extensions (DNSSEC) are described in {{!RFC9364}}. The
Extensible Provisioning Protocol (EPP) {{!RFC5730}} is used by
registrars to manage domain names in domain registries, and
{{!RFC5910}} specifies how DNSSEC parameters are conveyed in EPP.

For a signed zone to have a secure delegation, DS data must be
submitted to the parent registry, usually by a registrar using EPP.
That data identifies the algorithm used to sign the zone and the
digest type used to construct the DS record. When the algorithm
changes, new DS data must be submitted.

Guidance on suitable algorithms changes over time. Advances in
cryptanalysis weaken existing algorithms, and new algorithms are
being developed, for example to resist cryptanalysis by quantum
computers. Each new algorithm or digest type specified for DNSSEC is
assigned a new codepoint, and following current guidance is only
possible if registries and registrars accept those codepoints.

Registries and registrars often constrain the values they accept
using allowlists. What those allowlists contain, whether they are
published and how they are maintained varies, and this inconsistency
makes new algorithms difficult to deploy. [CITATIONS NEEDED]

The inconsistency is felt most by DNS operators. The algorithm used
for a zone is generally chosen by the DNS operator that signs it,
which may or may not be the registrar, and that choice is typically
made once for many zones in many top-level domains, before any EPP
transaction takes place. A DNS operator that cannot predict whether
a registry will accept a new algorithm risks leaving zones stuck
partway through an algorithm rollover, unable to retire the old
algorithm because DS data for the new one was rejected. Where DS
data is provisioned automatically, there may be nobody in a position
to notice the rejection.

Faced with this uncertainty, a DNS operator can use only algorithms
that every relevant registry is known to accept, limiting registrants
to what the most conservative registry allows. Alternatively, it can
sign only zones whose registries have known policies, or not sign
zones at all. DNSSEC deployment faces many obstacles, most of which
are outside the scope of this document. Unpredictable registry policy
is one of them, and removing it is a modest but real reduction in the
friction associated with deploying DNSSEC.

The IANA registries {{DNSKEY-IANA}} and {{DS-IANA}} already record
which values are suitable for use with DNSSEC, and are updated as
guidance changes {{RFC9904}}. If registries base their acceptance
policies on those IANA registries, DNS operators can know in advance
which algorithms will be accepted, and newly assigned algorithms
become usable across registries at approximately the same time.

This document recommends a consistent and liberal policy, based on
those IANA registries, for the DNSSEC parameters that registries and
registrars accept in EPP.


# Conventions and Definitions

This document assumes familiarity with DNS and domain name registration
terminology as defined in {{!RFC9499}}.

The word "registry" is used in this document in two ways: to refer
to domain registries, as described in {{RFC9499}} and also to refer
to IANA registries in the IETF sense. When the intention is to refer
to an IANA registry, the phrase "IANA registry" is used.

{::boilerplate bcp14-tagged}


# DNSSEC Parameters in EPP

This document is concerned only with the `<secDNS:alg>` and
`<secDNS:digestType>` elements of the DS data interface. The key data
interface described in {{Section 4.2 of RFC5910}} is out of scope.
This document does not change the contents of the IANA registries or
the requirement levels they record.

{{Section 4.1 of !RFC5910}} defines two child elements of the
`<secDNS:dsData>` element that are relevant to this document:

* `<secDNS:alg>` contains the algorithm number of the DNSKEY
  referenced by the DS record, as described in
  {{Section 5.1.2 of !RFC4034}}; and
* `<secDNS:digestType>` contains the algorithm used to construct
  the digest, as described in {{Section 5.1.3 of !RFC4034}}.

Values for these elements are drawn from the IANA registries
{{DNSKEY-IANA}} and {{DS-IANA}} respectively. Following
{{!RFC9904}}, those IANA registries are the canonical source of
requirement levels for each value, and those requirement levels are
expected to change over time.

This document refers to the following columns in {{DNSKEY-IANA}}:

* "Zone Signing", which indicates whether an algorithm may appear
  in DNSKEY, RRSIG and DS records;
* "Use for DNSSEC Signing", which gives the requirement level for
  using an algorithm to sign zones; and
* "Use for DNSSEC Validation", which gives the requirement level for
  using an algorithm in DNSSEC validators.

This document refers to the following columns in {{DS-IANA}}:

* "Use for DNSSEC Delegation", which gives the requirement level for
  using a digest type in DS records published by authoritative
  servers; and
* "Use for DNSSEC Validation", which gives the requirement level for
  using a digest type in DNSSEC validators.

The "Implement for" columns in those IANA registries describe
requirements for software implementations rather than for the
operation of a zone, and are not used by this document.


# Recommendations for Registries and Registrars {#recommendations}

## Default Policy {#default}

Registries and registrars SHOULD accept any value of the
`<secDNS:alg>` and `<secDNS:digestType>` elements that is not
excluded by {{deny}}, and SHOULD NOT reject values on any other
basis. For a registrar, this applies to values received from
registrants and DNS operators through whatever interface the
registrar provides.

In particular, registries and registrars SHOULD NOT reject a value
solely because they do not themselves implement the corresponding
algorithm. A validator that does not support the algorithm or digest
type specified in a DS record disregards that record
({{Section 5.2 of !RFC4035}}, {{Section 5.2 of !RFC6840}}), so
accepting such values cannot cause validation failures for the zone
concerned. Similarly, registries and registrars that check the
length of the `<secDNS:digest>` element SHOULD do so only for digest
types whose digest length they know.

A registrar SHOULD NOT apply restrictions beyond those applied by the
registry for the domain name concerned. A registrar is not expected
to accept a value that the registry would reject, and can instead
report the registry's rejection to its customer.


## Values to Deny {#deny}

The values to be denied are derived from the current contents of
{{DNSKEY-IANA}} and {{DS-IANA}}, not from a fixed snapshot of those
IANA registries.

The values excluded below are unassigned, cannot appear in DS
records, or are no longer expected to be validated. DS data containing
them provides no security benefit, and accepting them could lead a
registrant or DNS operator to believe that a zone is protected when
it is not. Rejecting such values also catches errors in submitted
data.

Registries and registrars SHOULD reject a `<secDNS:alg>` value
unless both of the following conditions are met:

* the "Zone Signing" column for the value in {{DNSKEY-IANA}} is
  "Y"; and
* the "Use for DNSSEC Validation" column for the value is not
  "MUST NOT".

These conditions admit the values reserved for private algorithms,
which are marked "Y" in the "Zone Signing" column. They exclude
values that are unassigned or reserved, and values that are not
usable in DS records.

Registries and registrars SHOULD reject a `<secDNS:digestType>`
value unless either of the following conditions is met:

* the "Use for DNSSEC Validation" column for the value in
  {{DS-IANA}} contains a requirement level other than "MUST NOT";
  or
* the value is reserved for private use.


## Existing DS Data {#existing}

The contents of the IANA registries change over time, so DS data
that was accepted in the past may later include values that
{{deny}} would exclude.

Registries and registrars MUST NOT reject a request to remove DS
data on the grounds that it contains values that would be denied
under {{deny}}.

Registries and registrars SHOULD NOT reject an otherwise acceptable
request on the grounds that DS data already associated with the
domain name contains values that would be denied under {{deny}}.


## Keeping Current {#current}

Registries and registrars SHOULD reflect changes to {{DNSKEY-IANA}}
and {{DS-IANA}} in their acceptance policy within 30 days of those
changes being published.


## Publication {#publication}

Registries and registrars SHOULD publish their policy for accepting
`<secDNS:alg>` and `<secDNS:digestType>` values at a stable and
publicly accessible location, so that registrants and DNS operators
can make informed choices. The published policy SHOULD state whether
it follows this document and SHOULD describe any respect in which it
does not. For registries that publish a DNSSEC Practice Statement
{{?RFC6841}}, that document is a suitable location.


# Operational Considerations {#operational}

Registry and registrar systems that process DS data, including
systems that generate zone data or publish registration data, may
encounter algorithm and digest type values they have not seen
before. Such systems need to handle unfamiliar values without
failure, for example by treating them as opaque numbers. A failure in
a registry's own systems caused by an unfamiliar value could affect
many delegations, not only the one concerned, and is a more
significant risk than any effect on validation.


# Security Considerations {#security}

## Unsupported Algorithms and Digest Types

The recommendations in {{recommendations}} cause registries and
registrars to accept algorithm and digest type values that they, and
some validators, may not implement.

A validator that does not support the algorithm specified in a DS
record, or that does not support its digest type, disregards that
record ({{Section 5.2 of RFC4035}}, {{Section 5.2 of !RFC6840}}). If
no remaining DS record for a delegation uses a supported algorithm
and digest type, the validator treats the child zone as unsigned.
Accepting such values therefore cannot cause a validator to treat a
correctly signed zone as bogus. The worst outcome is that the zone
is unsigned from the point of view of validators that lack support.
This is no worse than if the DS data had been rejected.

Registrants and DNS operators who publish DS data using only
algorithms that are not yet widely supported should understand that
their zones will not be validated by validators without that
support. Validators also generally do not support the private
algorithm values (253 and 254) in {{DNSKEY-IANA}}, and different
parties may interpret them differently.


## Weak Algorithms and Digest Types

A validator may accept any valid chain of trust from the parent to
the child, regardless of what other algorithms are present
({{Section 5.11 of RFC6840}}). The security of a signed delegation is
therefore limited by the weakest algorithm and digest type in its DS
data that validators still accept. Publishing DS data that uses a
weak algorithm or digest type alongside DS data that uses a strong
one does not preserve the strength of the stronger combination.

The values denied in {{deny}} either cannot be used in DS records or
are no longer expected to be validated, so they add no assurance.
Values that are deprecated for signing or delegation but are still
validated represent a greater risk. This document does not
recommend rejecting them, since doing so would interfere with
registrants who have not yet completed an algorithm rollover. The
risk of using a weak algorithm or digest type falls mainly on the
zone concerned and the zones beneath it.


## Unauthorised Changes

An attacker who can submit DS data for a domain name, for example by
compromising a registrant's account at a registrar, could submit DS
data containing arbitrary values. Accepting a wider range of values
does not materially change the impact of such an attack. An attacker
with that access could already remove the DS data or change the
delegation itself.


## Algorithm Agility

Policies that are too restrictive, or that are not kept current
({{current}}), can prevent registrants from moving away from
algorithms that are becoming weaker or from adopting new ones, such
as those designed to resist cryptanalysis by quantum computers. This
prolongs exposure to the weaknesses that algorithm agility is meant
to address. The recommendations in this document are intended to
remove that obstacle while still allowing registries and registrars
to exclude values that offer no security benefit.


# IANA Considerations {#iana}

This document has no IANA actions.


--- back

# Acknowledgments
{:numbered="false"}

Bas Westerbaan provided post-quantum energy. Scott Hollenbeck and
Gavin Brown provided welcome encouragement.

