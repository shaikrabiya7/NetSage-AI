def extract_evidence(text):

    text = text.lower()

    evidence = {
        "interface_status": "unknown",
        "protocol_status": "unknown",
        "vlan_status": "unknown",
        "trunk_status": "unknown",
        "route_status": "unknown",
        "dhcp_status": "unknown",
        "gateway_status": "unknown",
        "ip_address_status": "unknown"
    }

    # Interface
    if "administratively down" in text:
        evidence["interface_status"] = "administratively down"

    elif "interface is up" in text:
        evidence["interface_status"] = "up"

    # Protocol
    if "protocol is down" in text:
        evidence["protocol_status"] = "down"

    elif "protocol is up" in text:
        evidence["protocol_status"] = "up"

    # VLAN
    if "wrong vlan" in text or "incorrect vlan" in text:
        evidence["vlan_status"] = "incorrect"

    elif "vlan 30" in text and "missing" not in text:
        evidence["vlan_status"] = "present"

    # Trunk
    if "missing from trunk" in text:
        evidence["trunk_status"] = "vlan missing"

    elif "trunk" in text and "allowed" in text:
        evidence["trunk_status"] = "configured"

    # Routing
    if "route missing" in text or "destination network missing" in text:
        evidence["route_status"] = "missing"

    elif "route exists" in text:
        evidence["route_status"] = "present"

    # DHCP
    if "169.254" in text:
        evidence["ip_address_status"] = "apipa"

        evidence["dhcp_status"] = "possible dhcp failure"

    if "no ip helper-address" in text:
        evidence["dhcp_status"] = "relay missing"

    # Gateway
    if "wrong gateway" in text or "gateway mismatch" in text:
        evidence["gateway_status"] = "incorrect"

    return evidence