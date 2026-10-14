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

The Extensible Provisioning Protocol (EPP) is used to maintain
DNSSEC parameters associated with domain names in domain name
registries. Many domain name registries constrain the allowed values
for these parameters according to local policy; however, a local
policy which is too narrow or which is not updated regularly can
make it difficult to gain operational experience with new algorithms.
This document recommends a liberal policy for registries and
registrars that allows new algorithms to be adopted without delay.

--- middle

# Introduction {#intro}

DNS Security Extensions (DNSSEC) are described in {{!RFC9364}}. The
Extensible Provisioning Protocol (EPP) is described in {{!RFC5730}}.
A mapping of DNSSEC parameters for EPP is described in {{!RFC5910}}.

EPP is used by domain registrars to maintain various parameters
associated with registered domain names in domain registries.  In
particular, the choice of DNSSEC algorithm by the registrant of a
signed zone must be submitted to a registry via a registrar in order
for a secure delegation to be published. If a registrant changes
the algorithm used, new parameters must be submitted.

Both EPP and DNSSEC are extensible; in particular, they both
accommodate the use of new cryptographic algorithms. This is important
because guidance on the suitability of particular algorithms changes
over time. For example, algorithms that were once considered good
choices are weakened through advances in cryptanalysis; new algorithms
have been developed in order to provide defence against threats of
cryptanalysis by quantum computers. New algorithms that are specified
for use with DNSSEC are assigned new codepoints.

For a registrant to be able to follow evolving guidance about the
choice of signing algorithm, it must be possible for the codepoints
assigned to new algorithms to be accepted by both registry and
registrar. It is therefore important that any constraints imposed
by registries or registrars recognise this need, and that
the constraints are sufficiently liberal that they do not prevent
registrants from using new algorithms.

The allowable values for DNSSEC parameters in EPP are often constrained
using an allowlist by registries and registrars. The nature
of the allowlist (e.g. what is allowed, whether the allowlist is
published and how it is maintained) varies between registries and
registrars, and the lack of consistency can make it a challenge to
deploy new algorithms. [CITATIONS NEEDED]

This document recommends a consistent and liberal approach for
registries and registrars to handle DNSSEC parameters in EPP
in order to accommodate algorithm agility in secure delegations.


# Conventions and Definitions

This document assumes familiarity with DNS and domain name registration
terminology as defined in {{!RFC9499}}.

The word "registry" is used in this document in two ways: to refer
to domain registries, as described in {{RFC9499}} and also to refer
to IANA registries in the IETF sense. When the intention is to refer
to an IANA registry, the phrase "IANA registry" is used.

{::boilerplate bcp14-tagged}


# DNSSEC Parameters in EPP

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
basis.

In particular, registries and registrars SHOULD NOT reject a value
solely because they do not themselves implement the corresponding
algorithm. A validator that does not support the algorithm or digest
type specified in a DS record disregards that record
({{Section 5.2 of !RFC4035}}, {{Section 5.2 of !RFC6840}}), so
accepting such values does not introduce a risk of resolution
failure.

A registrar is not expected to accept a value that the registry
for the corresponding domain name would reject.


## Values to Deny {#deny}

The values to be denied are derived from the current contents of
{{DNSKEY-IANA}} and {{DS-IANA}}, not from a fixed snapshot of those
IANA registries.

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


## Robustness of Implementations

Software that processes DS data, including registry and registrar
systems and systems that consume data published by them, may
encounter values it has not seen before. Such software needs to
handle unfamiliar algorithm and digest type values without failure,
for example by treating them as opaque numbers.


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

