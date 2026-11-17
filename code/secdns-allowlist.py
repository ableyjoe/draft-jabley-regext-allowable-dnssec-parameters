#!/usr/bin/env python3
#
# Print allowlists for the EPP <secDNS:alg> and <secDNS:digestType>
# elements, derived from the current contents of the IANA
# registries as described in Section 4.2 of
# draft-jabley-regext-allowable-dnssec-parameters.

import json
import urllib.request
import xml.etree.ElementTree as ET

IANA = "https://www.iana.org/assignments/"
NS = {"i": "http://www.iana.org/assignments"}


def col(record, tag):
    return record.findtext("i:" + tag, "", NS).strip()


def alg_ok(r):
    # "Zone Signing" is "Y" and "Use for DNSSEC Validation" is
    # not "MUST NOT"; this admits the private algorithms
    return col(r, "signing") == "Y" and \
        col(r, "usevalid") != "MUST NOT"


def digest_ok(r):
    # "Use for DNSSEC Validation" contains a requirement level
    # other than "MUST NOT", or the value is for private use
    return col(r, "usevalid") not in ("", "MUST NOT") or \
        "private use" in col(r, "description").lower()


def allowlist(name, number, ok):
    url = IANA + name + "/" + name + ".xml"
    with urllib.request.urlopen(url) as f:
        root = ET.parse(f).getroot()
    # the table we want is the first sub-registry, "<name>-1"
    path = "i:registry[@id='" + name + "-1']/i:record"
    allow = []
    for r in root.iterfind(path, NS):
        if ok(r):
            lo, _, hi = col(r, number).partition("-")
            allow += range(int(lo), int(hi or lo) + 1)
    return {"updated": root.findtext("i:updated", "", NS),
            "allow": sorted(allow)}


print(json.dumps({
    "secDNS:alg":
        allowlist("dns-sec-alg-numbers", "number", alg_ok),
    "secDNS:digestType":
        allowlist("ds-rr-types", "value", digest_ok),
}, indent=2))
