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
This document provides recommendations to domain name registries and
registrars and recommends a liberal policy that allows new
algorithms to be adopted.

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
`<secDNS:dsData>` element that relate to the signing algorithm:

* `<secDNS:alg>` contains an algorithm value as described in
  {{section 5.1.2 of !RFC4034}}
* `<secDNS:digestType>` contains a digest type value as described in
  {{section 5.1.3 of !RFC4034}}

Requirements levels corresponding to the values of the `<secDNS:alg>`
and `<secDNS:digestType>` are managed according to {{!RFC9904}} and
current recommendations can be found in the corresponding IANA
registries {{DNSKEY-IANA}} and {{DS-IANA}}. Of particular relevance
to this document are the columns labelled "Implement for DNSSEC
Signing" and "Implement for DNSSEC Delegation".


# Recommendations for Registries and Registrars

Registries and registrars MAY allow any values for the `<secDNS:alg>`
and `<secDNS:digestType>` parameters. In other words, registries and
registrars MAY accept any values for these parameters that are
syntactically valid, regardless of the semantic meaning of those
parameters. This approach delegates responsibility for the choice
of values to registrants.

Alternatively, registries and registrars MAY constrain the values for the
`<secDNS:alg>` and `<secDNS:digestType>` parameters using a denylist
which allows all values by default, but denies values that
are marked "MUST NOT Implement for DNSSEC Signing" {{DNSKEY-IANA}} or
"MUST NOT Implement for DNSSEC Delegation" {{DS-IANA}}. Such
a denylist SHOULD be updated periodically in order to reflect changes
that are published in those registries.

Registries and Registrars SHOULD publish details of what values
they accept to allow registrants to make informed choices.


# Security Considerations {#security}

This document aims to make it easier for new cryptographic
algorithms to be used in DNSSEC, while accommodating the policy
needs of registries and registrars to exercise some measure
of control over algorithm choices.


# IANA Considerations {#iana}

This document has no IANA actions.


--- back

# Acknowledgments
{:numbered="false"}

Bas Westerbaan provided post-quantum energy. Scott Hollenbeck and
Gavin Brown provided welcome encouragement.

