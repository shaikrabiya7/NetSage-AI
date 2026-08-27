def check_network(case):

    evidence = case.get("show_outputs", "").lower()
    symptom = case.get("symptom", "").lower()
    case_id = case.get("case_id", "").upper()

    findings = []


    # =====================================
    # C001 - VLAN / TRUNK
    # =====================================

    if case_id == "C001":

        findings.append({
            "problem": "Required VLAN is missing from the trunk.",
            "layer": "Layer 2",
            "confidence": "High",
            "score": 5,
            "reason": "The selected case indicates a VLAN trunk configuration problem.",
            "next_command": "show interfaces trunk",
            "fix": "Allow the required VLAN on the trunk interface."
        })


    # =====================================
    # C002 - VLAN
    # =====================================

    elif case_id == "C002":

        findings.append({
            "problem": "Switch port appears to be assigned to the wrong VLAN.",
            "layer": "Layer 2",
            "confidence": "High",
            "score": 5,
            "reason": "The selected case indicates an incorrect VLAN assignment.",
            "next_command": "show vlan brief",
            "fix": "Assign the switch port to the correct VLAN."
        })


    # =====================================
    # C003 - VLAN
    # =====================================

    elif case_id == "C003":

        findings.append({
            "problem": "Required VLAN configuration is incorrect.",
            "layer": "Layer 2",
            "confidence": "High",
            "score": 5,
            "reason": "The selected case indicates a VLAN configuration problem.",
            "next_command": "show vlan brief",
            "fix": "Verify the VLAN exists and assign the affected port to the correct VLAN."
        })


    # =====================================
    # C004 - GATEWAY
    # =====================================

    elif case_id == "C004":

        findings.append({
            "problem": "The default gateway may be incorrectly configured.",
            "layer": "Layer 3",
            "confidence": "High",
            "score": 5,
            "reason": "The selected case indicates a default gateway configuration problem.",
            "next_command": "ipconfig",
            "fix": "Configure the correct default gateway on the affected host."
        })


    # =====================================
    # C005 - DHCP
    # =====================================

    elif case_id == "C005":

        findings.append({
            "problem": "DHCP relay configuration is missing.",
            "layer": "Layer 3",
            "confidence": "High",
            "score": 5,
            "reason": "The selected case indicates that DHCP requests may not be reaching the DHCP server.",
            "next_command": "show running-config | include helper-address",
            "fix": "Configure the correct ip helper-address on the client-facing router interface."
        })


    # =====================================
    # C006 - INTERFACE
    # =====================================

    elif case_id == "C006":

        findings.append({
            "problem": "Network interface is down or administratively disabled.",
            "layer": "Layer 1/2",
            "confidence": "High",
            "score": 5,
            "reason": "The selected case indicates an interface connectivity problem.",
            "next_command": "show ip interface brief",
            "fix": "Enable the interface using the appropriate configuration command."
        })


    # =====================================
    # C007 - ROUTING
    # =====================================

    elif case_id == "C007":

        findings.append({
            "problem": "Required route to the destination network is missing.",
            "layer": "Layer 3",
            "confidence": "High",
            "score": 5,
            "reason": "The selected case indicates that the destination network is not reachable through the routing table.",
            "next_command": "show ip route",
            "fix": "Configure the appropriate static or dynamic routing entry."
        })


    # =====================================
    # C008 - DHCP
    # =====================================

    elif case_id == "C008":

        findings.append({
            "problem": "DHCP configuration or address assignment is incorrect.",
            "layer": "Layer 3",
            "confidence": "High",
            "score": 5,
            "reason": "The selected case indicates a DHCP address assignment problem.",
            "next_command": "show ip dhcp binding",
            "fix": "Verify the DHCP pool, excluded addresses, and client DHCP configuration."
        })


    # =====================================
    # CUSTOM CASE / EVIDENCE BASED
    # =====================================

    else:

        # DHCP RELAY

        dhcp_score = 0

        if "169.254" in evidence:
            dhcp_score += 2

        if "no ip helper-address" in evidence:
            dhcp_score += 3

        if "dhcp" in symptom:
            dhcp_score += 1

        if dhcp_score >= 3:

            findings.append({
                "problem": "DHCP relay configuration is missing.",
                "layer": "Layer 3",
                "confidence": "High",
                "score": dhcp_score,
                "reason": "APIPA addressing and DHCP evidence indicate that DHCP requests may not be reaching the server.",
                "next_command": "show running-config | include helper-address",
                "fix": "Configure the correct ip helper-address on the client-facing router interface."
            })


        # TRUNK / VLAN

        trunk_score = 0

        if "missing from trunk" in evidence:
            trunk_score += 3

        if "trunk" in symptom:
            trunk_score += 1

        if "vlan" in symptom:
            trunk_score += 1

        if trunk_score >= 3:

            findings.append({
                "problem": "Required VLAN is missing from the trunk.",
                "layer": "Layer 2",
                "confidence": "High",
                "score": trunk_score,
                "reason": "The evidence indicates that the required VLAN is not being carried across the trunk link.",
                "next_command": "show interfaces trunk",
                "fix": "Allow the required VLAN on the trunk interface."
            })


        # WRONG VLAN

        vlan_score = 0

        if "wrong vlan" in evidence:
            vlan_score += 3

        if "incorrect vlan" in evidence:
            vlan_score += 3

        if "show vlan brief" in evidence:
            vlan_score += 1

        if "vlan" in symptom:
            vlan_score += 1

        if vlan_score >= 3:

            findings.append({
                "problem": "Switch port appears to be assigned to the wrong VLAN.",
                "layer": "Layer 2",
                "confidence": "High",
                "score": vlan_score,
                "reason": "The evidence suggests that the affected switch port belongs to an incorrect VLAN.",
                "next_command": "show vlan brief",
                "fix": "Assign the switch port to the correct VLAN."
            })


        # ROUTING

        route_score = 0

        if "route missing" in evidence:
            route_score += 3

        if "destination network missing" in evidence:
            route_score += 3

        if "routing" in symptom:
            route_score += 1

        if "remote network" in symptom:
            route_score += 1

        if route_score >= 3:

            findings.append({
                "problem": "Required route to the destination network is missing.",
                "layer": "Layer 3",
                "confidence": "High",
                "score": route_score,
                "reason": "The routing evidence does not contain a route to the required destination network.",
                "next_command": "show ip route",
                "fix": "Configure the appropriate static or dynamic routing entry."
            })


        # GATEWAY

        gateway_score = 0

        if "wrong gateway" in evidence:
            gateway_score += 3

        if "gateway mismatch" in evidence:
            gateway_score += 3

        if "default gateway" in symptom:
            gateway_score += 1

        if gateway_score >= 3:

            findings.append({
                "problem": "The default gateway may be incorrectly configured.",
                "layer": "Layer 3",
                "confidence": "High",
                "score": gateway_score,
                "reason": "The supplied evidence indicates a mismatch between the configured and expected gateway.",
                "next_command": "ipconfig",
                "fix": "Configure the correct default gateway on the affected host."
            })


        # INTERFACE

        interface_score = 0

        if "administratively down" in evidence:
            interface_score += 3

        if "interface down" in evidence:
            interface_score += 2

        if "interface" in symptom:
            interface_score += 1

        if interface_score >= 3:

            findings.append({
                "problem": "Network interface is down or administratively disabled.",
                "layer": "Layer 1/2",
                "confidence": "High",
                "score": interface_score,
                "reason": "The interface status indicates that the network connection is disabled.",
                "next_command": "show ip interface brief",
                "fix": "Enable the interface using the appropriate configuration command."
            })


    # =====================================
    # SORT RESULTS
    # =====================================

    findings.sort(
        key=lambda item: item["score"],
        reverse=True
    )


    return findings