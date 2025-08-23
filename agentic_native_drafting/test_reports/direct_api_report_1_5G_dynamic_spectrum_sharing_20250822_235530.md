# Direct Prior Art API Test Report

## Test Information
- **Query**: 5G dynamic spectrum sharing
- **Test Index**: 1
- **Timestamp**: 2025-08-22T23:55:30.746895
- **Duration**: 136.8 seconds
- **Total Results**: 20
- **Backend URL**: http://localhost:8000

## Search Results Summary
Found 20 relevant patents

## Patent Analysis Report


## Raw API Response
```json
{
  "query": "5G dynamic spectrum sharing",
  "total_results": 20,
  "results": [
    {
      "patent_id": "12069484",
      "title": "Base station supporting dynamic spectrum sharing between heterogeneous networks and wireless communication system including the same",
      "abstract": "The present disclosure provides a wireless communication system. The wireless communication system includes a base station and a user equipment. The base station is configured to support dynamic spectrum sharing (DSS) between a first network and a second network. The user equipment is configured to communicate with the base station based on the first network. The base station is further configured to puncture allocation of a first reference signal when performing resource allocation on a first control channel in a case where a resource to be allocated to the first reference signal corresponding to the first network overlaps with resource allocated to a second reference signal corresponding to the second network. The user equipment is further configured to receive the first control channel and perform channel estimation for the first network, taking into account the first reference signal that has been punctured.",
      "inventors": [
        "Jinho Kim",
        "Jungmin Park"
      ],
      "assignees": [
        "Samsung Electronics Co., Ltd."
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. A wireless communication system comprising:\na base station configured to support dynamic spectrum sharing (DSS) between a first network and a second network; and\na user equipment configured to communicate with the base station based on the first network,\nwherein the base station is further configured to puncture allocation of a first reference signal when performing resource allocation on a first control channel and when a first resource to be allocated to the first reference signal corresponding to the first network overlaps with a second resource allocated to a second reference signal corresponding to the second network, and\nwherein the user equipment is further configured to receive the first control channel and perform channel estimation for the first network based on the allocation of the first reference signal that has been punctured,\nwherein the base station is further configured to allow at least two time-frequency domains among a plurality of time-frequency domains to overlap with a time-frequency domain allocated to the first control channel of the first network when performing the resource allocation, the plurality of time-frequency domains respectively corresponding to a plurality of carriers of the second network,\nwherein the base station is further configured to puncture the first reference signal on the at least two time-frequency domains according to a same first puncturing pattern when performing the resource allocation, and\nwherein the base station is further configured to allocate, according to a second puncturing pattern, the first reference signal to a time-frequency domain of a guard band between the at least two time-frequency domains.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The wireless communication system of claim 1, wherein:\nthe first network includes a new radio (NR) network,\nthe second network includes a long-term evolution (LTE) network,\nthe first reference signal includes a demodulation reference signal (DMRS), and\nthe second reference signal includes a cell reference signal (CRS).",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The wireless communication system of claim 1, wherein the base station is further configured to allow one time-frequency domain among a plurality of time-frequency domains to overlap with a time-frequency domain allocated to the first control channel of the first network when performing the resource allocation, the plurality of time-frequency domains respectively corresponding to a plurality of carriers of the second network.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The wireless communication system of claim 1, wherein the user equipment is further configured to perform the channel estimation using the second puncturing pattern of the first reference signal allocated to the time-frequency domain of the guard band.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The wireless communication system of claim 1, wherein the user equipment is further configured to perform the channel estimation using a portion of the second puncturing pattern of the first reference signal allocated to the time-frequency domain of the guard band, excluding the first puncturing pattern.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. The wireless communication system of claim 1, wherein the base station is further configured to allocate the first reference signal to some resources among a plurality of consecutive resources on a time axis, the some resources being expected not to overlap with the second resource allocated to the second reference signal, and puncture allocation of the first reference signal in a remaining resource expected to overlap with the second resource allocated to the second reference signal.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The wireless communication system of claim 6, wherein the user equipment is further configured not to use the first reference signal allocated to the some resources, based on the puncture allocation of the first reference signal being punctured as in the remaining resource, when performing the channel estimation.",
          "claim_type": "dependent",
          "dependency": "claim 6",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The wireless communication system of claim 1, wherein, when a demodulation reference signal (DMRS) precoding unit of a second control channel is set to a second control channel allocation region, the base station is further configured to perform resource allocation on the second control channel such that the second resource allocated to the second reference signal does not overlap with the first resource to be allocated to the first reference signal; and\nwherein the user equipment is further configured to receive the second control channel and perform the channel estimation for the first network, taking into account that the first reference signal is not punctured.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. The wireless communication system of claim 1, wherein, when a plurality of second reference signal rate matching patterns applicable to a frequency domain corresponding to a certain carrier are set for resource allocation on a second control channel, the base station is further configured to perform the resource allocation on the second control channel such that the second resource allocated to the second reference signal does not overlap with the first resource to be allocated to the first reference signal; and\nwherein the user equipment is further configured to receive the second control channel and perform the channel estimation for the first network based on the first reference signal not being punctured.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. The wireless communication system of claim 1, wherein the base station is further configured to perform the resource allocation on the first control channel based on a number of supported punctured first reference signal patterns the user equipment supports.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. The wireless communication system of claim 10, wherein the user equipment is further configured to transmit the number of supported punctured first reference signal patterns to the base station via radio resource control (RRC) signaling.",
          "claim_type": "dependent",
          "dependency": "claim 10",
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. An operating method of a base station supporting dynamic spectrum sharing (DSS) between a first network and a second network, the operating method comprising:\ndetermining, based on communication settings, that a first resource element is allocated to a first reference signal corresponding to the first network and to a second reference signal corresponding to the second network; and\nperforming resource allocation on a control channel with a puncture of allocation of the first resource to the first reference signal in response to the determination.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. The operating method of claim 12, wherein determining whether to allow the overlap comprises determining not to allow the overlap when a demodulation reference signal (DMRS) precoding unit of the control channel is set to a control channel allocation region in the communication settings, and\nwherein performing resource allocation on the control channel comprises allocating the first reference signal to a different resource than the second resource allocated to the second reference signal in response to the determination not to allow the overlap.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. The operating method of claim 12, wherein determining whether to allow the overlap comprises determining not to allow the overlap when a plurality of second reference signal rate matching patterns applicable to a frequency domain corresponding to a certain carrier are set in the communication settings; and\nwherein performing resource allocation on the control channel comprises allocating different resources to the first reference signal and the second reference signal, respectively, in response to the determination not to allow the overlap.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00015",
          "claim_text": "15. A wireless communication system comprising:\na base station configured to support dynamic spectrum sharing (DSS) between a first network and a second network; and\na user equipment configured to communicate with the base station based on the first network,\nwherein the base station is further configured to puncture allocation of a first reference signal when performing resource allocation on a first control channel and when a first resource to be allocated to the first reference signal corresponding to the first network overlaps with a second resource allocated to a second reference signal corresponding to the second network, and\nwherein the user equipment is further configured to receive the first control channel and perform channel estimation for the first network based on the allocation of the first reference signal that has been punctured,\nwherein the base station is further configured to perform the resource allocation on the first control channel based on a number of supported punctured first reference signal patterns the user equipment supports.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.9,
      "publication_date": "2024-08-20",
      "patent_year": 2024
    },
    {
      "patent_id": "12192952",
      "title": "Efficient positioning enhancement for dynamic spectrum sharing",
      "abstract": "Techniques are provided for transmitting Positioning Reference Signals (PRSs) in cells supporting two different Radio Access Technologies (RATs), where the two RATs (e.g. 4G LTE and 5G NR) employ dynamic spectrum sharing. To avoid interference between the PRSs and between the two RATs, the PRSs may be time aligned to the same set of PRS positioning occasions, and may be assigned orthogonal characteristics such as different muting patterns, orthogonal code sequences, different frequency shifts or different frequency hopping. UEs supporting both RATs may be enabled to measure PRSs for both RATs. UEs supporting only one RAT (e.g. 4G LTE) may be enabled to measure PRSs for just this RAT. A location server such as an LMF, E-SMLC or SLP may provide assistance data to UEs, and request measurements from UEs, for PRSs in one or both RATs.",
      "inventors": [
        "Stephen William Edge",
        "Bapineedu Chowdary Gummadi",
        "Hem Agnihotri"
      ],
      "assignees": [
        "QUALCOMM Incorporated"
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. A method, at a network server, to support positioning of a mobile device with dynamic spectrum sharing, comprising:\nreceiving a first set of location measurements obtained by the mobile device for first positioning reference signals (PRSs) transmitted in a first plurality of cells, the first plurality of cells using a first radio access technology (RAT);\nreceiving a second set of location measurements obtained by the mobile device for second PRSs transmitted in a second plurality of cells, the second plurality of cells using a second RAT, wherein the first RAT and the second RAT are different radio access technologies operating on the same radio frequency band, with the first set of location measurements corresponding to first PRS positioning occasions of the first PRSs scheduled for occurrence at the same time with second PRS positioning occasions of the second PRSs corresponding to the second set of location measurements; and\ndetermining a location of the mobile device based at least in part on the first set of location measurements and the second set of location measurements.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The method of claim 1, wherein the first RAT is 4G Long Term Evolution (LTE) and the second RAT is 5G New Radio (NR).",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The method of claim 1, wherein the network server comprises a Location Management Function (LMF), an Enhanced Serving Mobile Location Center (E-SMLC), or a Secure User Plane Location (SUPL) Location Platform (SLP).",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The method of claim 1, wherein the first set of location measurements and the second set of location measurements each comprise measurements comprising at least one of a Time of Arrival (TOA), a Received Signal Strength Indication (RSSI), a Round Trip signal propagation Time (RTT), a Reference Signal Time Difference (RSTD), a Reference Signal Received Power (RSRP), a Receive Time-Transmission Time difference (Rx-Tx), a Reference Signal Received Quality (RSRQ), or some combination of these.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The method of claim 1, wherein each PRS in the first PRSs and the second PRSs comprises a sequence of PRS positioning occasions, wherein the sequence of PRS positioning occasions for each PRS occur at the same times as the sequence of PRS positioning occasions for each of other PRSs in the first PRSs and the second PRSs.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. The method of claim 1, wherein each PRS in the first PRSs and the second PRSs includes orthogonal characteristics, wherein the orthogonal characteristics reduce interference between the each PRS and other PRSs in the first PRSs and the second PRSs.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The method of claim 6, wherein the orthogonal characteristics include at least one of a distinct frequency shift, an orthogonal PRS code sequence, a distinct frequency hopping sequence, a distinct muting pattern, or some combination of these.",
          "claim_type": "dependent",
          "dependency": "claim 6",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The method of claim 6, wherein the orthogonal characteristics include a distinct muting pattern, wherein the each PRS is transmitted during PRS positioning occasions in which PRS is not transmitted for some other PRSs in the first PRSs and the second PRSs, wherein the each PRS is not transmitted during PRS positioning occasions in which PRS is transmitted for at least some of the some other PRSs in the first PRSs and the second PRSs.",
          "claim_type": "dependent",
          "dependency": "claim 6",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. The method of claim 8, further comprising sending assistance data to the mobile device, the assistance data including a configuration of each PRS in the first PRSs and the second PRSs, the configuration including an indication of the PRS positioning occasions and the orthogonal characteristics for the each PRS, wherein the first set of location measurements and the second set of location measurements are obtained by the mobile device based in part on the configuration of each PRS in the first PRSs and the second PRSs.",
          "claim_type": "dependent",
          "dependency": "claim 8",
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. The method of claim 1, wherein the radio frequency band includes frequencies in a range of 600 MHz to 700 MHz or in a range of 2.5 GHz to 3.5 GHz.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. An apparatus, comprising:\na memory;\na transceiver;\na processor communicatively coupled to the memory and the transceiver and configured to:\nreceive a first set of location measurements obtained by a mobile device for first positioning reference signals (PRSs) transmitted in a first plurality of cells, the first plurality of cells using a first radio access technology (RAT);\nreceive a second set of location measurements obtained by the mobile device for second PRSs transmitted in a second plurality of cells, the second plurality of cells using a second RAT, wherein the first RAT and the second RAT are different radio access technologies operating on the same radio frequency band, with the first set of location measurements corresponding to first PRS positioning occasions of the first PRSs scheduled for occurrence at the same time with second PRS positioning occasions of the second PRSs corresponding to the second set of location measurements; and\ndetermine a location of the mobile device based at least in part on the first set of location measurements and the second set of location measurements.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. The apparatus of claim 11 wherein the first RAT is 4G Long Term Evolution (LTE) and the second RAT is 5G New Radio (NR).",
          "claim_type": "dependent",
          "dependency": "claim 11",
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. The apparatus of claim 11, wherein the apparatus comprises a Location Management Function (LMF), an Enhanced Serving Mobile Location Center (E-SMLC), or a Secure User Plane Location (SUPL) Location Platform (SLP).",
          "claim_type": "dependent",
          "dependency": "claim 11",
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. The apparatus of claim 11, wherein the first set of location measurements and the second set of location measurements each comprise measurements comprising at least one of a Time of Arrival (TOA), a Received Signal Strength Indication (RSSI), a Round Trip signal propagation Time (RTT), a Reference Signal Time Difference (RSTD), a Reference Signal Received Power (RSRP), a Receive Time-Transmission Time difference (Rx-Tx), a Reference Signal Received Quality (RSRQ), or some combination of these.",
          "claim_type": "dependent",
          "dependency": "claim 11",
          "is_exemplary": true
        },
        {
          "claim_number": "00015",
          "claim_text": "15. The apparatus of claim 11, wherein each PRS in the first PRSs and the second PRSs comprises a sequence of PRS positioning occasions, wherein the sequence of PRS positioning occasions for each PRS occur at the same times as the sequence of PRS positioning occasions for each of other PRSs in the first PRSs and the second PRSs.",
          "claim_type": "dependent",
          "dependency": "claim 11",
          "is_exemplary": true
        },
        {
          "claim_number": "00016",
          "claim_text": "16. The apparatus of claim 11, wherein each PRS in the first PRSs and the second PRSs includes orthogonal characteristics, wherein the orthogonal characteristics reduce interference between the each PRS and other PRSs in the first PRSs and the second PRSs.",
          "claim_type": "dependent",
          "dependency": "claim 11",
          "is_exemplary": true
        },
        {
          "claim_number": "00017",
          "claim_text": "17. The apparatus of claim 16, wherein the orthogonal characteristics include at least one of a distinct frequency shift, an orthogonal PRS code sequence, a distinct frequency hopping sequence, a distinct muting pattern, or some combination of these.",
          "claim_type": "dependent",
          "dependency": "claim 16",
          "is_exemplary": true
        },
        {
          "claim_number": "00018",
          "claim_text": "18. The apparatus of claim 16, wherein the orthogonal characteristics include a distinct muting pattern, wherein the each PRS is transmitted during PRS positioning occasions in which PRS is not transmitted for some other PRSs in the first PRSs and the second PRSs, wherein the each PRS is not transmitted during PRS positioning occasions in which PRS is transmitted for at least some of the some other PRSs in the first PRSs and the second PRSs.",
          "claim_type": "dependent",
          "dependency": "claim 16",
          "is_exemplary": true
        },
        {
          "claim_number": "00019",
          "claim_text": "19. The apparatus of claim 18, wherein the processor is further configured to send assistance data to the mobile device, the assistance data including a configuration of each PRS in the first PRSs and the second PRSs, the configuration including an indication of the sequence of PRS positioning occasions and the orthogonal characteristics for the each PRS, wherein the first set of location measurements and the second set of location measurements are obtained by the mobile device based in part on the configuration of each PRS in the first PRSs and the second PRSs.",
          "claim_type": "dependent",
          "dependency": "claim 18",
          "is_exemplary": true
        },
        {
          "claim_number": "00020",
          "claim_text": "20. The apparatus of claim 11, wherein the radio frequency band includes frequencies in a range of 600 MHz to 700 MHz or in a range of 2.5 GHz to 3.5 GHZ.",
          "claim_type": "dependent",
          "dependency": "claim 11",
          "is_exemplary": true
        },
        {
          "claim_number": "00021",
          "claim_text": "21. An apparatus, comprising:\nmeans for receiving a first set of location measurements obtained by a mobile device for first positioning reference signals (PRSs) transmitted in a first plurality of cells, the first plurality of cells using a first radio access technology (RAT);\nmeans for receiving a second set of location measurements obtained by the mobile device for second PRSs transmitted in a second plurality of cells, the second plurality of cells using a second RAT, wherein the first RAT and the second RAT are different radio access technologies operating on the same radio frequency band, with the first set of location measurements corresponding to first PRS positioning occasions of the first PRSs scheduled for occurrence at the same time with second PRS positioning occasions of the second PRSs corresponding to the second set of location measurements; and\nmeans for determining a location of the mobile device based at least in part on the first set of location measurements and the second set of location measurements.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00022",
          "claim_text": "22. The apparatus of claim 21, wherein the first RAT is 4G Long Term Evolution (LTE) and the second RAT is 5G New Radio (NR).",
          "claim_type": "dependent",
          "dependency": "claim 21",
          "is_exemplary": true
        },
        {
          "claim_number": "00023",
          "claim_text": "23. The apparatus of claim 21, wherein the apparatus comprises a Location Management Function (LMF), an Enhanced Serving Mobile Location Center (E-SMLC), or a Secure User Plane Location (SUPL) Location Platform (SLP).",
          "claim_type": "dependent",
          "dependency": "claim 21",
          "is_exemplary": true
        },
        {
          "claim_number": "00024",
          "claim_text": "24. The apparatus of claim 21, wherein the first set of location measurements and the second set of location measurements each comprise measurements comprising at least one of a Time of Arrival (TOA), a Received Signal Strength Indication (RSSI), a Round Trip signal propagation Time (RTT), a Reference Signal Time Difference (RSTD), a Reference Signal Received Power (RSRP), a Receive Time-Transmission Time difference (Rx-Tx), a Reference Signal Received Quality (RSRQ), or some combination of these.",
          "claim_type": "dependent",
          "dependency": "claim 21",
          "is_exemplary": true
        },
        {
          "claim_number": "00025",
          "claim_text": "25. The apparatus of claim 21, wherein each PRS in the first PRSs and the second PRSs comprises a sequence of PRS positioning occasions, wherein the sequence of PRS positioning occasions for each PRS occur at the same times as the sequence of PRS positioning occasions for each of other PRSs in the first PRSs and the second PRSs.",
          "claim_type": "dependent",
          "dependency": "claim 21",
          "is_exemplary": true
        },
        {
          "claim_number": "00026",
          "claim_text": "26. The apparatus of claim 21, wherein each PRS in the first PRSs and the second PRSs includes orthogonal characteristics, wherein the orthogonal characteristics reduce interference between the each PRS and other PRSs in the first PRSs and the second PRSs.",
          "claim_type": "dependent",
          "dependency": "claim 21",
          "is_exemplary": true
        },
        {
          "claim_number": "00027",
          "claim_text": "27. The apparatus of claim 26, wherein the orthogonal characteristics include at least one of a distinct frequency shift, an orthogonal PRS code sequence, a distinct frequency hopping sequence, a distinct muting pattern, or some combination of these.",
          "claim_type": "dependent",
          "dependency": "claim 26",
          "is_exemplary": true
        },
        {
          "claim_number": "00028",
          "claim_text": "28. The apparatus of claim 26, wherein the orthogonal characteristics include a distinct muting pattern, wherein the each PRS is transmitted during PRS positioning occasions in which PRS is not transmitted for some other PRSs in the first PRSs and the second PRSs, wherein the each PRS is not transmitted during PRS positioning occasions in which PRS is transmitted for at least some of the some other PRSs in the first PRSs and the second PRSs.",
          "claim_type": "dependent",
          "dependency": "claim 26",
          "is_exemplary": true
        },
        {
          "claim_number": "00029",
          "claim_text": "29. The apparatus of claim 28, further comprising means for sending assistance data to the mobile device, the assistance data including a configuration of each PRS in the first PRSs and the second PRSs, the configuration including an indication of the sequence of PRS positioning occasions and the orthogonal characteristics for the each PRS, wherein the first set of location measurements and the second set of location measurements are obtained by the mobile device based in part on the configuration of each PRS in the first PRSs and the second PRSs.",
          "claim_type": "dependent",
          "dependency": "claim 28",
          "is_exemplary": true
        },
        {
          "claim_number": "00030",
          "claim_text": "30. The apparatus of claim 21, wherein the radio frequency band includes frequencies in a range of 600 MHz to 700 MHz or in a range of 2.5 GHz to 3.5 GHz.",
          "claim_type": "dependent",
          "dependency": "claim 21",
          "is_exemplary": true
        },
        {
          "claim_number": "00031",
          "claim_text": "31. A non-transitory processor-readable storage medium comprising processor-readable instructions configured to cause one or more processors to support positioning of a mobile device with dynamic spectrum sharing, comprising:\ncode for receiving a first set of location measurements obtained by the mobile device for first positioning reference signals (PRSs) transmitted in a first plurality of cells, the first plurality of cells using a first radio access technology (RAT);\ncode for receiving a second set of location measurements obtained by the mobile device for second PRSs transmitted in a second plurality of cells, the second plurality of cells using a second RAT, wherein the first RAT and the second RAT are different radio access technologies operating on the same radio frequency band, with the first set of location measurements corresponding to first PRS positioning occasions of the first PRSs scheduled for occurrence at the same time with second PRS positioning occasions of the second PRSs corresponding to the second set of location measurements; and\ncode for determining a location of the mobile device based at least in part on the first set of location measurements and the second set of location measurements.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00032",
          "claim_text": "32. The non-transitory processor-readable storage medium of claim 31, further comprising code for sending assistance data to the mobile device, the assistance data including a configuration of each PRS in the first PRSs and the second PRSs, the configuration including an indication of a sequence of PRS positioning occasions and orthogonal characteristics for the each PRS, wherein the first set of location measurements and the second set of location measurements are obtained by the mobile device based in part on the configuration of each PRS in the first PRSs and the second PRSs.",
          "claim_type": "dependent",
          "dependency": "claim 31",
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.8,
      "publication_date": "2025-01-07",
      "patent_year": 2025
    },
    {
      "patent_id": "12063645",
      "title": "Scheduling restriction enhancements for LTE and 5G NR dynamic spectrum sharing",
      "abstract": "Methods and devices for a base station acting as a primary cell to perform dual spectrum sharing (DSS) with a first user equipment device (UE) over a 5G NR connection and a second UE over an LTE connection. The first UE establishes the 5G NR connection with the primary cell and one or more secondary cells. One of the secondary cells is configured in the 5G NR connection to provide downlink control information to the UE for the primary cell, to avoid collisions by the primary cell with LTE control transmissions.",
      "inventors": [
        "Hong He",
        "Chunhai Yao",
        "Sigen Ye",
        "Dawei Zhang",
        "Chunxuan Ye",
        "Weidong Yang",
        "Wei Zeng",
        "Yushu Zhang",
        "Oghenekome Oteri",
        "Huaning Niu",
        "Haitong Sun",
        "Wei Zhang"
      ],
      "assignees": [
        "Apple Inc."
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. A method comprising:\nby a base station:\nestablishing a connection as a primary cell with a user equipment device (UE);\nproviding a first indication to the UE to monitor a common search space (CSS) for first downlink control information (DCI) from the primary cell, wherein the first DCI is for scheduling of the primary cell for the UE;\nproviding a second indication to the UE to monitor a UE-specific search space (USS) for second DCI from a secondary cell, wherein the second DCI is for cross-carrier scheduling to the primary cell for the UE, wherein the second DCI has a 5G NR DCI format of 0_1, 0_2, 1_1 or 1_2, and wherein, regardless of a monitoring capability of the UE, all physical downlink control channel (PDCCH) monitoring occasions on the secondary cell for DCIs for cross-carrier scheduling to the primary cell for the UE are constrained to be within an initial three symbols of a slot; and\n\noperating the connection according to the first DCI and the second DCI.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The method of claim 1, wherein the connection with the UE utilizes a 5th Generation New Radio (5G NR) radio access technology (RAT), wherein the method further comprises:\nestablishing a second connection with a second UE using a Long Term Evolution (LTE) RAT, wherein the first DCI is scheduled to not overlap with third DCI transmitted for the second connection.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The method of claim 2,\nwherein the base station communicates with the UE and the second UE using a 15 kHz subcarrier spacing, and\nwherein the secondary cell communicates with the UE using either the 15 kHz or a 30 kHz subcarrier spacing.",
          "claim_type": "dependent",
          "dependency": "claim 2",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The method of claim 1, further comprising:\nproviding a third indication to the UE to monitor the USS for third DCI from the secondary cell, wherein the third DCI schedules a communication with a second secondary cell.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The method of claim 1,\nwherein operating the connection according to the first DCI and the second DCI comprises one or more of:\nreceiving one or more uplink communications from the UE according to scheduling information of the first DCI or the second DCI;\ntransmitting one or more downlink communications to the UE according to the scheduling information of the first DCI or the second DCI.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. The method of claim 1,\nwherein the first DCI has:\na 5th Generation New Radio (5G NR) fallback DCI format of 0_0 or 1_0; or\na 5G NR special DCI format of 2_0, 2_1, 2_2, 2_3, 2_4, 2_5 or 2_6.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The method of claim 1,\nwherein the first DCI has:\na 5th Generation New Radio (5G NR) fallback DCI format of 0_0 or 1_0.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The method of claim 1,\nwherein the first indication and the second indication comprise one or more radio resource control (RRC) configuration messages.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. The method of claim 1,\nwherein the first DCI and the second DCI each comprise one or more of:\na scheduling indication for an uplink communication with the primary cell;\na scheduling indication for a downlink communication with the primary cell; and\na control message indicating a behavior modification of the UE.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. A base station, comprising:\na radio;\na processor communicatively coupled to the radio, wherein the base station is configured to:\nestablish a connection as a primary cell with a user equipment device (UE);\nprovide a first indication to the UE to monitor a common search space (CSS) for first downlink control information (DCI) from the primary cell, wherein the first DCI is for scheduling of the primary cell for the UE;\nprovide a second indication to the UE to monitor a UE-specific search space (USS) for second DCI from a secondary cell, wherein the second DCI is for cross-carrier scheduling to the primary cell for the UE, and wherein the second DCI has a 5G NR DCI format of 0_1, 0_2, 1_1 or 1_2, wherein, regardless of a monitoring capability of the UE, all physical downlink control channel (PDCCH) monitoring occasions on the secondary cell for DCIs for cross-carrier scheduling to the primary cell for the UE are constrained to be within an initial three symbols of a slot; and\noperate the connection according to the first DCI and the second DCI.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. The base station of claim 10, wherein the connection with the UE utilizes a 5th Generation New Radio (5G NR) radio access technology (RAT), wherein the base station is further configured to:\nestablish a second connection with a second UE using a Long Term Evolution (LTE) RAT, wherein the first DCI is scheduled to not overlap with third DCI transmitted for the second connection.",
          "claim_type": "dependent",
          "dependency": "claim 10",
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. An apparatus, comprising:\na processor configured to cause a base station to:\nestablish a connection as a primary cell with a user equipment device (UE);\nprovide a first indication to the UE to monitor a common search space (CSS) for first downlink control information (DCI) from the primary cell, wherein the first DCI is for scheduling of the primary cell for the UE;\nprovide a second indication to the UE to monitor a UE-specific search space (USS) for second DCI from a secondary cell, wherein the second DCI is for cross-carrier scheduling to the primary cell for the UE, and wherein the second DCI has a 5G NR DCI format of 0_1, 0_2, 1_1 or 1_2, wherein, regardless of a monitoring capability of the UE, all physical downlink control channel (PDCCH) monitoring occasions on the secondary cell for DCIs for cross-carrier scheduling to the primary cell for the UE are constrained to be within an initial three symbols of a slot; and\noperate the connection according to the first DCI and the second DCI.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. The apparatus of claim 12, wherein the connection with the UE utilizes a 5th Generation New Radio (5G NR) radio access technology (RAT), wherein the processor is further configured to cause the base station to:\nestablish a second connection with a second UE using a Long Term Evolution (LTE) RAT, wherein the first DCI is scheduled to not overlap with third DCI transmitted for the second connection.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. The apparatus of claim 13,\nwherein the base station communicates with the UE and the second UE using a 15 kHz subcarrier spacing, and\nwherein the secondary cell communicates with the UE using either the 15 kHz or a 30 kHz subcarrier spacing.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00015",
          "claim_text": "15. The apparatus of claim 12, wherein the base station is further configured to:\nprovide a third indication to the UE to monitor the USS for third DCI from the secondary cell, wherein the third DCI schedules a communication with a second secondary cell.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00016",
          "claim_text": "16. The apparatus of claim 12,\nwherein in operating the connection according to the first DCI and the second DCI, the processor is further configured to cause the base station to:\nreceive one or more uplink communications from the UE according to scheduling information of the first DCI or the second DCI;\ntransmit one or more downlink communications to the UE according to the scheduling information of the first DCI or the second DCI.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00017",
          "claim_text": "17. The apparatus of claim 12,\nwherein the first DCI has:\na 5th Generation New Radio (5G NR) fallback DCI format of 0_0 or 1_0; or\na 5G NR special DCI format of 2_0, 2_1, 2_2, 2_3, 2_4, 2_5 or 2_6.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00018",
          "claim_text": "18. The apparatus of claim 12,\nwherein the first DCI has:\na 5th Generation New Radio (5G NR) fallback DCI format of 0_0 or 1_0.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00019",
          "claim_text": "19. The apparatus of claim 12,\nwherein the first indication and the second indication comprise one or more radio resource control (RRC) configuration messages.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00020",
          "claim_text": "20. The apparatus of claim 12,\nwherein the first DCI and the second DCI each comprise one or more of:\na scheduling indication for an uplink communication with the primary cell;\na scheduling indication for a downlink communication with the primary cell; and\na control message indicating a behavior modification of the UE.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.8,
      "publication_date": "2024-08-13",
      "patent_year": 2024
    },
    {
      "patent_id": "11888610",
      "title": "Method and apparatus for positioning with LTE-NR dynamic spectrum sharing (DSS)",
      "abstract": "A user equipment (UE) is configured to be connected to a 5G New Radio (NR) network that shares one or more frequency bands using dynamic spectrum sharing (DSS) with a Long Term Evolution (LTE) network that is transmitting LTE positioning reference signal (PRS). The UE may receive LTE PRS rate matching information from the NR network, such as the LTE PRS configuration data or an LTE PRS rate matching pattern. The UE may decode and process NR data signals and control signals transmitted by the NR network while LTE PRS is transmitted by rate matching around the LTE PRS in accordance with the LTE PRS rate matching information. The LTE PRS muting pattern may be adjusted based on NR data or control signals, and the UE may receive and process NR data and control signals transmitted while the LTE PRS is muted.",
      "inventors": [
        "Akash Kumar",
        "Amit Jain",
        "Hargovind Prasad BANSAL"
      ],
      "assignees": [
        "QUALCOMM Incorporated"
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. A method for wireless communications performed by a user equipment (UE) connected to a New Radio (NR) network, the method comprising:\nreceiving, from an entity in the NR network, an NR signal comprising Long Term Evolution (LTE) positioning reference signal (PRS) rate matching information for dynamic LTE PRS transmitted by a first base station in an LTE network in one or more frequency bands shared by the NR network using dynamic spectrum sharing (DSS), wherein the LTE PRS rate matching information comprises an LTE PRS rate matching pattern;\nreceiving NR data signals and control signals transmitted by a second base station in the NR network and the dynamic LTE PRS transmitted by the first base station in the LTE network on the one or more frequency bands; and\ndecoding and processing the NR data signals and control signals from the second base station in the NR network by rate matching around the dynamic LTE PRS in accordance with the LTE PRS rate matching information, wherein rate matching around the dynamic LTE PRS in accordance with the LTE PRS rate matching information comprises applying the LTE PRS rate matching pattern to the NR data signals and control signals to receive NR data.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The method of claim 1, wherein the NR data signals and control signals transmitted by the second base station in the NR network comprise at least one of physical downlink shared channel (PDSCH) transmissions, physical downlink common channel (PDCCH) transmissions, Synchronization Signal Block (SSB) transmissions, or a combination thereof.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The method of claim 1, wherein the LTE PRS rate matching information comprises LTE PRS configuration data to enable the UE to perform PRS positioning measurements.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The method of claim 3, wherein the LTE PRS configuration data comprises one or more of carrier frequency, carrier bandwidth, a number of consecutive PRS sub-frames, a PRS periodicity, a PRS configuration index, a muting pattern, or a combination thereof.",
          "claim_type": "dependent",
          "dependency": "claim 3",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The method of claim 1, further comprising:\ntransmitting an indication to the entity in the NR network of a capability of rate matching around the dynamic LTE PRS in DSS, prior to receiving the LTE PRS rate matching information.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. The method of claim 1, further comprising:\nreceiving a muting pattern for the dynamic LTE PRS or a regularly scheduled LTE PRS in the LTE PRS rate matching information, wherein the muting pattern is at least partly based on a Synchronization Signal Block (SSB) periodicity from the NR network; and\nreceiving SSB transmissions from the second base station in the NR network while the dynamic LTE PRS or the regularly scheduled LTE PRS transmitted by the first base station in the LTE network is muted.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The method of claim 6, further comprising:\nmuting the dynamic LTE PRS or the regularly scheduled LTE PRS for at least two symbols in a physical resource block (PRB) transmitted by the first base station in the LTE network to leave at least four consecutive symbols available for SSB transmissions in the PRB transmitted by the second base station in the NR network.",
          "claim_type": "dependent",
          "dependency": "claim 6",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. A user equipment (UE) configured for wireless communications with a New Radio (NR) network, the UE comprising:\na wireless transceiver configured to wirelessly communicate with network entities in a wireless communication system;\nat least one memory; and\nat least one processor coupled to the wireless transceiver and the at least one memory, wherein the at least one processor is configured to:\nreceive, from an entity in the NR network via the wireless transceiver, an NR signal comprising Long Term Evolution (LTE) positioning reference signal (PRS) rate matching information for dynamic LTE PRS transmitted by a first base station in an LTE network in one or more frequency bands shared by the NR network using dynamic spectrum sharing (DSS), wherein the LTE PRS rate matching information comprises an LTE PRS rate matching pattern;\nreceive, via the wireless transceiver, NR data signals and control signals transmitted by a second base station in the NR network and the dynamic LTE PRS transmitted by the first base station in the LTE network on the one or more frequency bands; and\ndecode and process the NR data signals and control signals from the second base station in the NR network, wherein, to decode and process the NR data signals and control signals from the second base station in the NR network, the at least one processor is configured to rate match around the dynamic LTE PRS in accordance with the LTE PRS rate matching information, wherein, to rate match around the dynamic LTE PRS in accordance with the LTE PRS rate matching information, the at least one processor is configured to apply the LTE PRS rate matching pattern to the NR data signals and control signals to receive NR data.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. The UE of claim 8, wherein the NR data signals and control signals transmitted by the second base station in the NR network comprise at least one of physical downlink shared channel (PDSCH) transmissions, physical downlink common channel (PDCCH) transmissions, Synchronization Signal Block (SSB) transmissions, or a combination thereof.",
          "claim_type": "dependent",
          "dependency": "claim 8",
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. The UE of claim 8, wherein the LTE PRS rate matching information comprises LTE PRS configuration data to enable the UE to perform PRS positioning measurements.",
          "claim_type": "dependent",
          "dependency": "claim 8",
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. The UE of claim 10, wherein the LTE PRS configuration data comprises one or more of carrier frequency, carrier bandwidth, a number of consecutive PRS sub-frames, a PRS periodicity, a PRS configuration index, a muting pattern, or a combination thereof.",
          "claim_type": "dependent",
          "dependency": "claim 10",
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. The UE of claim 8, wherein the at least one processor is further configured to:\ntransmit, via the wireless transceiver, an indication to the entity in the NR network of a capability of rate matching around the dynamic LTE PRS in DSS, prior to receiving the LTE PRS rate matching information.",
          "claim_type": "dependent",
          "dependency": "claim 8",
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. The UE of claim 8, wherein the at least one processor is further configured to:\nreceive, via the wireless transceiver, a muting pattern for the dynamic LTE PRS or a regularly scheduled LTE PRS in the LTE PRS rate matching information, wherein the muting pattern is at least partly based on a Synchronization Signal Block (SSB) periodicity from the NR network; and\nreceive, via the wireless transceiver, SSB transmissions from the second base station in the NR network while the dynamic LTE PRS or the regularly scheduled LTE PRS transmitted by the first base station in the LTE network is muted.",
          "claim_type": "dependent",
          "dependency": "claim 8",
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. The UE of claim 13, wherein the at least one processor is further configured to:\nmute the dynamic LTE PRS or the regularly scheduled LTE PRS for at least two symbols in a physical resource block (PRB) transmitted by the first base station in the LTE network to leave at least four consecutive symbols available for SSB transmissions in the PRB transmitted by the second base station in the NR network.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00015",
          "claim_text": "15. A user equipment (UE) configured for wireless communications with a New Radio (NR) network, the UE comprising:\nmeans for receiving, from an entity in the NR network, an NR signal comprising Long Term Evolution (LTE) positioning reference signal (PRS) rate matching information for dynamic LTE PRS transmitted by a first base station in an LTE network in one or more frequency bands shared by the NR network using dynamic spectrum sharing (DSS), wherein the LTE PRS rate matching information comprises an LTE PRS rate matching pattern;\nmeans for receiving NR data signals and control signals transmitted by a second base station in the NR network and the dynamic LTE PRS transmitted by the base station in the LTE network on the one or more frequency bands; and\nmeans for decoding and processing the NR data signals and control signals from the second base station in the NR network configured to rate match around the dynamic LTE PRS in accordance with the LTE PRS rate matching information, wherein the means for rate matching around the dynamic LTE PRS in accordance with the LTE PRS rate matching information is configured to apply the LTE PRS rate matching pattern to the NR data signals and control signals to receive NR data.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00016",
          "claim_text": "16. The UE of claim 15, wherein the NR data signals and control signals transmitted by the second base station in the NR network comprise at least one of physical downlink shared channel (PDSCH) transmissions, physical downlink common channel (PDCCH) transmissions, Synchronization Signal Block (SSB) transmissions, or a combination thereof.",
          "claim_type": "dependent",
          "dependency": "claim 15",
          "is_exemplary": true
        },
        {
          "claim_number": "00017",
          "claim_text": "17. The UE of claim 15, wherein the LTE PRS rate matching information comprises LTE PRS configuration data to enable the UE to perform PRS positioning measurements.",
          "claim_type": "dependent",
          "dependency": "claim 15",
          "is_exemplary": true
        },
        {
          "claim_number": "00018",
          "claim_text": "18. The UE of claim 17, wherein the LTE PRS configuration data comprises one or more of carrier frequency, carrier bandwidth, a number of consecutive PRS sub-frames, a PRS periodicity, a PRS configuration index, a muting pattern, or a combination thereof.",
          "claim_type": "dependent",
          "dependency": "claim 17",
          "is_exemplary": true
        },
        {
          "claim_number": "00019",
          "claim_text": "19. The UE of claim 15, further comprising:\nmeans for transmitting an indication to the entity in the NR network of a capability of rate matching around the dynamic LTE PRS in DSS, prior to receiving the LTE PRS rate matching information.",
          "claim_type": "dependent",
          "dependency": "claim 15",
          "is_exemplary": true
        },
        {
          "claim_number": "00020",
          "claim_text": "20. The UE of claim 15, further comprising:\nmeans for receiving a muting pattern for the dynamic LTE PRS or a regularly scheduled LTE PRS in the LTE PRS rate matching information, wherein the muting pattern is at least partly based on a Synchronization Signal Block (SSB) periodicity from the NR network; and\nmeans for receiving SSB transmissions from the second base station in the NR network while the dynamic LTE PRS or the regularly scheduled LTE PRS transmitted by the first base station in the LTE network is muted.",
          "claim_type": "dependent",
          "dependency": "claim 15",
          "is_exemplary": true
        },
        {
          "claim_number": "00021",
          "claim_text": "21. The UE of claim 20, further comprising:\nmeans for muting the dynamic LTE PRS or the regularly scheduled LTE PRS for at least two symbols in a physical resource block (PRB) transmitted by the first base station in the LTE network to leave at least four consecutive symbols available for SSB transmissions in the PRB transmitted by the second base station in the NR network.",
          "claim_type": "dependent",
          "dependency": "claim 20",
          "is_exemplary": true
        },
        {
          "claim_number": "00022",
          "claim_text": "22. A non-transitory storage medium including program code stored thereon, the program code is operable to configure at least one processor in a user equipment (UE) for wireless communications with a New Radio (NR) network, the UE comprising:\nprogram code to receive, from an entity in the NR network, an NR signal comprising Long Term Evolution (LTE) positioning reference signal (PRS) rate matching information for dynamic LTE PRS transmitted by a first base station in an LTE network in one or more frequency bands shared by the NR network using dynamic spectrum sharing (DSS), wherein the LTE PRS rate matching information comprises an LTE PRS rate matching pattern;\nprogram code to receive NR data signals and control signals transmitted by a second base station in the NR network and the dynamic LTE PRS transmitted by the first base station in the LTE network on the one or more frequency bands; and\nprogram code to decode and process the NR data signals and control signals from the second base station in the NR network, wherein the program code to decode and process the NR data signals and control signals from the second base station in the NR network is configured to rate match around the dynamic LTE PRS in accordance with the LTE PRS rate matching information, wherein the program code to rate match around the dynamic LTE PRS in accordance with the LTE PRS rate matching information is configured to apply the LTE PRS rate matching pattern to the NR data signals and control signals to receive NR data.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00023",
          "claim_text": "23. The non-transitory storage medium of claim 22, wherein the NR data signals and control signals transmitted by the second base station in the NR network comprise at least one of physical downlink shared channel (PDSCH) transmissions, physical downlink common channel (PDCCH) transmissions, Synchronization Signal Block (SSB) transmissions, or a combination thereof.",
          "claim_type": "dependent",
          "dependency": "claim 22",
          "is_exemplary": true
        },
        {
          "claim_number": "00024",
          "claim_text": "24. The non-transitory storage medium of claim 22, wherein the LTE PRS rate matching information comprises LTE PRS configuration data to enable the UE to perform PRS positioning measurements.",
          "claim_type": "dependent",
          "dependency": "claim 22",
          "is_exemplary": true
        },
        {
          "claim_number": "00025",
          "claim_text": "25. The non-transitory storage medium of claim 22, wherein the UE comprises program code to:\ntransmit an indication to the entity in the NR network of a capability of rate matching around the dynamic LTE PRS in DSS, prior to receiving the LTE PRS rate matching information.",
          "claim_type": "dependent",
          "dependency": "claim 22",
          "is_exemplary": true
        },
        {
          "claim_number": "00026",
          "claim_text": "26. The non-transitory storage medium of claim 22, wherein the UE comprises program code to:\nreceive a muting pattern for the dynamic LTE PRS or a regularly scheduled LTE PRS in the LTE PRS rate matching information, wherein the muting pattern is at least partly based on a Synchronization Signal Block (SSB) periodicity from the NR network; and\nreceive SSB transmissions from the second base station in the NR network while the dynamic LTE PRS or the regularly scheduled LTE PRS transmitted by the first base station in the LTE network is muted.",
          "claim_type": "dependent",
          "dependency": "claim 22",
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.8,
      "publication_date": "2024-01-30",
      "patent_year": 2024
    },
    {
      "patent_id": "11832111",
      "title": "Dynamic spectrum sharing between 4G and 5G wireless networks",
      "abstract": "Aspects of the present disclosure provide various devices, methods, and systems for dynamic spectrum sharing of a spectrum between different radio access technologies and multiple frequency division duplexing modes. Dynamic spectrum sharing (DSS) is a technology that allows wireless network operators to share a spectrum between different radio access technologies (RATs). DSS allows an operator to dynamically allocate some existing 4G spectrum to 5G use to deliver 5G services using a shared spectrum.",
      "inventors": [
        "Wanshi Chen",
        "Huilin XU",
        "Peter Pui Lok Ang",
        "Jing Lei",
        "Runxin WANG"
      ],
      "assignees": [
        "QUALCOMM Incorporated"
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. A method for spectrum sharing in wireless communication at a first scheduling entity, the method comprising:\nexchanging scheduling information with a second scheduling entity, the scheduling information identifying a resource usage of a first radio access technology (RAT) in a resource pool for wireless communication, the second scheduling entity associated with the first RAT;\ndetermining a scheduling constraint imposed by the resource usage of the first RAT for sharing the resource pool for wireless communication using a second RAT, the first scheduling entity associated with the second RAT;\nallocating, based on the scheduling constraint, a resource of the resource pool for wireless communication using the second RAT, the resource comprising a plurality of time-frequency-space resources that are grouped in one or more mini-slots based on a numerology of the second RAT, each mini-slot spanning a time interval corresponding to one or more time domain symbols based on a numerology of the first RAT or the second RAT; and\ncommunicating with a user equipment (UE) using the resource allocated to the second RAT.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The method of claim 1, wherein the communicating with the UE comprises communicating with the UE using half-duplex frequency division duplex (HD-FDD) with the resource allocated to the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The method of claim 2,\nwherein identifying the resource usage comprises identifying a downlink resource usage dedicated to the first RAT as the scheduling constraint for using the second RAT, and the downlink resource usage comprises a resource of the resource pool used for at least one of:\na physical HARQ indicator channel (PHICH);\na physical control format indicator channel (PCFICH);\na physical downlink shared channel (PDSCH);\na channel state information reference signal (CSI-RS); or\na positioning reference signal (PRS).",
          "claim_type": "dependent",
          "dependency": "claim 2",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The method of claim 2,\nwherein identifying the resource usage comprises identifying an uplink resource usage dedicated to the first RAT as the scheduling constraint for using the second RAT, and the uplink resource usage comprises a resource of the resource pool used for at least one of:\na sounding reference signal (SRS);\na physical uplink shared channel (PUSCH); or\na physical uplink control channel (PUCCH).",
          "claim_type": "dependent",
          "dependency": "claim 2",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The method of claim 1, wherein the scheduling constraint comprises a predetermined frequency offset or slot offset from an LTE synchronization signal.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. The method of claim 1, wherein communicating with the UE comprises at least one of:\nrepeating a signal transmission of the second RAT using the one or more mini-slots; or\ntransmitting a signal of the second RAT using frequency hopping in the one or more mini-slots.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The method of claim 1, wherein communicating with the UE comprises:\ntransmitting a synchronization signal block (SSB) of the second RAT that is not punctured by a reference signal of the first RAT, a numerology of the first RAT being different from a numerology of the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The method of claim 1, wherein communicating with the UE comprises:\ntransmitting a synchronization signal block (SSB) of the second RAT that is punctured by or rate-matched around a cell-specific reference signal, a control channel, or a semi-persistently scheduled downlink data channel of the first RAT.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. The method of claim 1, wherein communicating with the UE comprises:\ntransmitting a synchronization signal block (SSB) and a control resource set (CORESET) of the second RAT using time-division multiplexing, frequency-division multiplexing, or space-division-multiplexing, depending on at least one of a bandwidth constraint, a power constraint, or capabilities of the UE.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. The method of claim 9, wherein allocating the resource comprises at least one of:\nallocating the resource to the SSB based on a predetermined frequency offset from a synchronization signal of the first RAT, wherein a numerology of the frequency offset is based on a numerology of the first RAT or a numerology of the second RAT; or\nallocating the resource to the SSB based on a predetermined slot offset from the synchronization signal of the first RAT, wherein a numerology of the slot offset is based on a numerology of the first RAT or a numerology of the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 9",
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. The method of claim 9, wherein transmitting the SSB comprises:\ntransmitting an SSB burst comprising a plurality of SSBs that are time-multiplexed, frequency-multiplexed, or space-multiplexed with resources of the resource pool that are dedicated to the first RAT.",
          "claim_type": "dependent",
          "dependency": "claim 9",
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. The method of claim 1, wherein allocating the resource comprises:\nallocating resources of the resource pool to a random access procedure (RACH) of the second RAT that is time-multiplexed or frequency-multiplexed with one or more RACH occasions of the first RAT.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. The method of claim 1, further comprising:\ndetermining a cell-specific slot format of the second RAT based on the scheduling constraint, wherein the cell-specific slot format comprises information for configuring at least one of a downlink mini-slot, an uplink mini-slot, a guard period mini-slot, and a special mini-slot; and\ntransmitting a radio resource control (RRC) message including the cell-specific slot format to a user equipment using the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. A first scheduling entity for wireless communication, comprising:\na communication interface configured for wireless communication using spectrum sharing between a first radio access technology (RAT) and a second RAT;\na memory; and\na processor coupled with the communication interface and the memory,\nthe processor and the memory being configured to:\nexchange scheduling information with a second scheduling entity, the scheduling information identifying a resource usage of the first RAT in a resource pool for wireless communication, the second scheduling entity associated with the first RAT;\ndetermine a scheduling constraint imposed by the resource usage of the first RAT for sharing the resource pool for wireless communication using the second RAT, the first scheduling entity associated with the second RAT;\nallocate, based on the scheduling constraint, a resource of the resource pool for wireless communication using the second RAT, the resource comprising a plurality of time-frequency-space resources that are grouped in one or more mini-slots based on a numerology of the second RAT, each mini-slot spanning a time interval corresponding to one or more time domain symbols based on a numerology of the first RAT or the second RAT; and\ncommunicate with a user equipment (UE) using the resource allocated to the second RAT.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00015",
          "claim_text": "15. The apparatus of claim 14, wherein the processor and the memory are configured to communicate with the UE using half-duplex frequency division duplex (HD-FDD) with the resource allocated to the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00016",
          "claim_text": "16. The apparatus of claim 15,\nwherein the resource usage comprises a downlink resource usage dedicated to the first RAT as the scheduling constraint for using the second RAT, and the downlink resource usage comprises a resource of the resource pool used for at least one of:\na physical HARQ indicator channel (PHICH);\na physical control format indicator channel (PCFICH);\na physical downlink shared channel (PDSCH);\na channel state information reference signal (CSI-RS); or\na positioning reference signal (PRS).",
          "claim_type": "dependent",
          "dependency": "claim 15",
          "is_exemplary": true
        },
        {
          "claim_number": "00017",
          "claim_text": "17. The apparatus of claim 15,\nwherein the resource usage comprises an uplink resource usage dedicated to the first RAT as the scheduling constraint for using the second RAT, and the uplink resource usage comprises a resource of the resource pool used for at least one of:\na sounding reference signal (SRS);\na physical uplink shared channel (PUSCH); or\na physical uplink control channel (PUCCH).",
          "claim_type": "dependent",
          "dependency": "claim 15",
          "is_exemplary": true
        },
        {
          "claim_number": "00018",
          "claim_text": "18. The apparatus of claim 14, wherein the scheduling constraint comprises a predetermined frequency offset or slot offset from an LTE synchronization signal.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00019",
          "claim_text": "19. The apparatus of claim 14, wherein, for communicating with the UE, the processor and the memory are further configured to at least one of:\nrepeat a signal transmission of the second RAT using the one or more mini-slots; or\ntransmit a signal of the second RAT using frequency hopping using the one or more mini-slots.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00020",
          "claim_text": "20. The apparatus of claim 14, wherein, for communicating with the UE, the processor and the memory are further configured to:\ntransmit a synchronization signal block (SSB) of the second RAT that is not punctured by a reference signal of the first RAT, a numerology of the first RAT being different from a numerology of the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00021",
          "claim_text": "21. The apparatus of claim 14, wherein, for communicating with the UE, the processor and the memory are further configured to:\ntransmit a synchronization signal block (SSB) of the second RAT that is punctured by or rate matched around a cell-specific reference signal, a control channel, or a semi-persistently scheduled downlink data channel of the first RAT.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00022",
          "claim_text": "22. The apparatus of claim 14, wherein, for communicating with the UE, the processor and the memory are further configured to:\ntransmit a synchronization signal block (SSB) and a control resource set (CORESET) of the second RAT using time-division multiplexing, frequency-division multiplexing, or space-division-multiplexing, depending on at least one of a bandwidth constraint, a power constraint, or capabilities of the UE.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00023",
          "claim_text": "23. The apparatus of claim 22, wherein, for allocating the resource, the processor and the memory are further configured to at least one of:\nallocate the resource to the SSB based on a predetermined frequency offset from a synchronization signal of the first RAT, wherein a numerology of the frequency offset is based on a numerology of the first RAT or a numerology of the second RAT; or\nallocate the resource to the SSB based on a predetermined slot offset from the synchronization signal of the first RAT, wherein a numerology of the slot offset is based on a numerology of the first RAT or a numerology of the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 22",
          "is_exemplary": true
        },
        {
          "claim_number": "00024",
          "claim_text": "24. The apparatus of claim 22, wherein, for transmitting the SSB, the processor and the memory are further configured to:\ntransmit an SSB burst comprising a plurality of SSBs that are time-multiplexed, frequency-multiplexed, or space-multiplexed with resources of the resource pool that are dedicated to the first RAT.",
          "claim_type": "dependent",
          "dependency": "claim 22",
          "is_exemplary": true
        },
        {
          "claim_number": "00025",
          "claim_text": "25. The apparatus of claim 14, wherein, for allocating the resource, the processor and the memory are further configured to:\nallocate resources of the resource pool to a random access procedure (RACH) of the second RAT that is time-multiplexed or frequency-multiplexed with one or more RACH occasions of the first RAT.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00026",
          "claim_text": "26. The apparatus of claim 14, wherein the processor and the memory are further configured to:\ndetermine a cell-specific slot format of the second RAT based on the scheduling constraint, wherein the cell-specific slot format comprises information for configuring at least one of a downlink mini-slot, an uplink mini-slot, a guard period mini-slot, and a special mini-slot; and\ntransmit a radio resource control (RRC) message including the cell-specific slot format to a user equipment using the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00027",
          "claim_text": "27. A first scheduling entity for wireless communication using spectrum sharing, comprising:\nmeans for exchanging scheduling information with a second scheduling entity, the scheduling information identifying a resource usage of a first radio access technology (RAT) in a resource pool for wireless communication, the second scheduling entity associated with the first RAT;\nmeans for determining a scheduling constraint imposed by the resource usage of the first RAT for sharing the resource pool for wireless communication using a second RAT, the first scheduling entity associated with the second RAT;\nmeans for allocating, based on the scheduling constraint, a resource of the resource pool for wireless communication using the second RAT, the resource comprising a plurality of time-frequency-space resources that are grouped in one or more mini-slots based on a numerology of the second RAT, each mini-slot spanning a time interval corresponding to one or more time domain symbols based on a numerology of the first RAT or the second RAT; and\nmeans for communicating with a user equipment (UE) using the resource allocated to the second RAT.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00028",
          "claim_text": "28. A non-transitory computer-readable medium storing computer-executable code at a first scheduling entity for wireless communication using dynamic spectrum sharing, comprising code for causing a processor to:\nexchange scheduling information with a second scheduling entity, the scheduling information identifying a resource usage of a first radio access technology (RAT) in a resource pool for wireless communication, the second scheduling entity associated with the first RAT;\ndetermine a scheduling constraint imposed by the resource usage of the first RAT for sharing the resource pool for wireless communication using a second RAT, the first scheduling entity associated with the second RAT;\nallocate, based on the scheduling constraint, a resource of the resource pool for wireless communication using the second RAT, the resource comprising a plurality of time-frequency-space resources that are grouped in one or more mini-slots based on a numerology of the second RAT, each mini-slot spanning a time interval corresponding to one or more time domain symbols based on a numerology of the first RAT or the second RAT; and\ncommunicate with a user equipment (UE) using the resource allocated to the second RAT.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.8,
      "publication_date": "2023-11-28",
      "patent_year": 2023
    },
    {
      "patent_id": "11044693",
      "title": "Efficient positioning enhancement for dynamic spectrum sharing",
      "abstract": "Techniques are provided for transmitting Positioning Reference Signals (PRSs) in cells supporting two different Radio Access Technologies (RATs), where the two RATs (e.g. 4G LTE and 5G NR) employ dynamic spectrum sharing. To avoid interference between the PRSs and between the two RATs, the PRSs may be time aligned to the same set of PRS positioning occasions, and may be assigned orthogonal characteristics such as different muting patterns, orthogonal code sequences, different frequency shifts or different frequency hopping. UEs supporting both RATs may be enabled to measure PRSs for both RATs. UEs supporting only one RAT (e.g. 4G LTE) may be enabled to measure PRSs for just this RAT. A location server such as an LMF, E-SMLC or SLP may provide assistance data to UEs, and request measurements from UEs, for PRSs in one or both RATs.",
      "inventors": [
        "Stephen William Edge",
        "Bapineedu Chowdary Gummadi",
        "Hem Agnihotri"
      ],
      "assignees": [
        "QUALCOMM Incorporated"
      ],
      "claims": [],
      "relevance_score": 0.8,
      "publication_date": "2021-06-22",
      "patent_year": 2021
    },
    {
      "patent_id": "10849180",
      "title": "Dynamic spectrum sharing in 4G and 5G",
      "abstract": "Techniques for dynamically allocating frequency resources in accordance with wireless access technologies are discussed herein. For example, a base station can determine whether user equipment (UE) requesting communications at the base station are configured to operate in accordance with 4th Generation (5G) radio access technologies and/or in accordance with 5th Generation (5G) radio access technologies. Based on the number of 5G UEs and 4G UEs, a first portion of a frequency resource can be allocated to 5G and a second portion of the frequency resource can be allocated to 4G. In some examples, a first allocation strategy for a first frequency resource (e.g., Band 71) can be used to generate a second allocation strategy for a partially overlapping second frequency resource (e.g., Band 41).",
      "inventors": [
        "Yasmin Karimli",
        "Gunjan Nimbavikar"
      ],
      "assignees": [
        "T-Mobile USA, Inc."
      ],
      "claims": [],
      "relevance_score": 0.8,
      "publication_date": "2020-11-24",
      "patent_year": 2020
    },
    {
      "patent_id": "11716124",
      "title": "Dynamic spectrum sharing with spatial division multiplexing",
      "abstract": "Methods, systems, and devices for wireless communications are described. A base station to communicate with a set of user equipments (UEs) in a spatial division multiplexing (SDM) configuration for dynamic spectrum sharing (DSS) communications. One or more first UEs of the set of UEs may communicate via a first radio access technology (RAT), and one or more second UEs may communicate via a second RAT in a multiple-user multiple-input multiple output (MU-MIMO) configuration. The base station may indicate the SDM configuration to one or more of the set of UEs. In some examples, the base station may transmit an indication to the set of UEs which may indicate a set of resources to be used for DSS communications. In some examples, the SDM configuration may specify one or more reference signal patterns for communicating in the set of resources.",
      "inventors": [
        "Tao Luo",
        "Wooseok Nam",
        "Kausik Ray Chaudhuri"
      ],
      "assignees": [
        "QUALCOMM Incorporated"
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. A method for wireless communications at a user equipment (UE), comprising:\nreceiving, from a network device, an indication of a set of resources to be used for dynamic spectrum sharing communications with the network device;\ndetermining, based at least in part on the indication, a spatial division multiplexing configuration comprising interference measurement resources for the set of resources, rate matching resources for the set of resources, or both;\nreceiving a notification that a first communication between the UE and the network device applies the spatial division multiplexing configuration; and\nperforming, based at least in part on the notification, the first communication on the set of resources via a first spatial layer associated with the first radio access technology in accordance with the spatial division multiplexing configuration, the first communication being multiplexed on the set of resources with a second communication between a second UE and the network device via a second radio access technology using a second spatial layer associated with the second radio access technology.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The method of claim 1, further comprising:\nreceiving, via explicit signaling, the notification that the first communication applies the spatial division multiplexing configuration.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The method of claim 2, wherein the notification indicates that the first communication with the UE via the first radio access technology is multiplexed with the second communication with the second UE via the second radio access technology in accordance with the spatial division multiplexing configuration.",
          "claim_type": "dependent",
          "dependency": "claim 2",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The method of claim 2, wherein the notification includes a location, a scrambling sequence, a transmission power, or any combination thereof, for one or more reference signals configured for the transmission in the set of resources.",
          "claim_type": "dependent",
          "dependency": "claim 2",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The method of claim 1, further comprising:\nreceiving, via implicit signaling, the notification that the first communication applies the spatial division multiplexing configuration.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. The method of claim 1, further comprising:\ndetermining one or more reference signal patterns associated with the set of resources, wherein the one or more reference signal patterns comprise the interference measurement resources, the rate matching resources, or both.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The method of claim 6, wherein the one or more reference signal patterns further comprise a set of antenna ports associated with one or more demodulation reference signals shared between the first communication via the first radio access technology and the second communication via the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 6",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The method of claim 6, wherein the indication comprises a configuration associated with the one or more reference signal patterns.",
          "claim_type": "dependent",
          "dependency": "claim 6",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. The method of claim 1, wherein the interference measurement resources are associated with the first communication via the first radio access technology and the second communication via the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. The method of claim 1, wherein the interference measurement resources include a New Radio (NR) interference measurement resource, or a resource for measuring interference from a Long Term Evolution (LTE) cell-specific reference signal, an LTE non-zero power channel state information reference signal, an LTE sounding reference signal, or any combination thereof.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. The method of claim 1, wherein the rate matching resources are associated with a Long Term Evolution (LTE) demodulation reference signal, an LTE cell-specific reference signal, a zero power channel state information reference signal (CSI-RS) associated with LTE CSI-RS resources, or any combination thereof.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. The method of claim 1, further comprising:\nidentifying, in the indication, a configuration associated with a rate matching pattern for one or more reference signals configured for transmission in the set of resources, wherein the rate matching pattern is based at least in part on a first numerology associated with the first radio access technology and a second numerology associated with the second radio access technology, and wherein performing the first communication with the network device is further in accordance with the rate matching pattern.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. A method for wireless communications at a network device, comprising:\ndetermining a spatial division multiplexing configuration for dynamic spectrum sharing communications with one or more first user equipments (UEs) communicating via a first radio access technology and with one or more second UEs communicating via a second radio access technology;\ntransmitting, to at least the one or more first UEs, an indication of a set of resources associated with a spatial division multiplexing configuration to be used for the dynamic spectrum sharing communications, wherein the spatial division multiplexing configuration comprises interference measurement resources for the set of resources, rate matching resources for the set of resources, or both;\ntransmitting, to at least the one or more first UEs, a notification that the first communication applies the spatial division multiplexing configuration; and\nperforming, based at least in part on the notification, the first communication on the set of resources via a first spatial layer associated with the first radio access technology in accordance with the spatial division multiplexing configuration and a second communication between the one or more second UEs and the network device via the second radio access technology on a second spatial layer associated with the second radio access technology, the first communication being multiplexed on the set of resources with the second communication.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. The method of claim 13, further comprising:\ntransmitting, via explicit signaling, the notification that the first communication applies the spatial division multiplexing configuration.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00015",
          "claim_text": "15. The method of claim 14, wherein the notification indicates that the first communication with the one or more first UEs via the first radio access technology is multiplexed with the second communication with the one or more second UEs via the second radio access technology in accordance with the spatial division multiplexing configuration.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00016",
          "claim_text": "16. The method of claim 14, wherein the notification includes a location, a scrambling sequence, a transmission power, or any combination thereof, for one or more reference signals configured for the transmission in the set of resources.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00017",
          "claim_text": "17. The method of claim 13, further comprising:\ntransmitting, via implicit signaling, the notification that the first communication applies the spatial division multiplexing configuration.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00018",
          "claim_text": "18. The method of claim 13, further comprising:\ndetermining one or more reference signal patterns associated with the set of resources, wherein the one or more reference signal patterns comprise the interference measurement resources, the rate matching resources, or both.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00019",
          "claim_text": "19. The method of claim 18, wherein the one or more reference signal patterns further comprise a set of antenna ports associated with one or more demodulation reference signals shared between the first communication via the first radio access technology and the second communication via the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 18",
          "is_exemplary": true
        },
        {
          "claim_number": "00020",
          "claim_text": "20. The method of claim 13, wherein the interference measurement resources are associated with the first communication via the first radio access technology and the second communication via the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00021",
          "claim_text": "21. The method of claim 13, wherein the interference measurement resources include a New Radio (NR) interference measurement resource, or a resource for measuring interference from a Long Term Evolution (LTE) cell-specific reference signal, an LTE non-zero power channel state information reference signal, an LTE sounding reference signal, or any combination thereof.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00022",
          "claim_text": "22. The method of claim 13, wherein the rate matching resources are associated with a Long Term Evolution (LTE) demodulation reference signal, an LTE cell-specific reference signal, a zero power channel state information reference signal (CSI-RS) associated with LTE CSI-RS resources, or any combination thereof.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00023",
          "claim_text": "23. The method of claim 13, further comprising:\ndetermining a first numerology associated with the first radio access technology and a second numerology associated with the second radio access technology; and\ndetermining a rate matching pattern for one or more reference signals configured for transmission in the set of resources based at least in part on the first numerology and the second numerology, wherein the indication comprises a configuration associated with the rate matching pattern.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00024",
          "claim_text": "24. The method of claim 23, wherein the rate matching pattern comprises a New Radio (NR) demodulation reference signal rate matching pattern associated with interference between the first communication via the first radio access technology and the second communication via the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 23",
          "is_exemplary": true
        },
        {
          "claim_number": "00025",
          "claim_text": "25. The method of claim 13, further comprising:\npuncturing one or more resource elements of the set of resources based at least in part on interference between the first communication via the first radio access technology and the second communication via the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00026",
          "claim_text": "26. An apparatus for wireless communications, comprising:\na processor;\nmemory coupled with the processor; and\ninstructions stored in the memory and executable by the processor to cause the apparatus to:\nreceive, from a network device, an indication of a set of resources to be used for dynamic spectrum sharing communications with the network device;\ndetermine, based at least in part on the indication, a spatial division multiplexing configuration comprising interference measurement resources for the set of resources, rate matching resources for the set of resources, or both;\nreceive a notification that a first communication between the UE and the network device applies the spatial division multiplexing configuration; and\nperform, based at least in part on the notification, a first communication on the set of resources via a first spatial layer associated with the first radio access technology in accordance with the spatial division multiplexing configuration, the first communication being multiplexed on the set of resources with a second communication between a second apparatus and the network device via a second radio access technology using a second spatial layer associated with the second radio access technology.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00027",
          "claim_text": "27. An apparatus for wireless communications, comprising:\na processor;\nmemory coupled with the processor; and\ninstructions stored in the memory and executable by the processor to cause the apparatus to:\ndetermine a spatial division multiplexing configuration for dynamic spectrum sharing communications with one or more first user equipments (UEs) communicating via a first radio access technology and with one or more second UEs communicating via a second radio access technology;\ntransmit, to at least the one or more first UEs, an indication of a set of resources associated with a spatial division multiplexing configuration to be used for the dynamic spectrum sharing communications, wherein the spatial division multiplexing configuration comprises interference measurement resources for the set of resources, rate matching resources for the set of resources, or both;\ntransmit, to at least the one or more first UEs, a notification that a first communication applies the spatial division multiplexing configuration; and\nperform, based at least in part on the notification, the first communication on the set of resources via a first spatial layer associated with the first radio access technology in accordance with the spatial division multiplexing configuration and a second communication between the one or more second UEs and the apparatus via the second radio access technology on a second spatial layer associated with the second radio access technology, the first communication being multiplexed on the set of resources with the second communication.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.8,
      "publication_date": "2023-08-01",
      "patent_year": 2023
    },
    {
      "patent_id": "11943204",
      "title": "Method and systems for dynamic spectrum sharing with a spectrum management firewall",
      "abstract": "Methods and systems for dynamically sharing spectrum between a commercial network and a protected system network. A spectrum management firewall (SMF) computing device may receive information from the commercial network, receive characteristic information identifying one or more characteristics of a resource or entity in the protected system network, determine a class of system (COS) and an area of operation (AOO) for the resource or entity based on the characteristic information received from the protected system network, and determine potential interference based on the information received from the commercial network and the characteristic information received from the protected system network. The SMF may determine which frequencies may be suppressed on which cells in the commercial network based on the determined potential interference, generate a suppression message that identifies the determined frequencies per cell, and send the generated suppression message to a component in the commercial network.",
      "inventors": [
        "John Arpee"
      ],
      "assignees": [
        "RIVADA NETWORKS, LLC"
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. A method of dynamically sharing spectrum between a commercial network and a protected system network, comprising:\nreceiving, by a processor a spectrum management firewall (SMF) computing device, information from the commercial network;\nreceiving, by the processor, characteristic information identifying one or more characteristics of a resource or entity in the protected system network;\ndetermining, by the processor, a class of system (COS) and an area of operation (AOO) for the resource or entity based on the characteristic information received from the protected system network;\ndetermining, by the processor, potential interference based on the information received from the commercial network and the characteristic information received from the protected system network;\ndetermining, by the processor, which frequencies may be suppressed on which cells in the commercial network based on the determined potential interference;\ngenerating, by the processor, a suppression message that identifies the determined frequencies per cell; and\nsending, by the processor, the generated suppression message to a component in the commercial network to cause that component to suppress the identified frequencies in the identified cells.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The method of claim 1, wherein generating the suppression message that identifies the determined frequencies per cell that mask the activities, operations, communications, locations, features, properties, or characteristics of the resource or entity in the protected system network.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The method of claim 2, wherein generating the obfuscated message comprises adding additional frequencies that mask the activities, operations, communications, locations, features, properties, or characteristics of the resource or entity in the protected system network to the suppression message.",
          "claim_type": "dependent",
          "dependency": "claim 2",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The method of claim 1, further comprising:\nusing a generative adversarial network (GAN) that includes a deep neural network and a generator to produce fake data;\ninserting the generated fake data into the suppression message prior to sending the generated suppression message to the component in the commercial network; or\nusing the generated fake data to generate additional suppression messages that are intentionally misleading and sending the additional suppression messages to the component in the commercial network.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The method of claim 1, further comprising using a generative adversarial network (GAN) that includes a deep neural network and a generator to create credible fake activities of the resource or entities in the protected systems network including movement patterns, emissions spectrums, frequency blanking patterns and realistic activity schedules.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. The method of claim 1, wherein:\nreceiving characteristic information from the protected system network comprises:\nreceiving detected activity information, signal level information and frequency information collected by sensors within a vicinity of the resource or entity in the protected systems network in response to detecting that the resource or entity recently became active; and\ndetermining the COS and the PAOO based on the characteristic information received from the protected system network comprises:\ndetermining the COS and an approximate area associated with the recently active resource or entity based on the received activity information, signal level information, and frequency information.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The method of claim 1, wherein receiving characteristic information from the protected system network comprises:\nreceiving a spectrum reservation message from the protected system network indicating that the resource or entity is anticipated to become or is becoming active in an area; and\nwherein determining the COS and the AOO based on the characteristic information received from the protected system network comprises:\ndetermining the COS and an approximate area of the resource or entity that is anticipated to become or is becoming active based on the received spectrum reservation message.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The method of claim 1, wherein sending the generated message to the component in the commercial network to cause that component to suppress the identified frequencies in the identified cells comprises sending the generated message to the component in the commercial network to cause that component to:\nstop all transmissions on the identified frequencies;\nreduce power on the identified frequencies;\nreorient antennas to direct power away from the resource or entity in the protected systems network; or\ndown-tilt or direct the antennas into focused areas that only allow the power to be transmitted in the immediate vicinity of the identified cells.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. The method of claim 1, further comprising:\nreceiving, by the processor, a notification message from the protected system network indicating that a detected activity identified in the received characteristic information has ceased; and\ncausing, by the processor, the component in the commercial network to cease suppressing the identified frequencies in the identified cells and restore power levels in response to the processor receiving the notification message from the protected system network indicating that the detected activity identified in the received characteristic information has ceased.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. The method of claim 9, wherein causing the component in the commercial network to cease suppressing the identified frequencies in the identified cells and restore power levels comprises sending a communication message to the component that causes the component to reorient and uptilt antennas back to configurations that are optimized for full utilization of the identified frequencies on the commercial network.",
          "claim_type": "dependent",
          "dependency": "claim 9",
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. The method of claim 1, wherein determining potential interference based on the information received from the commercial network and the characteristic information received from the protected system network comprises:\ndetermining the cell sites and frequencies that would result in interference between the resource or entity within the protected systems network and specific cells and attached mobiles in the commercial network.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. A server computing device implementing a spectrum management firewall (SMF), comprising:\na processor configured with processor-executable instructions to perform operations comprising:\nreceiving information from a commercial network;\n\nreceiving characteristic information identifying one or more characteristics of a resource or entity in a protected system network;\ndetermining a class of system (COS) and a planned area of operation (AOO) for the resource or entity based on the characteristic information received from the protected system network;\ndetermining potential interference based on the information received from the commercial network and the characteristic information received from the protected system network;\ndetermining which frequencies may be suppressed on which cells in the commercial network based on the determined potential interference;\ngenerating a suppression message that identifies the determined frequencies per cell; and\nsending the generated suppression message to a component in the commercial network to cause that component to suppress the identified frequencies in the identified cells.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. The server computing device of claim 12, wherein the processor is configured with processor executable instructions to perform operations such that generating the suppression message that identifies the determined frequencies per cell comprises generating an obfuscation message that mask the activities, operations, communications, locations, features, properties, or characteristics of the resource or entity in the protected system network.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. The server computing device of claim 13, wherein the processor is configured with processor executable instructions to perform operations such that generating the obfuscation message comprises adding additional frequencies that mask the activities, operations, communications, locations, features, properties, or characteristics of the resource or entity in the protected system network to the suppression message.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00015",
          "claim_text": "15. The server computing device of claim 12, wherein the processor is configured with processor executable instructions to perform operations further comprising:\nusing a generative adversarial network (GAN) that includes a deep neural network and a generator to produce fake data;\ninserting the generated fake data into the suppression message prior to sending the generated suppression message to the component in the commercial network; or\nusing the generated fake data to generate additional suppression messages that are intentionally misleading and sending the additional suppression messages to the component in the commercial network.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00016",
          "claim_text": "16. The server computing device of claim 12, wherein the processor is configured with processor executable instructions to perform operations further comprising using a generative adversarial network (GAN) that includes a deep neural network and a generator to detect and differentiate between real and fake activities of the resource or entities in the protected systems network.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00017",
          "claim_text": "17. The server computing device of claim 12, wherein the processor is configured with processor executable instructions to perform operations such that:\nreceiving characteristic information from the protected system network comprises:\nreceiving detected activity information, signal level information and frequency information collected by sensors within a vicinity of the resource or entity in the protected systems network in response to detecting that the resource or entity recently became active; and\ndetermining the COS and the PAOO based on the characteristic information received from the protected system network comprises:\ndetermining the COS and an approximate area associated with the recently active resource or entity based on the received activity information, signal level information, and frequency information.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00018",
          "claim_text": "18. The server computing device of claim 12, wherein the processor is configured with processor executable instructions to perform operations such that receiving characteristic information from the protected system network comprises:\nreceiving a spectrum reservation message from the protected system network indicating that the resource or entity is anticipated to become active in an area; and\nwherein the processor is configured with processor executable instructions to perform operations such that determining the COS and the AOO based on the characteristic information received from the protected system network comprises:\ndetermining the COS and an approximate area of the resource or entity that is anticipated to become active based on the received spectrum reservation message.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00019",
          "claim_text": "19. The server computing device of claim 12, wherein the processor is configured with processor executable instructions to perform operations such that sending the generated message to the component in the commercial network to cause that component to suppress the identified frequencies in the identified cells comprises sending the generated message to the component in the commercial network to cause that component to:\nstop all transmissions on the identified frequencies;\nreduce power on the identified frequencies;\nreorient antennas to direct power away from the resource or entity in the protected systems network; or\ndown-tilt or direct the antennas into focused areas that only allow the power to be transmitted in the immediate vicinity of the identified cells.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00020",
          "claim_text": "20. The server computing device of claim 12, wherein the processor is configured with processor executable instructions to perform operations further comprising:\nreceiving a notification message from the protected system network indicating that a detected activity identified in the received characteristic information has ceased; and\ncausing the component in the commercial network to cease suppressing the identified frequencies in the identified cells and restore power levels in response to the processor receiving the notification message from the protected system network indicating that the detected activity identified in the received characteristic information has ceased.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00021",
          "claim_text": "21. The server computing device of claim 20, wherein the processor is configured with processor executable instructions to perform operations such that causing the component in the commercial network to cease suppressing the identified frequencies in the identified cells and restore power levels comprises sending a communication message to the component that causes the component to reorient and uptilt antennas back to configurations that are optimized for full utilization of the identified frequencies on the commercial network.",
          "claim_type": "dependent",
          "dependency": "claim 20",
          "is_exemplary": true
        },
        {
          "claim_number": "00022",
          "claim_text": "22. The server computing device of claim 12, wherein the processor is configured with processor executable instructions to perform operations such that determining potential interference based on the information received from the commercial network and the characteristic information received from the protected system network comprises:\ndetermining the cell sites and frequencies that would result in interference between the resource or entity within the protected systems network and specific cells and attached mobiles in the commercial network.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00023",
          "claim_text": "23. A non-transitory computer readable storage medium having stored thereon processor-executable software instructions configured to cause a processor of a server computing device perform operations for dynamically sharing spectrum between a commercial network and a protected system network, the operations comprising:\nreceiving information from the commercial network;\nreceiving characteristic information identifying one or more characteristics of a resource or entity in the protected system network;\ndetermining a class of system (COS) and a area of operation (AOO) for the resource or entity based on the characteristic information received from the protected system network;\ndetermining potential interference based on the information received from the commercial network and the characteristic information received from the protected system network;\ndetermining which frequencies may be suppressed on which cells in the commercial network based on the determined potential interference;\ngenerating a suppression message that identifies the determined frequencies per cell; and\nsending the generated suppression message to a component in the commercial network to cause that component to suppress the identified frequencies in the identified cells.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00024",
          "claim_text": "24. The non-transitory computer readable storage medium of claim 23, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations such that generating the suppression message that identifies the determined frequencies per cell comprises generating an obfuscation message that mask the activities, operations, communications, locations, features, properties, or characteristics of the resource or entity in the protected system network.",
          "claim_type": "dependent",
          "dependency": "claim 23",
          "is_exemplary": true
        },
        {
          "claim_number": "00025",
          "claim_text": "25. The non-transitory computer readable storage medium of claim 24, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations such that generating the obfuscation message comprises adding additional frequencies that mask the activities, operations, communications, locations, features, properties, or characteristics of the resource or entity in the protected system network to the suppression message.",
          "claim_type": "dependent",
          "dependency": "claim 24",
          "is_exemplary": true
        },
        {
          "claim_number": "00026",
          "claim_text": "26. The non-transitory computer readable storage medium of claim 23, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations further comprising:\nusing a generative adversarial network (GAN) that includes a deep neural network and a generator to produce fake data;\ninserting the generated fake data into the suppression message prior to sending the generated suppression message to the component in the commercial network; or\nusing the generated fake data to generate additional suppression messages that are intentionally misleading and sending the additional suppression messages to the component in the commercial network.",
          "claim_type": "dependent",
          "dependency": "claim 23",
          "is_exemplary": true
        },
        {
          "claim_number": "00027",
          "claim_text": "27. The non-transitory computer readable storage medium of claim 23, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations further comprising using a generative adversarial network (GAN) that includes a deep neural network and a generator to detect and differentiate between real and fake activities of the resource or entities in the protected systems network.",
          "claim_type": "dependent",
          "dependency": "claim 23",
          "is_exemplary": true
        },
        {
          "claim_number": "00028",
          "claim_text": "28. The non-transitory computer readable storage medium of claim 23, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations such that:\nreceiving characteristic information from the protected system network comprises:\nreceiving detected activity information, signal level information and frequency information collected by sensors within a vicinity of the resource or entity in the protected systems network in response to detecting that the resource or entity recently became active; and\ndetermining the COS and the AOO based on the characteristic information received from the protected system network comprises:\ndetermining the COS and an approximate area associated with the recently active resource or entity based on the received activity information, signal level information, and frequency information.",
          "claim_type": "dependent",
          "dependency": "claim 23",
          "is_exemplary": true
        },
        {
          "claim_number": "00029",
          "claim_text": "29. The non-transitory computer readable storage medium of claim 23, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations such that receiving characteristic information from the protected system network comprises:\nreceiving a spectrum reservation message from the protected system network indicating that the resource or entity is anticipated to become active in an area; and\nwherein the stored processor-executable software instructions are configured to cause a processor to perform operations such that determining the COS and the AOO based on the characteristic information received from the protected system network comprises:\ndetermining the COS and an approximate area of the resource or entity that is anticipated to become active based on the received spectrum reservation message.",
          "claim_type": "dependent",
          "dependency": "claim 23",
          "is_exemplary": true
        },
        {
          "claim_number": "00030",
          "claim_text": "30. The non-transitory computer readable storage medium of claim 23, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations such that sending the generated message to the component in the commercial network to cause that component to suppress the identified frequencies in the identified cells comprises sending the generated message to the component in the commercial network to cause that component to:\nstop all transmissions on the identified frequencies;\nreduce power on the identified frequencies;\nreorient antennas to direct power away from the resource or entity in the protected systems network; or\ndown-tilt or direct the antennas into focused areas that only allow the power to be transmitted in the immediate vicinity of the identified cells.",
          "claim_type": "dependent",
          "dependency": "claim 23",
          "is_exemplary": true
        },
        {
          "claim_number": "00031",
          "claim_text": "31. The non-transitory computer readable storage medium of claim 23, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations further comprising:\nreceiving a notification message from the protected system network indicating that a detected activity identified in the received characteristic information has ceased; and\ncausing the component in the commercial network to cease suppressing the identified frequencies in the identified cells and restore power levels in response to the processor receiving the notification message from the protected system network indicating that the detected activity identified in the received characteristic information has ceased.",
          "claim_type": "dependent",
          "dependency": "claim 23",
          "is_exemplary": true
        },
        {
          "claim_number": "00032",
          "claim_text": "32. The non-transitory computer readable storage medium of claim 31, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations such that causing the component in the commercial network to cease suppressing the identified frequencies in the identified cells and restore power levels comprises sending a communication message to the component that causes the component to reorient and uptilt antennas back to configurations that are optimized for full utilization of the identified frequencies on the commercial network.",
          "claim_type": "dependent",
          "dependency": "claim 31",
          "is_exemplary": true
        },
        {
          "claim_number": "00033",
          "claim_text": "33. The non-transitory computer readable storage medium of claim 23, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations such that determining potential interference based on the information received from the commercial network and the characteristic information received from the protected system network comprises:\ndetermining the cell sites and frequencies that would result in interference between the resource or entity within the protected systems network and specific cells and attached mobiles in the commercial network.",
          "claim_type": "dependent",
          "dependency": "claim 23",
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.8,
      "publication_date": "2024-03-26",
      "patent_year": 2024
    },
    {
      "patent_id": "11638169",
      "title": "First radio access technology (RAT) channel state feedback (CSF) to increase accuracy of interference estimates from second RAT neighbor cells with dynamic spectrum sharing (DSS)",
      "abstract": "A user equipment (UE) receives, from a base station, a message including at least one reporting configuration and resource configuration for a number of channel state information-interference measurement (CSI-IM) resource patterns associated with a first radio access technology (RAT). Each of the configured CSI-IM resource patterns corresponds to a time and frequency location in a resource block of a neighbor cell associated with a second RAT. The UE transmits one or more CSI reports based on the reporting configuration(s) and the resource configuration(s).",
      "inventors": [
        "Alexei Yurievitch Gorokhov",
        "Hobin Kim",
        "Hari Sankar",
        "Faris RASSAM"
      ],
      "assignees": [
        "QUALCOMM Incorporated"
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. A method for wireless communication performed by a user equipment (UE), comprising:\nreceiving, from a base station, a message comprising at least one reporting configuration and at least one resource configuration for a plurality of channel state information-interference measurement (CSI-IM) resource patterns associated with a first radio access technology (RAT), each CSI-IM resource pattern of the plurality of CSI-IM resource patterns corresponding to a time and frequency location in a resource block of a neighbor cell associated with a second RAT; and\ntransmitting at least one CSI report based on the at least one reporting configuration and the at least one resource configuration.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The method of claim 1, in which:\nthe at least one reporting configuration configures reporting for a plurality of CSI reports, each CSI report of the plurality of CSI reports corresponding to a CSI-IM resource pattern of the plurality of CSI-IM resource patterns;\nan interference measurement of each CSI report comprises a total interference power of a set of resource elements (REs) of the resource blocks aligned with a time and frequency location of the CSI-IM resource pattern corresponding to the CSI report; and\nthe set of REs comprises at least one of a cell-specific reference signal (CRS) RE, a first physical downlink shared channel (PDSCH) RE in a symbol including CRS REs, or a second PDSCH RE in a symbol without CRS REs.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The method of claim 2, in which:\nthe at least one reporting configuration indicates a periodic reporting periodicity;\nthe transmitting the at least one CSI report comprises transmitting each CSI report of the plurality of CSI reports according to the periodic reporting periodicity; and\nthe method further comprises measuring the interference measurement for each CSI-IM resource pattern of the plurality of CSI-IM resource patterns.",
          "claim_type": "dependent",
          "dependency": "claim 2",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The method of claim 2, in which:\nthe at least one reporting configuration indicates a semi-persistent reporting periodicity;\nthe transmitting the at least one CSI report comprises transmitting each CSI report of a set of CSI reports from the plurality of CSI reports according to the semi-persistent reporting periodicity; and\nthe method further comprises:\nreceiving a signal for activating the set of CSI reports and a set of CSI-IM resource patterns corresponding to the set of CSI reports; and\nmeasuring the interference power for each CSI-IM resource pattern of the set of CSI-IM resource patterns.",
          "claim_type": "dependent",
          "dependency": "claim 2",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The method of claim 4, in which CSI resources are semi-persistent resources or periodic resources.",
          "claim_type": "dependent",
          "dependency": "claim 4",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. The method of claim 2, in which:\nthe at least one reporting configuration indicates an aperiodic reporting periodicity;\ntransmitting the at least one CSI report comprises transmitting each CSI report of a set of CSI reports from the plurality of CSI reports in response to a trigger; and\nthe method further comprises:\nreceiving the trigger for triggering the set of CSI reports and a set of CSI-IM resource patterns corresponding to the set of CSI reports; and\nmeasuring the interference power for each CSI-IM resource pattern of the set of CSI-IM resource patterns.",
          "claim_type": "dependent",
          "dependency": "claim 2",
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The method of claim 6, in which CSI resources are periodic resources, semi-persistent resources or aperiodic resources.",
          "claim_type": "dependent",
          "dependency": "claim 6",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The method of claim 1, in which a first frequency shift parameter (vShift) of cell-specific reference signal (CRS) resource elements (REs) of a serving cell of the second RAT is different from a second vShift of CRS REs of the neighbor cell.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. A method for wireless communication performed by a base station associated with a first radio access technology (RAT), comprising:\nconfiguring at least one reporting configuration and at least one resource configuration for a plurality of channel state information-interference measurement (CSI-IM) resource patterns associated with the first RAT, each CSI-IM resource pattern of the plurality of CSI-IM resource patterns corresponding to a time and frequency location in a resource block of a neighbor cell associated with a second RAT;\ntransmitting, to a user equipment (UE), a message comprising the at least one reporting configuration and the at least one resource configuration; and\nreceiving, from the UE, at least one CSI report based on the transmitted message.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. The method of claim 9, in which:\nthe at least one reporting configuration configures reporting for a plurality of CSI reports, each CSI report of the plurality of CSI reports corresponding to a CSI-IM resource pattern of the plurality of CSI-IM resource patterns;\neach CSI report comprises an interference measurement based on a total interference power of a set of resource elements (REs) of the resource blocks aligned with a time and frequency location of a CSI-IM resource pattern corresponding to the CSI report;\nthe set of REs comprises at least one of a cell-specific reference signal (CRS) RE, a first physical downlink shared channel (PDSCH) RE in a symbol including CRS REs, or a second PDSCH RE in a symbol without CRS REs; and\nthe method further comprises receiving, from the UE, a signal strength measurement of the neighbor cell.",
          "claim_type": "dependent",
          "dependency": "claim 9",
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. The method of claim 10, in which:\nthe at least one reporting configuration indicates a periodic reporting periodicity;\nthe receiving the at least one CSI report comprises receiving each CSI report of the plurality of CSI reports according to the periodic reporting periodicity; and\nthe method further comprises:\nselecting one or more CSI reports from the plurality of CSI reports based on the signal strength measurement of the neighbor cell; and\nscheduling the UE based on the interference measurement of the one or more CSI reports.",
          "claim_type": "dependent",
          "dependency": "claim 10",
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. The method of claim 10, in which:\nthe at least one reporting configuration indicates a semi-persistent reporting periodicity;\nthe receiving the at least one CSI report comprises receiving each CSI report of a set of CSI reports from the plurality of CSI reports according to the semi-persistent reporting periodicity; and\nthe method further comprises transmitting a signal for activating the set of CSI reports and a set of CSI-IM resource patterns corresponding to the set of CSI reports based on the signal strength measurement of the neighbor cell.",
          "claim_type": "dependent",
          "dependency": "claim 10",
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. The method of claim 12, in which CSI resources are semi-persistent resources or periodic resources.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. The method of claim 10, in which:\nthe at least one reporting configuration indicates an aperiodic reporting periodicity;\nthe receiving the at least one CSI report comprises receiving each CSI report of a set of CSI reports from the plurality of CSI reports in response to a trigger; and\nthe method further comprises transmitting the trigger to trigger the set of CSI reports and a set of CSI-IM resource patterns corresponding to the set of CSI reports based on the signal strength measurement of the neighbor cell.",
          "claim_type": "dependent",
          "dependency": "claim 10",
          "is_exemplary": true
        },
        {
          "claim_number": "00015",
          "claim_text": "15. The method of claim 14, in which CSI resources are periodic resources, semi-persistent resources or aperiodic resources.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00016",
          "claim_text": "16. The method of claim 9, in which a first frequency shift parameter (vShift) of cell-specific reference signal (CRS) resource elements (REs) of a serving cell of the second RAT is different from a second vShift of CRS REs of the neighbor cell.",
          "claim_type": "dependent",
          "dependency": "claim 9",
          "is_exemplary": true
        },
        {
          "claim_number": "00017",
          "claim_text": "17. An apparatus for wireless communications at a user equipment (UE), comprising:\na processor,\nmemory coupled with the processor; and\ninstructions stored in the memory and operable, when executed by the processor, to cause the apparatus:\nto receive, from a base station, a message comprising at least one reporting configuration and at least one resource configuration for a plurality of channel state information-interference measurement (CSI-IM) resource patterns associated with a first radio access technology (RAT), each CSI-IM resource pattern of the plurality of CSI-IM resource patterns corresponding to a time and frequency location in a resource block of a neighbor cell associated with a second RAT; and\nto transmit at least one CSI report based on the at least one reporting configuration and the at least one resource configuration.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00018",
          "claim_text": "18. The apparatus of claim 17, in which:\nthe at least one reporting configuration configures reporting for a plurality of CSI reports, each CSI report of the plurality of CSI reports corresponding to a CSI-IM resource pattern of the plurality of CSI-IM resource patterns;\nan interference measurement of each CSI report comprises a total interference power of a set of resource elements (REs) of the resource blocks aligned with a time and frequency location of a CSI-IM resource pattern corresponding to the CSI report; and\nthe set of REs comprises at least one of a cell-specific reference signal (CRS) RE, a first physical downlink shared channel (PDSCH) RE in a symbol including CRS REs, or a second PDSCH RE in a symbol without CRS REs.",
          "claim_type": "dependent",
          "dependency": "claim 17",
          "is_exemplary": true
        },
        {
          "claim_number": "00019",
          "claim_text": "19. The apparatus of claim 18, in which:\nthe at least one reporting configuration indicates a periodic reporting periodicity; and\nthe processor causes the apparatus:\nto transmit the at least one CSI report by transmitting each CSI report of the plurality of CSI reports according to the periodic reporting periodicity; and\nto measure the interference measurement for each CSI-IM resource pattern of the plurality of CSI-IM resource patterns.",
          "claim_type": "dependent",
          "dependency": "claim 18",
          "is_exemplary": true
        },
        {
          "claim_number": "00020",
          "claim_text": "20. The apparatus of claim 18, in which:\nthe at least one reporting configuration indicates a semi-persistent reporting periodicity; and\nthe processor causes the apparatus:\nto transmit the at least one CSI report by transmitting each CSI report of a set of CSI reports from the plurality of CSI reports according to the semi-persistent reporting periodicity;\nto receive a signal for activating the set of CSI reports and a set of CSI-IM resource patterns corresponding to the set of CSI reports; and\nto measure the interference power for each CSI-IM resource pattern of the set of CSI-IM resource patterns.",
          "claim_type": "dependent",
          "dependency": "claim 18",
          "is_exemplary": true
        },
        {
          "claim_number": "00021",
          "claim_text": "21. The apparatus of claim 18, in which:\nthe at least one reporting configuration indicates an aperiodic reporting periodicity; and\nthe processor causes the apparatus:\nto transmit the at least one CSI report by transmitting each CSI report of a set of CSI reports from the plurality of CSI reports in response to a trigger; and\nto receive the trigger for triggering the set of CSI reports and a set of CSI-IM resource patterns corresponding to the set of CSI reports; and\nto measure the interference power for each CSI-IM resource pattern of the set of CSI-IM resource patterns.",
          "claim_type": "dependent",
          "dependency": "claim 18",
          "is_exemplary": true
        },
        {
          "claim_number": "00022",
          "claim_text": "22. The apparatus of claim 17, in which a first frequency shift parameter (vShift) of cell-specific reference signal (CRS) resource elements (REs) of a serving cell of the second RAT is different from a second vShift of CRS REs of the neighbor cell.",
          "claim_type": "dependent",
          "dependency": "claim 17",
          "is_exemplary": true
        },
        {
          "claim_number": "00023",
          "claim_text": "23. An apparatus for wireless communications at a base station associated with a first radio access technology (RAT), comprising:\na processor,\nmemory coupled with the processor; and\ninstructions stored in the memory and operable, when executed by the processor, to cause the apparatus:\nto configure at least one reporting configuration and at least one resource configuration for a plurality of channel state information-interference measurement (CSI-IM) resource patterns associated with the first RAT, each CSI-IM resource pattern of the plurality of CSI-IM resource patterns corresponding to a time and frequency location in a resource block of a neighbor cell associated with a second RAT;\nto transmit, to a user equipment (UE), a message comprising the at least one reporting configuration and the at least one resource configuration; and\nto receive, from the UE, at least one CSI report based on the transmitted message.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00024",
          "claim_text": "24. The apparatus of claim 23, in which:\nthe at least one reporting configuration configures reporting for a plurality of CSI reports, each CSI report of the plurality of CSI reports corresponding to a CSI-IM resource pattern of the plurality of CSI-IM resource patterns;\neach CSI report comprises an interference measurement based on a total interference power of a set of resource elements (REs) of the resource blocks aligned with a time and frequency location of a CSI-IM resource pattern corresponding to the CSI report;\nthe set of REs comprise at least one of a cell-specific reference signal (CRS) RE, a first physical downlink shared channel (PDSCH) RE in a symbol including CRS REs, or a second PDSCH RE in a symbol without CRS REs; and\nthe processor causes the apparatus to receive, from the UE, a signal strength measurement of the neighbor cell.",
          "claim_type": "dependent",
          "dependency": "claim 23",
          "is_exemplary": true
        },
        {
          "claim_number": "00025",
          "claim_text": "25. The apparatus of claim 24, in which CSI resources are semi-persistent resources or periodic resources.",
          "claim_type": "dependent",
          "dependency": "claim 24",
          "is_exemplary": true
        },
        {
          "claim_number": "00026",
          "claim_text": "26. The apparatus of claim 24, in which:\nthe at least one reporting configuration indicates a periodic reporting periodicity; and\nthe processor causes the apparatus:\nto receive the at least one CSI report by receiving each CSI report of the plurality of CSI reports according to the periodic reporting periodicity;\nto select one or more CSI reports from the plurality of CSI reports based on the signal strength measurement of the neighbor cell; and\nto schedule the UE based on the interference measurement of the one or more CSI reports.",
          "claim_type": "dependent",
          "dependency": "claim 24",
          "is_exemplary": true
        },
        {
          "claim_number": "00027",
          "claim_text": "27. The apparatus of claim 24, in which:\nthe at least one reporting configuration indicates a semi-persistent reporting periodicity; and\nthe processor causes the apparatus:\nto receive the at least one CSI report by receiving each CSI report of a set of CSI reports from the plurality of CSI reports according to the semi-persistent reporting periodicity; and\nto transmit a signal for activating the set of CSI reports and a set of CSI-IM resource patterns corresponding to the set of CSI reports based on the signal strength measurement of the neighbor cell.",
          "claim_type": "dependent",
          "dependency": "claim 24",
          "is_exemplary": true
        },
        {
          "claim_number": "00028",
          "claim_text": "28. The apparatus of claim 26, in which CSI resources are periodic resources, semi-persistent resources or aperiodic resources.",
          "claim_type": "dependent",
          "dependency": "claim 26",
          "is_exemplary": true
        },
        {
          "claim_number": "00029",
          "claim_text": "29. The apparatus of claim 24, in which:\nthe at least one reporting configuration indicates an aperiodic reporting periodicity; and\nthe processor causes the apparatus:\nto receive the at least one CSI report by receiving each CSI report of a set of CSI reports from the plurality of CSI reports in response to a trigger; and\nto transmit the trigger for triggering the set of CSI reports and a set of CSI-IM resource patterns corresponding to the set of CSI reports based on the signal strength measurement of the neighbor cell.",
          "claim_type": "dependent",
          "dependency": "claim 24",
          "is_exemplary": true
        },
        {
          "claim_number": "00030",
          "claim_text": "30. The apparatus of claim 23, in which a first frequency shift parameter (vShift) of cell-specific reference signal (CRS) resource elements (REs) of a serving cell of the second RAT is different from a second vShift of CRS REs of the neighbor cell.",
          "claim_type": "dependent",
          "dependency": "claim 23",
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.8,
      "publication_date": "2023-04-25",
      "patent_year": 2023
    },
    {
      "patent_id": "7450947",
      "title": "Method and apparatus for dynamic spectrum sharing",
      "abstract": "A technique for dynamic spectrum sharing includes identifying (705) a plurality of radio nodes (115, 120), measuring (710) a local signal value (SV) at each radio node (110, 200), and determining (715) a transmit decision. Each radio node can measure a local signal value (SV) of a protected transmission and the radio nodes are within a uniform SV region of the protected transmission. The transmit decision is determined for at least one of the plurality of radio nodes based on the SV of each radio node in the plurality of radio nodes and at least one threshold value that is related to statistical characteristics of the protected transmission at an interference boundary (105) of the protected transmission and a desired probability of non-interference with the protected transmission at the interference boundary.",
      "inventors": [
        "Eugene Visotsky",
        "Stephen L. Kuffner",
        "Roger L. Peterson"
      ],
      "assignees": [
        "Motorola, Inc."
      ],
      "claims": [],
      "relevance_score": 0.8,
      "publication_date": "2008-11-11",
      "patent_year": 2008
    },
    {
      "patent_id": "12238529",
      "title": "Electronic device and method of controlling electronic device in communication network supporting dynamic spectrum sharing",
      "abstract": "An electronic device is provided. The electronic device includes a communication processor, at least one Radio Frequency Integrated Circuit (RFIC) connected thereto, and an antenna connected through the at least one RFIC and configured to transmit and receive a signal corresponding to at least one communication network. The communication processor is configured to control the electronic device to receive a signal corresponding to a first communication network from a first base station corresponding to the first communication network supporting a first frequency band through the antenna, identify information related to a second communication network supporting a second frequency band including at least a portion of the first frequency band, identify a time interval allocated for transmission of data corresponding to the second communication network on the basis of the information related to the second communication network, and operate in a sleep state in the identified time interval.",
      "inventors": [
        "Dooyoung KIM",
        "Euichang JUNG",
        "Sunmin HWANG"
      ],
      "assignees": [
        "Samsung Electronics Co., Ltd."
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. An electronic device comprising:\na communication processor;\nat least one radio frequency integrated circuit (RFIC) connected to the communication processor;\nan antenna connected to the at least one RFIC and configured to transmit and receive a signal corresponding to at least one communication network, and\nmemory storing instructions,\nwherein the instructions, when executed by the communication processor, cause the electronic device to:\ncontrol the electronic device to receive a signal corresponding to a first communication network from a first base station corresponding to the first communication network supporting a first frequency band, through the antenna,\nidentify information related to a second communication network supporting a second frequency band including at least a portion of the first frequency band,\nidentify a time interval allocated for transmission of data corresponding to the second communication network, based on the information related to the second communication network, and\ncontrol the electronic device to operate in a sleep state in the identified time interval,\n\nwherein, when the first base station corresponding to a long term evolution (LTE) communication network does not transmit broadcast service data through predetermined subframes configured as multimedia broadcast multicast service single frequency network (MBSFN) subframes or does not transmit any data, dynamic spectrum sharing (DSS) in a time division multiplexing scheme is applied through the predetermined subframes.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The electronic device of claim 1, wherein the instructions further cause the electronic device to control to refrain from identifying control data corresponding to the first communication network while in the sleep state.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The electronic device of claim 1, wherein the instructions further cause the electronic device to identify the time interval allocated for transmission of the data corresponding to the second communication network when there is the second communication network supporting the second frequency band including at least the portion of the first frequency band.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The electronic device of claim 1, wherein the instructions further cause the electronic device to:\nreceive a signal transmitted from a second base station corresponding to the second communication network for a preset time, and\nidentify the time interval allocated for transmission of the data corresponding to the second communication network from the received signal.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The electronic device of claim 1, wherein the first base station corresponds to new radio (NR) communication network data in at least one subframe in which the LTE communication network data is not transmitted among predetermined subframes which are not configured as the MBSFN subframes and which are allocated for use by a second base station of the LTE communication network.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. One or more non-transitory computer-readable storage media storing one or more programs including computer-executable instructions that, when executed by one or more processors of an electronic device individually or collectively, cause to the electronic to perform operations, the operations comprising:\nreceiving a signal corresponding to a first communication network from a first base station corresponding to the first communication network supporting a first frequency band through an antenna;\nidentifying information related to a second communication network supporting a second frequency band including at least a portion of the first frequency band;\nidentifying a time interval allocated for transmission of data corresponding to the second communication network, based on the information related to the second communication network; and\ncontrolling the electronic device to operate in a sleep state in the identified time interval,\nwherein, when the first base station corresponding to a long term evolution (LTE) communication network does not transmit broadcast service data through predetermined subframes configured as multimedia broadcast multicast service single frequency network (MBSFN) subframes or does not transmit any data, dynamic spectrum sharing (DSS) in a time division multiplexing scheme is applied through the predetermined subframes.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The one or more non-transitory computer-readable storage media of claim 6, the operations further comprise controlling the electronic device to refrain from identifying control data corresponding to the first communication network while in the sleep state.",
          "claim_type": "dependent",
          "dependency": "claim 6",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The one or more non-transitory computer-readable storage media of claim 6, the operations further comprise identifying the time interval allocated for transmission of the data corresponding to the second communication network when there is the second communication network supporting the second frequency band including at least the portion of the first frequency band.",
          "claim_type": "dependent",
          "dependency": "claim 6",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. The one or more non-transitory computer-readable storage media of claim 8, the operations further comprise identifying whether there is the second communication network, based on frequency band information related to a neighbor base station of the first base station.",
          "claim_type": "dependent",
          "dependency": "claim 8",
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. The one or more non-transitory computer-readable storage media of claim 6, wherein the first base station corresponds to new radio (NR) communication network data in at least one subframe in which the LTE communication network data is not transmitted among predetermined subframes which are not configured as the MBSFN subframes and which are allocated for use by a second base station of the LTE communication network.",
          "claim_type": "dependent",
          "dependency": "claim 6",
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.8,
      "publication_date": "2025-02-25",
      "patent_year": 2025
    },
    {
      "patent_id": "12185118",
      "title": "Dual connectivity cell selection with dynamic spectrum sharing",
      "abstract": "The disclosed technology is directed towards avoiding a misconfiguration that uses a Long Term Evolution (LTE) and new radio dynamic spectrum sharing (DSS) carrier as an LTE carrier and new radio primary secondary cell carrier concurrently for a dual connectivity mobile device. Network equipment can detect the misconfiguration and prevent its usage, or if already configured, deconfigure the LTE DSS secondary cell during setup of a dual connectivity mobile device. Alternatively a dual connectivity mobile device can detect the misconfiguration and notify the network to terminate one of the carriers. Information regarding the misconfiguration can be saved in the mobile device to proactively avoid the dual misconfiguration going forward. Such information can be communicated to other mobile devices, as well as the network.",
      "inventors": [
        "Yupeng Jia"
      ],
      "assignees": [
        "AT&T Intellectual Property I, L.P."
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. A first mobile device, comprising:\na processor; and\na memory that stores executable instructions which, when executed by the processor of the first mobile device, facilitate performance of operations, the operations comprising:\ndetermining whether first dynamic spectrum sharing data corresponding to a long term evolution secondary cell of a communication network and second dynamic spectrum sharing data corresponding to a new radio primary secondary cell of the communication network have been concurrently received by the first mobile device via a frequency carrier;\nin response to the first dynamic spectrum sharing data and the second dynamic spectrum sharing data being determined to have been concurrently received by the first mobile device via the frequency carrier, performing an action to prevent a future reception, via the frequency carrier, of one of: the first dynamic spectrum sharing data or the second dynamic spectrum sharing data by the first mobile device; and\nsending a first dynamic spectrum sharing cell misconfiguration message to a second mobile device, wherein the first dynamic spectrum sharing cell misconfiguration message causes the communication network to drop the one of: the first dynamic spectrum sharing data or the second dynamic spectrum sharing data and to record, in a storage accessible to the first mobile device, a network identifier of the long term evolution secondary cell to avoid, based on the identifier, the future reception of the first dynamic spectrum sharing data by the first mobile device.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The first mobile device of claim 1, wherein the performing the action comprises terminating a usage of a long term evolution carrier associated with the long term evolution secondary cell.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The first mobile device of claim 2, wherein the terminating the usage of the long term evolution carrier comprises sending a long term evolution radio link failure message to network equipment of the communication network.",
          "claim_type": "dependent",
          "dependency": "claim 2",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The first mobile device of claim 2, wherein the terminating the usage of the long term evolution carrier comprises sending a second dynamic spectrum sharing cell misconfiguration message to network equipment of the communication network.",
          "claim_type": "dependent",
          "dependency": "claim 2",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The first mobile device of claim 1, wherein the performing the action comprises terminating a usage of a new radio carrier associated with the new radio primary secondary cell.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. The first mobile device of claim 5, wherein the terminating the usage of the new radio carrier comprises sending a secondary cell group radio link failure message to network equipment of the communication network.",
          "claim_type": "dependent",
          "dependency": "claim 5",
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The first mobile device of claim 5, wherein the terminating the usage of the new radio carrier comprises sending a second dynamic spectrum sharing cell misconfiguration message to network equipment of the communication network.",
          "claim_type": "dependent",
          "dependency": "claim 5",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The first mobile device of claim 1, wherein the sending comprises:\ncommunicating the first dynamic spectrum sharing cell misconfiguration message to the second mobile device via direct device-to-device communication.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. The first mobile device of claim 1, further comprising:\nbroadcasting the identifier of the long term evolution secondary cell to a third mobile device.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. Network equipment, comprising:\na processor; and\na memory that stores executable instructions which, when executed by the processor of the network equipment, facilitate performance of operations, the operations comprising:\nreceiving, from a dual connectivity mobile device, a dynamic spectrum sharing cell misconfiguration message;\ndetermining, in response to the receiving, that a long term evolution secondary cell of a communication network has been configured for a concurrent communication, via a carrier frequency, with the dual connectivity mobile device;\ndetermining, in response to the receiving, that a new radio primary secondary cell of the communication network has been configured for the concurrent communication with the dual connectivity mobile device;\ndetermining, in response to the receiving, that the dual connectivity mobile device has recorded, in a storage accessible to the dual connectivity mobile device, a network identifier of the long term evolution secondary cell to avoid, based on the identifier, a future reception of the concurrent communication by the dual connectivity mobile device; and\nin response to the determining that the long term evolution secondary cell and the new radio primary secondary cell have been configured for the concurrent communication, performing an action with respect to blocking a reception by the dual connectivity mobile device of dynamic spectrum sharing data corresponding to one of: the long term evolution secondary cell or the new radio primary secondary cell based on an indication in the dynamic spectrum sharing cell misconfiguration message that the dual connectivity mobile device has dropped the dynamic spectrum sharing data.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. The network equipment of claim 10, wherein the blocking the reception of the concurrent communication by the dual connectivity mobile device comprises: deconfiguring the long term evolution secondary cell in response to an indication in the dynamic spectrum sharing cell misconfiguration message.",
          "claim_type": "dependent",
          "dependency": "claim 10",
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. The network equipment of claim 11, wherein the deconfiguring the long term evolution secondary cell is performed during a dual connectivity setup of the dual connectivity mobile device.",
          "claim_type": "dependent",
          "dependency": "claim 11",
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. The network equipment of claim 11, wherein the blocking the reception of the concurrent communication by the dual connectivity mobile device comprises:\nexcluding the long term evolution secondary cell for usage by the dual connectivity mobile device until the new radio primary secondary cell is released by the dual connectivity mobile device.",
          "claim_type": "dependent",
          "dependency": "claim 11",
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. The network equipment of claim 10, wherein the blocking the reception of the concurrent communication by the dual connectivity mobile device comprises:\npreventing the long term evolution secondary cell from being utilized in concurrent communications comprising the concurrent communication corresponding to respective carrier frequencies comprising the carrier frequency.",
          "claim_type": "dependent",
          "dependency": "claim 10",
          "is_exemplary": true
        },
        {
          "claim_number": "00015",
          "claim_text": "15. The first mobile device of claim 10, wherein the second mobile device is a dual connectivity mobile device.",
          "claim_type": "dependent",
          "dependency": "claim 10",
          "is_exemplary": true
        },
        {
          "claim_number": "00016",
          "claim_text": "16. A non-transitory machine-readable medium, comprising executable instructions that, when executed by a processor of a first mobile device that is a dual connectivity mobile device, facilitate performance of operations of the processor, the operations comprising:\ndetermining that a long term evolution secondary cell of a cellular network and a new radio primary secondary cell of the cellular network have been misconfigured for a concurrent communication using a single carrier frequency;\nin response to the determining that the long term evolution secondary cell and the new radio primary secondary cell have been misconfigured, storing, in a data storage device of the dual connectivity mobile device, an identifier representing the long term evolution secondary cell;\nin response to detecting that the dual connectivity mobile device has left and subsequently re-entered a wireless coverage area of the long term evolution secondary cell, determining, based on the identifier that is stored, that a reception of the concurrent communication by the dual connectivity mobile device should be prevented while the dual connectivity mobile device remains within the wireless coverage area of the long term evolution secondary cell; and;\nand\ncommunicating, to a second mobile device, a dynamic spectrum sharing cell misconfiguration message that indicates that the long term evolution secondary cell and the new radio primary secondary cell have been misconfigured for the concurrent communication using the single carrier frequency, that the first mobile device has dropped dynamic spectrum sharing data corresponding to one of: the long term evolution secondary cell or the new radio primary secondary cell, and that the identifier has been recorded by the first mobile device to avoid the reception of the dynamic spectrum sharing data by the first mobile device while the first mobile device remains within the wireless coverage area of the long term evolution secondary cell.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00017",
          "claim_text": "17. The non-transitory machine-readable medium of claim 16, wherein the determining that the long term evolution secondary cell and the new radio primary secondary cell have been misconfigured comprises:\ncommunicating with network equipment of the cellular network to cease a long term evolution communication of the long term evolution secondary cell.",
          "claim_type": "dependent",
          "dependency": "claim 16",
          "is_exemplary": true
        },
        {
          "claim_number": "00018",
          "claim_text": "18. The non-transitory machine-readable medium of claim 16, wherein the operations further comprise:\nin response to entering the wireless coverage area of the long term evolution secondary cell, determining whether the identifier has been stored in the data storage device.",
          "claim_type": "dependent",
          "dependency": "claim 16",
          "is_exemplary": true
        },
        {
          "claim_number": "00019",
          "claim_text": "19. The non-transitory machine-readable medium of claim 16, wherein the second mobile device is a dual connectivity mobile device.",
          "claim_type": "dependent",
          "dependency": "claim 16",
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.8,
      "publication_date": "2024-12-31",
      "patent_year": 2024
    },
    {
      "patent_id": "12120531",
      "title": "Methods, systems, and apparatuses for handling dynamic spectrum sharing with uplink subcarrier shift",
      "abstract": "Embodiments described herein include methods, systems, and apparatuses for allowing a user equipment (UE) that supports dynamic spectrum sharing (DSS) with uplink (UL)-shift to access a cell and barring UEs that do not support DSS with UL-shift. Embodiments may use a cell barring field in a master information block and additional filters to indicate a barring state for a network node.",
      "inventors": [
        "Yuqin Chen",
        "Zhibin Wu",
        "Leilei Song",
        "Anatoliy Sergey Ioffe",
        "Fangli Xu",
        "Haijing Hu",
        "Sarma V. Vangala",
        "Naveen Kumar R Palle Venkata",
        "Ralf Rossbach",
        "Alexander Sayenko",
        "Ruoheng Liu"
      ],
      "assignees": [
        "Apple Inc."
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. A method for a user equipment (UE) that supports dynamic spectrum sharing (DSS) with uplink (UL)-shift, the method comprising:\nreceiving a first message from a network node, the first message comprising a cell barred field;\ndecoding the first message and determining status of the cell barred field;\nreceiving a second message from the network node comprising a second field related to barring UEs that support DSS with uplink-shift, and a third field related to support of UL-shift;\ndecoding the second message and determining status of the second field and the third field, wherein the second field is an exemption field which explicitly expresses whether UEs which support DSS with UL-shift are allowed to camp or not when the cell barred field is set to barred, and wherein the third field is a frequnecyShift7p5khz field; and\naccessing a cell when the cell barred field is set to barred and the second field indicates that the UEs which support DSS with UL-shift are allowed to access the cell, and the third field is set to true.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The method of claim 1, further comprising checking that the UE supports UL-shift only for an initial bandwidth part (BWP) against a particular sub-carrier spacing (SCS) the initial BWP is configured with, and wherein the UE accesses the cell when the UE supports UL-shift for the initial BWP.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The method of claim 1, further comprising checking that the UE supports UL shift for all the BWPs against a SCS broadcasted information provides, and wherein the UE accesses the cell only when the UE supports UL-shift for all BWPs.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The method of claim 1, wherein the first message is a master information block (MIB) and the second message is a system information block 1 (SIB1).",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The method of claim 1, wherein the second field is provided in a FrequencyInfoUL information element.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. The method of claim 1, further comprising reporting to the network node UL-shifting capability for each band that the UE supports.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. A user equipment (UE) that supports dynamic spectrum sharing (DSS) with uplink (UL)-shift, the UE comprising:\na baseband processing unit; and\na memory storing instructions that, when executed by the baseband processing unit, configure the UE to:\nreceive a first message from a network node, the first message comprising a cell barred field;\ndecode the first message and determining status of the cell barred field;\nreceive a second message from the network node comprising a second field related to barring UEs that support DSS with uplink-shift, and a third field related to support of UL-shift;\ndecode the second message and determining status of the second field and the third field, wherein the second field is an exemption field which explicitly expresses whether UEs which support DSS with UL-shift are allowed to camp or not when the cell barred field is set to barred, and wherein the third field is a frequencyShift7p5 hz field;\naccess a cell when the cell barred field is set to barred and the second field indicates that the UEs which support DSS with UL-shift are allowed to access the cell, and the third field is set to true.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The UE of claim 7, wherein the instructions further configure the baseband processing unit to check that the UE supports UL-shift only for an initial bandwidth part (BWP) against a particular sub-carrier spacing (SCS) the initial BWP is configured with, and wherein the UE accesses the cell when the UE supports UL-shift for the initial BWP.",
          "claim_type": "dependent",
          "dependency": "claim 7",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. The UE of claim 7, wherein the instructions further configure the baseband processing unit to check that the UE supports UL shift for all the BWPs against a SCS broadcasted information provides, and wherein the UE accesses the cell only when the UE supports UL-shift for all BWPs.",
          "claim_type": "dependent",
          "dependency": "claim 7",
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. The UE of claim 7, wherein the first message is a master information block (MIB) and the second message is a system information block 1 (SIB1).",
          "claim_type": "dependent",
          "dependency": "claim 7",
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. The UE of claim 7, wherein the second field is provided in a FrequencyInfoUL information element.",
          "claim_type": "dependent",
          "dependency": "claim 7",
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. The UE of claim 7, wherein the instructions further configure the baseband processing unit to report to the network node UL-shifting capability for each band that the UE supports.",
          "claim_type": "dependent",
          "dependency": "claim 7",
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. A non-transitory computer-readable storage medium of a user equipment (UE) that supports dynamic spectrum sharing (DSS) with uplink (UL)-shift, the computer-readable storage medium having computer-readable instructions stored thereon, the computer-readable instructions configured to instruct one or more processors to:\nreceive a first message from a network node, the first message comprising a cell barred field;\ndecode the first message and determining status of the cell barred field;\nreceive a second message from the network node comprising a second field related to barring UEs that support DSS with uplink-shift, and a third field related to support of UL-shift;\ndecode the second message and determining status of the second field and the third field, wherein the second field is an exemption field which explicitly expresses whether UEs which support DSS with UL-shift are allowed to camp or not when the cell barred field is set to barred, and wherein the third field is a frequencyShift7p5khz field;\naccess a cell when the cell barred field is set to barred and the second field indicates that the UEs which support DSS with UL-shift are allowed to access the cell, and the third field is set to true.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. The non-transitory computer-readable storage medium of claim 13, wherein the computer-readable instructions are configured to instruct the one or more processors to check that the UE supports UL-shift only for an initial bandwidth part (BWP) against a particular sub-carrier spacing (SCS) the initial BWP is configured with, and wherein the UE accesses the cell when the UE supports UL-shift for the initial BWP.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.8,
      "publication_date": "2024-10-15",
      "patent_year": 2024
    },
    {
      "patent_id": "12003975",
      "title": "Channel state information (CSI) measurement and report for dynamic spectrum sharing (DSS) in a wireless wide area network (WWAN)",
      "abstract": "This disclosure provides systems, methods, and apparatus, including computer programs encoded on computer-readable media, for implementing a channel state information (CSI) measurement and reporting protocol for dynamic spectrum sharing (DSS) in a wireless communication network. In some aspects, a BS may transmit control messages periodically and aperiodically that configure a UE to perform signal quality measurements and transmit signal quality reports. When the UE receives a periodic control message, the UE may perform signal quality measurements on both a multimedia broadcast single frequency network (MBSFN) subframe and a non-MBSFN subframe of a frame received from the BS. When the UE receives an aperiodic control message, the UE may perform a signal quality measurement on either a MBSFN subframe or a non-MBSFN subframe. The UE may generate and transmit signal quality reports to the BS periodically and aperiodically corresponding to the received periodic and aperiodic control messages, respectively.",
      "inventors": [
        "Juan Montojo",
        "Ming Yang",
        "Kausik Ray Chaudhuri"
      ],
      "assignees": [
        "QUALCOMM Incorporated"
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. A method for dynamic spectrum sharing (DSS) in a wireless wide area network (WWAN) performed by a first node, comprising:\nperforming a first signal quality measurement associated with a first subframe of a frame received from a second node, wherein the first subframe is associated with a first subframe type;\nperforming a second signal quality measurement associated with a second subframe of the frame, wherein the second subframe is associated with a second subframe type;\nidentifying that a first percentage of the frame includes subframes of the first subframe type, wherein the first signal quality measurement is associated with the subframes of the first subframe type;\nidentifying that a second percentage of the frame includes subframes of the second subframe type, wherein the second signal quality measurement is associated with the subframes of the second subframe type;\nweighing the first signal quality measurement according to the first percentage and the second signal quality measurement according to the second percentage;\ncalculating a third signal quality measurement using the weighted first signal quality measurement and the weighted second signal quality measurement; and\ntransmitting, to the second node, a first signal quality report associated with at least one of the first signal quality measurement and the second signal quality measurement and including the third signal quality measurement that is calculated using the weighted first signal quality measurement and the weighted second signal quality measurement.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The method of claim 1, wherein the first signal quality report is a channel state information (CSI) report, and performing the first signal quality measurement associated with the first subframe includes:\nperforming the first signal quality measurement on CSI reference signals (CSI-RSs) included in the first subframe, or\nperforming the first signal quality measurement on data included in the first subframe.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The method of claim 2, wherein:\nthe data includes data of a Physical Downlink Shared Channel (PDSCH).",
          "claim_type": "dependent",
          "dependency": "claim 2",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The method of claim 1, wherein performing the second signal quality measurement associated with the second subframe includes:\nperforming the second signal quality measurement on channel state information (CSI) reference signals (CSI-RSs) included in the second subframe, or\nperforming the second signal quality measurement on data included in the second subframe.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The method of claim 4, wherein:\nthe data includes data of a Physical Downlink Shared Channel (PDSCH).",
          "claim_type": "dependent",
          "dependency": "claim 4",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. The method of claim 4, wherein the first signal quality report is a CSI report.",
          "claim_type": "dependent",
          "dependency": "claim 4",
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The method of claim 1, wherein transmitting the first signal quality report including the third signal quality measurement comprises:\ntransmitting the first signal quality report including the third signal quality measurement periodically according to a time interval.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The method of claim 1, further comprising:\ngenerating one or more additional signal quality reports;\nindicating either the first signal quality measurement or the second signal quality measurement; and\ntransmitting the one or more additional signal quality reports to the second node.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. The method of claim 8, wherein transmitting the one or more additional signal quality reports comprises:\ntransmitting the one or more additional signal quality reports periodically according to a time interval.",
          "claim_type": "dependent",
          "dependency": "claim 8",
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. The method of claim 1, further comprising:\nreceiving a radio resource control (RRC) message from the second node; and\nperforming the first signal quality measurement and the second signal quality measurement based on receiving the RRC message from the second node.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. The method of claim 1, wherein the first subframe type is a multimedia broadcast single frequency network (MBSFN) subframe type and the second subframe type is a non-MBSFN subframe type.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. A method for dynamic spectrum sharing (DSS) in a wireless wide area network (WWAN) performed by a first node, comprising:\ntransmitting, to a second node, a control message that indicates one of a first subframe of a frame or a second subframe of the frame in which one or more channel state information (CSI) reference signals (CSI-RSs) are to be provided to the second node, wherein the first subframe is associated with a first subframe type and the second subframe is associated with a second subframe type;\nreceiving a first signal quality report from the second node, the first signal quality report indicating a third signal quality measurement that is a combination of a first signal quality measurement weighted by a percentage of the frame that includes subframes of the first subframe type and a second signal quality measurement weighted by a percentage of the frame that includes subframes of the second subframe type; and\nscheduling a data transmission in at least one of the first subframe and the second subframe, the scheduling being associated with the third signal quality measurement.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. The method of claim 12, wherein scheduling the data transmission in at least one of the first subframe and the second subframe includes at least one of:\nscheduling a first data transmission in the first subframe, the scheduling being associated with the first signal quality measurement; and\nscheduling a second data transmission in the second subframe, the scheduling being associated with the second signal quality measurement.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. The method of claim 13, wherein the first signal quality report further indicates at least one of the first signal quality measurement and the second signal quality measurement.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00015",
          "claim_text": "15. The method of claim 12, wherein receiving the first signal quality report indicating the third signal quality measurement comprises:\nreceiving the first signal quality report indicating the third signal quality measurement periodically according to a time interval.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00016",
          "claim_text": "16. The method of claim 12, wherein the first subframe type is a multimedia broadcast single frequency network (MBSFN) subframe type and the second subframe type is a non-MBSFN subframe type.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00017",
          "claim_text": "17. An apparatus of a first node configured to implement dynamic spectrum sharing (DSS) in a wireless wide area network (WWAN), the apparatus comprising:\none or more processors;\none or more memories coupled with the one or more processors; and\none or more processor-readable instructions stored in the one or more memories and executable by the one or more processors individually or collectively to cause the apparatus to:\nperform a first signal quality measurement associated with a first subframe of a frame received from a second node, and perform a second signal quality measurement associated with a second subframe of the frame, wherein the first subframe is associated with a first subframe type and the second subframe is associated with a second subframe type;\nidentify that a first percentage of the frame includes subframes of the first subframe type, wherein the first signal quality measurement is associated with the subframes of the first subframe type;\nidentify that a second percentage of the frame includes subframes of the second subframe type, wherein the second signal quality measurement is associated with the subframes of the second subframe type;\nweigh the first signal quality measurement according to the first percentage and the second signal quality measurement according to the second percentage;\ncalculate a third signal quality measurement using the weighted first signal quality measurement and the weighted second signal quality measurement; and\ntransmit, to the second node, a first signal quality report associated with at least one of the first signal quality measurement and the second signal quality measurement, and including the third signal quality measurement that is calculated using the weighted first signal quality measurement and the weighted second signal quality measurement.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00018",
          "claim_text": "18. The apparatus of claim 17, wherein the first signal quality report is a channel state information (CSI) report, and wherein, to perform the first signal quality measurement associated with the first subframe, the one or more processor-readable instructions are executable by the one or more processors individually or collectively to cause the apparatus to:\nperform the first signal quality measurement on CSI reference signals (CSI-RSs) included in the first subframe, or\nperform the first signal quality measurement on data included in the first subframe.",
          "claim_type": "dependent",
          "dependency": "claim 17",
          "is_exemplary": true
        },
        {
          "claim_number": "00019",
          "claim_text": "19. The apparatus of claim 18, wherein the data includes data of a Physical Downlink Shared Channel (PDSCH).",
          "claim_type": "dependent",
          "dependency": "claim 18",
          "is_exemplary": true
        },
        {
          "claim_number": "00020",
          "claim_text": "20. The apparatus of claim 17, wherein, to perform the second signal quality measurement associated with the second subframe, the one or more processor-readable instructions are executable by the one or more processors individually or collectively to cause the apparatus to:\nperform the second signal quality measurement on channel state information (CSI) reference signals (CSI-RSs) included in the second subframe, or\nperform the second signal quality measurement on data included in the second subframe.",
          "claim_type": "dependent",
          "dependency": "claim 17",
          "is_exemplary": true
        },
        {
          "claim_number": "00021",
          "claim_text": "21. The apparatus of claim 20, wherein the first signal quality report is a CSI report.",
          "claim_type": "dependent",
          "dependency": "claim 20",
          "is_exemplary": true
        },
        {
          "claim_number": "00022",
          "claim_text": "22. The apparatus of claim 20, wherein the data includes data of a Physical Downlink Shared Channel (PDSCH).",
          "claim_type": "dependent",
          "dependency": "claim 20",
          "is_exemplary": true
        },
        {
          "claim_number": "00023",
          "claim_text": "23. The apparatus of claim 17, wherein, to transmit the first signal quality report including the third signal quality measurement, the one or more processor-readable instructions are executable by the one or more processors individually or collectively to cause the apparatus to:\ntransmit the first signal quality report including the third signal quality measurement periodically according to a time interval.",
          "claim_type": "dependent",
          "dependency": "claim 17",
          "is_exemplary": true
        },
        {
          "claim_number": "00024",
          "claim_text": "24. The apparatus of claim 17, wherein the one or more processor-readable instructions are further executable by the one or more processors individually or collectively to cause the apparatus to:\ngenerate one or more additional signal quality reports; indicating either the first signal quality measurement or the second signal quality measurement; and\ntransmit the one or more additional signal quality reports to the second node.",
          "claim_type": "dependent",
          "dependency": "claim 17",
          "is_exemplary": true
        },
        {
          "claim_number": "00025",
          "claim_text": "25. The apparatus of claim 24, wherein, to transmit the one or more additional signal quality reports, the one or more processor-readable instructions are executable by the one or more processors individually or collectively to cause the apparatus to:\ntransmit the one or more additional signal quality reports periodically according to a time interval.",
          "claim_type": "dependent",
          "dependency": "claim 24",
          "is_exemplary": true
        },
        {
          "claim_number": "00026",
          "claim_text": "26. The apparatus of claim 17, wherein the one or more processor-readable instructions are further executable by the one or more processors individually or collectively to cause the apparatus to:\nreceive a radio resource control (RRC) message from the second node; and\nperform the first signal quality measurement and the second signal quality measurement based on reception of the RRC message from the second node.",
          "claim_type": "dependent",
          "dependency": "claim 17",
          "is_exemplary": true
        },
        {
          "claim_number": "00027",
          "claim_text": "27. The apparatus of claim 17, wherein the first subframe type is a multimedia broadcast single frequency network (MBSFN) subframe type and the second subframe type is a non-MBSFN subframe type.",
          "claim_type": "dependent",
          "dependency": "claim 17",
          "is_exemplary": true
        },
        {
          "claim_number": "00028",
          "claim_text": "28. An apparatus of a first node configured to implement dynamic spectrum sharing (DSS) in a wireless wide area network (WWAN), the apparatus comprising:\none or more processors;\none or more memories coupled with the one or more processors; and\none or more processor-readable instructions stored in the one or more memories and executable by the one or more processors individually or collectively to cause the apparatus to:\ntransmit, to a second node, a control message that indicates one of a first subframe of a frame or a second subframe of the frame in which one or more channel state information (CSI) reference signals (CSI-RSs) are to be provided to the second node, wherein the first subframe is associated with a first subframe type and the second subframe is associated with a second subframe type;\nreceive, from the second node, a first signal quality report indicating a third signal quality measurement that is a combination of a first signal quality measurement weighted by a percentage of the frame that includes subframes of the first subframe type and a second signal quality measurement weighted by a percentage of the frame that includes subframes of the second subframe type; and\nschedule a data transmission in at least one of the first subframe and the second subframe, the scheduled data transmission being associated with the third signal quality measurement.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00029",
          "claim_text": "29. The apparatus of claim 28, wherein, to schedule the data transmission in at least one of the first subframe and the second subframe, the one or more memories are executable by the one or more processors individually or collectively to cause the apparatus to:\nschedule a first data transmission in the first subframe, the scheduled first transmission being associated with the first signal quality measurement; and\nschedule a second data transmission in the second subframe, the scheduled second transmission being associated with the second signal quality measurement,\nwherein the first signal quality report further indicates at least one of the first signal quality measurement and the second signal quality measurement.",
          "claim_type": "dependent",
          "dependency": "claim 28",
          "is_exemplary": true
        },
        {
          "claim_number": "00030",
          "claim_text": "30. The apparatus of claim 28, wherein, to receive the first signal quality report indicating the third signal quality measurement, the one or more processor-readable instructions are executable by the one or more processors individually or collectively to cause the apparatus to:\nreceive the first signal quality report indicating the third signal quality measurement periodically according to a time interval.",
          "claim_type": "dependent",
          "dependency": "claim 28",
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.8,
      "publication_date": "2024-06-04",
      "patent_year": 2024
    },
    {
      "patent_id": "11943630",
      "title": "Enhancements for multiple radio protocol dynamic spectrum sharing",
      "abstract": "Methods, systems, and devices for wireless communications are described. Some wireless communications systems may support dynamic spectrum sharing for multiple radio protocols, such as New Radio and Long Term Evolution. Systems may implement a number of techniques to improve spectrum use by user equipment in dynamically shared frequency spectrums. In some aspects, the network may assign a user equipment to a specific bandwidth part based on a rate matching capability of the user equipment. Additionally or alternatively, the network may activate a specific bandwidth part based on the frequency of handover for a user equipment. In some aspects, the network may support dual registration (e.g., registration in a same frequency spectrum using different radio protocols) for a user equipment operating on a dynamically shared spectrum. To reduce the control overhead for such a user equipment, the network may use a single control channel to schedule data for multiple radio protocols.",
      "inventors": [
        "Akash Kumar"
      ],
      "assignees": [
        "QUALCOMM Incorporated"
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. A method for wireless communications implemented by a user equipment (UE), comprising:\nregistering, with a network entity, on a first cell supporting a first radio access technology in a frequency spectrum;\nregistering, with the network entity, on a second cell supporting a second radio access technology different from the first radio access technology and at least partially overlapping with the first cell in the frequency spectrum based at least in part on the network entity supporting dynamic sharing of the frequency spectrum between the first radio access technology and the second radio access technology;\nreceiving, via a control channel for the first radio access technology, a control message indicating a first set of resources in the frequency spectrum for communications using the first radio access technology and a second set of resources in the frequency spectrum for communications using the second radio access technology, wherein the first set of resources and the second set of resources are multiplexed according to a time division multiplexing scheme; and\ncommunicating with the network entity based at least in part on the registering on the first cell supporting the first radio access technology and the registering on the second cell supporting the second radio access technology.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The method of claim 1, further comprising:\nreceiving a cell identifier for the first cell, wherein the cell identifier indicates that the network entity supports the dynamic sharing of the frequency spectrum between the first radio access technology and the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The method of claim 1, wherein the communicating comprises:\nperforming data communications on the first cell using the first radio access technology; and\nperforming, at least partially concurrent to the performing the data communications, voice communications on the second cell using the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The method of claim 1, further comprising:\nestablishing a first radio bearer for the communicating with the network entity using the first radio access technology and a second radio bearer for the communicating with the network entity using the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The method of claim 1, further comprising:\ncaching, in local memory at the UE, an indication that the network entity supports the dynamic sharing of the frequency spectrum between the first radio access technology and the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. The method of claim 1, wherein the control message is received on a primary carrier corresponding to the first radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The method of claim 1, further comprising:\nusing a single radio frequency transceiver to receive the first set of resources and the second set of resources.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The method of claim 1, wherein the registering on the first cell supporting the first radio access technology and the registering on the second cell supporting the second radio access technology comprise a dual registration procedure.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. The method of claim 1, further comprising:\ndisplaying, in a user interface of the UE, an icon indicating that the UE supports the dynamic sharing of the frequency spectrum between the first radio access technology and the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. The method of claim 1, wherein the communicating comprises:\ncommunicating with the network entity on a first carrier using the first radio access technology based at least in part on the registering on the first cell supporting the first radio access technology; and\ncommunicating with the network entity on a second carrier using the second radio access technology based at least in part on the registering on the second cell supporting the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. The method of claim 10, wherein the first carrier and the second carrier are a same carrier.",
          "claim_type": "dependent",
          "dependency": "claim 10",
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. The method of claim 1, wherein:\nthe first radio access technology comprises a fifth generation radio technology; and\nthe second radio access technology comprises a long term evolution technology.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. A method for wireless communications implemented by a network entity, comprising:\nconfiguring a frequency spectrum for dynamic sharing between a first radio access technology and a second radio access technology;\nregistering a user equipment (UE) on a first cell supporting the first radio access technology in the frequency spectrum;\nregistering the UE on a second cell supporting the second radio access technology different from the first radio access technology and at least partially overlapping with the first cell in the frequency spectrum based at least in part on the configuring;\ntransmitting, via a control channel for the first radio access technology, a control message indicating a first set of resources in the frequency spectrum for communications using the first radio access technology and a second set of resources in the frequency spectrum for communications using the second radio access technology, wherein the first set of resources and the second set of resources are multiplexed according to a time division multiplexing scheme; and\ncommunicating with the UE based at least in part on the registering the UE on the first cell supporting the first radio access technology and the registering the UE on the second cell supporting the second radio access technology.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. The method of claim 13, further comprising:\ntransmitting a cell identifier for the first cell, the second cell, or both, wherein the cell identifier is associated with support of the dynamic sharing between the first radio access technology and the second radio access technology, wherein the registering the UE on the second cell supporting the second radio access technology is based at least in part on the cell identifier.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00015",
          "claim_text": "15. The method of claim 13, wherein the communicating comprises:\nperforming data communications on the first cell using the first radio access technology; and\nperforming, at least partially concurrent to the performing the data communications, voice communications on the second cell using the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00016",
          "claim_text": "16. The method of claim 15, further comprising:\ndirecting traffic associated with the voice communications to the second radio access technology based at least in part on the second radio access technology supporting a threshold quality of service for the voice communications.",
          "claim_type": "dependent",
          "dependency": "claim 15",
          "is_exemplary": true
        },
        {
          "claim_number": "00017",
          "claim_text": "17. The method of claim 15, further comprising:\nmaintaining data connectivity using the first radio access technology during the performing the voice communications using the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 15",
          "is_exemplary": true
        },
        {
          "claim_number": "00018",
          "claim_text": "18. The method of claim 13, wherein the registering the UE on the first cell supporting the first radio access technology and the registering the UE on the second cell supporting the second radio access technology comprise a dual registration procedure for the UE.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00019",
          "claim_text": "19. The method of claim 13, wherein the communicating comprises:\ncommunicating with the UE on a first carrier using the first radio access technology based at least in part on the registering the UE on the first cell supporting the first radio access technology; and\ncommunicating with the UE on a second carrier using the second radio access technology based at least in part on the registering the UE on the second cell supporting the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00020",
          "claim_text": "20. The method of claim 19, wherein the first carrier and the second carrier are a same carrier.",
          "claim_type": "dependent",
          "dependency": "claim 19",
          "is_exemplary": true
        },
        {
          "claim_number": "00021",
          "claim_text": "21. The method of claim 13, wherein:\nthe first radio access technology comprises a fifth generation radio technology; and\nthe second radio access technology comprises a long term evolution technology.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00022",
          "claim_text": "22. An apparatus for wireless communications implemented by a user equipment (UE), comprising:\na processor;\nmemory coupled with the processor; and\ninstructions stored in the memory and executable by the processor to cause the apparatus to:\nregister, with a network entity, on a first cell supporting a first radio access technology in a frequency spectrum;\nregister, with the network entity, on a second cell supporting a second radio access technology different from the first radio access technology and at least partially overlapping with the first cell in the frequency spectrum based at least in part on the network entity supporting dynamic sharing of the frequency spectrum between the first radio access technology and the second radio access technology;\nreceive, via a control channel for the first radio access technology, a control message indicating a first set of resources in the frequency spectrum for communications using the first radio access technology and a second set of resources in the frequency spectrum for communications using the second radio access technology, wherein the first set of resources and the second set of resources are multiplexed according to a time division multiplexing scheme; and\ncommunicate with the network entity based at least in part on the registering on the first cell supporting the first radio access technology and the registering on the second cell supporting the second radio access technology.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00023",
          "claim_text": "23. The apparatus of claim 22, wherein the instructions are further executable by the processor to cause the apparatus to receive a cell identifier for the first cell, wherein the cell identifier indicates that the network entity supports the dynamic sharing of the frequency spectrum between the first radio access technology and the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 22",
          "is_exemplary": true
        },
        {
          "claim_number": "00024",
          "claim_text": "24. The apparatus of claim 22, wherein the instructions to communicate are further executable by the processor to cause the apparatus to:\nperform data communications on the first cell using the first radio access technology; and\nperform, at least partially concurrent to the performing the data communications, voice communications on the second cell using the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 22",
          "is_exemplary": true
        },
        {
          "claim_number": "00025",
          "claim_text": "25. The apparatus of claim 22, wherein the instructions are further executable by the processor to cause the apparatus to cache, in local memory at the UE, an indication that the network entity supports the dynamic sharing of the frequency spectrum between the first radio access technology and the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 22",
          "is_exemplary": true
        },
        {
          "claim_number": "00026",
          "claim_text": "26. An apparatus for wireless communications implemented by a network entity, comprising:\na processor;\nmemory coupled with the processor; and\ninstructions stored in the memory and executable by the processor to cause the apparatus to:\nconfigure a frequency spectrum for dynamic sharing between a first radio access technology and a second radio access technology;\nregister a user equipment (UE) on a first cell supporting the first radio access technology in the frequency spectrum;\nregister the UE on a second cell supporting the second radio access technology different from the first radio access technology and at least partially overlapping with the first cell in the frequency spectrum based at least in part on the configuring;\ntransmit, via a control channel for the first radio access technology, a control message indicating a first set of resources in the frequency spectrum for communications using the first radio access technology and a second set of resources in the frequency spectrum for communications using the second radio access technology, wherein the first set of resources and the second set of resources are multiplexed according to a time division multiplexing scheme; and\ncommunicate with the UE based at least in part on the registering the UE on the first cell supporting the first radio access technology and the registering the UE on the second cell supporting the second radio access technology.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00027",
          "claim_text": "27. The apparatus of claim 26, wherein the instructions are further executable by the processor to cause the apparatus to transmit a cell identifier for the first cell, the second cell, or both, wherein the cell identifier is associated with support of the dynamic sharing between the first radio access technology and the second radio access technology, wherein the registering the UE on the second cell supporting the second radio access technology is based at least in part on the cell identifier.",
          "claim_type": "dependent",
          "dependency": "claim 26",
          "is_exemplary": true
        },
        {
          "claim_number": "00028",
          "claim_text": "28. The apparatus of claim 26, wherein the instructions to communicate are further executable by the processor to cause the apparatus to:\nperform data communications on the first cell using the first radio access technology; and\nperform, at least partially concurrent to the performing the data communications, voice communications on the second cell using the second radio access technology.",
          "claim_type": "dependent",
          "dependency": "claim 26",
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.8,
      "publication_date": "2024-03-26",
      "patent_year": 2024
    },
    {
      "patent_id": "11490381",
      "title": "Systems and methods for dynamic spectrum sharing (\u201cDSS\u201d) interleaving and pre-scheduling to optimize resource utilization",
      "abstract": "A system described herein may provide a scheduling technique for physical radio frequency (\u201cRF\u201d) resources of a base station of a radio access network (\u201cRAN\u201d) of a wireless network. Resources for a first group of User Equipment (\u201cUEs\u201d) may be allocated during or prior to a first time slot, and the UEs may be notified during the first time slot of the allocated resources. The allocated resources may be provided during a subsequent second time slot. A second group of UEs may be notified, during the first time slot, of physical RF resources allocated for downlink data for the second group of resources, and such downlink data may be provided to the second group of UEs during the first time slot via the allocated physical RF resources. The assignments of the UEs to the respective groups may change over time based on network load or other metrics.",
      "inventors": [
        "Xin Wang",
        "Susan Wu Sanders",
        "Nischal Patel",
        "Monte Giles"
      ],
      "assignees": [
        "Verizon Patent and Licensing Inc."
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. A device, comprising:\none or more processors configured to:\nreceive a request to allocate, for a User Equipment (\u201cUE\u201d), physical downlink radio frequency (\u201cRF\u201d) resources of a base station associated with a radio access network (\u201cRAN\u201d) of a wireless network;\nallocate, based on the request, a first set of downlink Physical Resource Blocks (\u201cPRBs\u201d) at a first time slot to indicate, to the UE, a second set of downlink PRBs, at a subsequent second time slot, that will be used to provide downlink data to the UE,\nwherein the first and second time slots are each subdivided into a plurality of symbols, and wherein allocating the first set of PRBs includes allocating the first set of PRBs at a last symbol of the plurality of symbols of the first time slot; and\n\nallocate, at the second subsequent time slot, the second set of downlink PRBs to provide the downlink data to the UE.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The device of claim 1, wherein the plurality of symbols consist of fourteen symbols, and wherein the last symbol is a fourteenth symbol of the fourteen symbols of the first time slot.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The device of claim 2, wherein allocating the second set of downlink PRBs includes allocating PRBs on symbols other than the first, second, third and fourteenth symbols of the fourteen symbols of the second time slot for the downlink data for the UE.",
          "claim_type": "dependent",
          "dependency": "claim 2",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. A device, comprising:\none or more processors configured to:\nreceive a first request to allocate, for a first User Equipment (\u201cUE\u201d), physical downlink radio frequency (\u201cRF\u201d) resources of a base station associated with a radio access network (\u201cRAN\u201d) of a wireless network;\nallocate, based on the first request, a first set of downlink Physical Resource Blocks (\u201cPRBs\u201d) at a first time slot to indicate, to the first UE, a second set of downlink PRBs, at a subsequent second time slot, that will be used to provide downlink data to the first UE;\nallocate, at the second subsequent time slot, the second set of downlink PRBs to provide the downlink data to the first UE;\nreceive a second request to allocate, for a second UE, physical downlink RF resources of the base station;\nallocate, based on the second request, a third set of PRBs at the first time slot to indicate, to the second UE, a fourth set of downlink PRBs, at the first time slot, that will be used to provide downlink data to the second UE; and\nallocate, at the first time slot, the fourth set of downlink PRBs to provide the downlink data to the second UE.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The device of claim 4, wherein the allocated first set of PRBs correspond to a Physical Downlink Control Channel (\u201cPDCCH\u201d), and wherein the allocated second set of PRBs correspond to a Physical Downlink Shared Channel (\u201cPDSCH\u201d).",
          "claim_type": "dependent",
          "dependency": "claim 4",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. A device, comprising:\none or more processors configured to:\nreceive a first request to allocate, for a first User Equipment (\u201cUE\u201d), physical downlink radio frequency (\u201cRF\u201d) resources of a base station associated with a radio access network (\u201cRAN\u201d) of a wireless network;\nallocate, based on the first request, a first set of downlink Physical Resource Blocks (\u201cPRBs\u201d) at a first time slot to indicate, to the first UE, a second set of downlink PRBs, at a subsequent second time slot, that will be used to provide downlink data to the first UE;\nallocate, at the second subsequent time slot, the second set of downlink PRBs to provide the downlink data to the first UE;\nidentify a second request, pending during the second time slot, to allocate physical RF resources for a second UE;\nallocate, based on the second request, a third set of PRBs at the second time slot to indicate, to the second UE, a fourth set of downlink PRBs, at the second time slot, that will be used to provide downlink data to the second UE; and\nallocate, at the second time slot, the fourth set of downlink PRBs to provide the downlink data to the second UE.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The device of claim 6, wherein allocating the second set of downlink PRBs includes allocating PRBs on symbols other than first and last symbols of the second time slot for the downlink data for the first UE.",
          "claim_type": "dependent",
          "dependency": "claim 6",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The device of claim 6, wherein the allocated first set of PRBs correspond to a Physical Downlink Control Channel (\u201cPDCCH\u201d), and wherein the allocated second set of PRBs correspond to a Physical Downlink Shared Channel (\u201cPDSCH\u201d).",
          "claim_type": "dependent",
          "dependency": "claim 6",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. A non-transitory computer-readable medium, storing a plurality of processor-executable instructions to:\nreceive a request to allocate, for a User Equipment (\u201cUE\u201d), physical downlink radio frequency (\u201cRF\u201d) resources of a base station associated with a radio access network (\u201cRAN\u201d) of a wireless network;\nallocate, based on the request, a first set of downlink Physical Resource Blocks (\u201cPRBs\u201d) at a first time slot to indicate, to the UE, a second set of downlink PRBs, at a subsequent second time slot, that will be used to provide downlink data to the UE,\nwherein the first and second time slots are each subdivided into a plurality of symbols, and wherein allocating the first set of PRBs includes allocating the first set of PRBs at a last symbol of the plurality of symbols of the first time slot; and\n\nallocate, at the second subsequent time slot, the second set of downlink PRBs to provide the downlink data to the UE.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. The non-transitory computer-readable medium of claim 9, wherein the plurality of symbols consist of fourteen symbols, and wherein the last symbol is a fourteenth symbol of the fourteen symbols of the first time slot.",
          "claim_type": "dependent",
          "dependency": "claim 9",
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. The non-transitory computer-readable medium of claim 10, wherein allocating the second set of downlink PRBs includes allocating PRBs on symbols other than the first, second, third and fourteenth symbols of the fourteen symbols of the second time slot for the downlink data for the UE.",
          "claim_type": "dependent",
          "dependency": "claim 10",
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. The non-transitory computer-readable medium of claim 9, wherein the allocated first set of PRBs correspond to a Physical Downlink Control Channel (\u201cPDCCH\u201d), and wherein the allocated second set of PRBs correspond to a Physical Downlink Shared Channel (\u201cPDSCH\u201d).",
          "claim_type": "dependent",
          "dependency": "claim 9",
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. The non-transitory computer-readable medium of claim 9, wherein the UE is a first UE, wherein the request is a first request, wherein the plurality of processor-executable instructions further include processor-executable instructions to:\nreceive a second request to allocate, for a second UE, physical downlink RF resources of the base station;\nallocate, based on the second request, a third set of PRBs at the first time slot to indicate, to the second UE, a fourth set of downlink PRBs, at the first time slot, that will be used to provide downlink data to the second UE; and\nallocate, at the first time slot, the fourth set of downlink PRBs to provide the downlink data to the second UE.",
          "claim_type": "dependent",
          "dependency": "claim 9",
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. The non-transitory computer-readable medium of claim 9, wherein the request is a first request, wherein the UE is a first UE, wherein the plurality of processor-executable instructions further include processor-executable instructions to:\nidentify a second request, pending during the second time slot, to allocate physical RF resources for a second UE;\nallocate, based on the second request, a third set of PRBs at the second time slot to indicate, to the second UE, a fourth set of downlink PRBs, at the second time slot, that will be used to provide downlink data to the second UE; and\nallocate, at the second time slot, the fourth set of downlink PRBs to provide the downlink data to the second UE.",
          "claim_type": "dependent",
          "dependency": "claim 9",
          "is_exemplary": true
        },
        {
          "claim_number": "00015",
          "claim_text": "15. A method, comprising:\nreceiving a first request to allocate, a first User Equipment (\u201cUE\u201d), physical downlink radio frequency (\u201cRF\u201d) resources of a base station associated with a radio access network (\u201cRAN\u201d) of a wireless network;\nallocating, based on the first request, a first set of downlink Physical Resource Blocks (\u201cPRBs\u201d) at a first time slot to indicate, to the first UE, a second set of downlink PRBs, at a subsequent second time slot, that will be used to provide downlink data to the first UE;\nallocating, at the second subsequent time slot, the second set of downlink PRBs to provide the downlink data to the UE;\nreceiving a second request to allocate, for a second UE, physical downlink RF resources of the base station;\nallocating, based on the second request, a third set of PRBs at the first time slot to indicate, to the second UE, a fourth set of downlink PRBs, at the first time slot, that will be used to provide downlink data to the second UE; and\nallocating, at the first time slot, the fourth set of downlink PRBs to provide the downlink data to the second UE.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00016",
          "claim_text": "16. The method of claim 15, wherein the first and second time slots are each subdivided into a fourteen symbols, wherein allocating the first set of PRBs includes allocating the first set of PRBs at a fourteenth symbol of the first time slot.",
          "claim_type": "dependent",
          "dependency": "claim 15",
          "is_exemplary": true
        },
        {
          "claim_number": "00017",
          "claim_text": "17. The method of claim 16, wherein allocating the second set of downlink PRBs includes allocating PRBs on symbols other than the first, second, third and fourteenth symbols of the fourteen symbols of the second time slot for the downlink data for the first UE.",
          "claim_type": "dependent",
          "dependency": "claim 16",
          "is_exemplary": true
        },
        {
          "claim_number": "00018",
          "claim_text": "18. A method, comprising:\nreceiving a first request to allocate, for a first User Equipment (\u201cUE\u201d), physical downlink radio frequency (\u201cRF\u201d) resources of a base station associated with a radio access network (\u201cRAN\u201d) of a wireless network;\nallocating, based on the first request, a first set of downlink Physical Resource Blocks (\u201cPRBs\u201d) at a first time slot to indicate, to the first UE, a second set of downlink PRBs, at a subsequent second time slot, that will be used to provide downlink data to the first UE;\nallocating, at the second subsequent time slot, the second set of downlink PRBs to provide the downlink data to the first UE;\nidentifying a second request, pending during the second time slot, to allocate physical RF resources for a second UE;\nallocating, based on the second request, a third set of PRBs at the second time slot to indicate, to the second UE, a fourth set of downlink PRBs, at the second time slot, that will be used to provide downlink data to the second UE; and\nallocating, at the second time slot, the fourth set of downlink PRBs to provide the downlink data to the second UE.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00019",
          "claim_text": "19. The method of claim 18, wherein the allocated first set of PRBs correspond to a Physical Downlink Control Channel (\u201cPDCCH\u201d), and wherein the allocated second set of PRBs correspond to a Physical Downlink Shared Channel (\u201cPDSCH\u201d).",
          "claim_type": "dependent",
          "dependency": "claim 18",
          "is_exemplary": true
        },
        {
          "claim_number": "00020",
          "claim_text": "20. The method of claim 18, wherein allocating the second set of downlink PRBs includes allocating PRBs on symbols other than first and last symbols of the second time slot for the downlink data for the first UE.",
          "claim_type": "dependent",
          "dependency": "claim 18",
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.7,
      "publication_date": "2022-11-01",
      "patent_year": 2022
    },
    {
      "patent_id": "11259263",
      "title": "Dual registration using dynamic spectrum sharing (DSS) in a wide area network (WAN)",
      "abstract": "This disclosure provides systems, methods, and apparatus, including computer programs encoded on computer-readable media, for implementing a dual registration mode and a dual receive mode using a single radio for wireless communications. A UE may determine that a wireless communication network supports the dual registration mode and dynamic spectrum sharing (DSS). The UE may establish a first connection with a first base station using a first radio access technology (RAT) of the wireless communication network. The UE may determine, based on one or more parameters associated with the DSS, that a second RAT of the wireless communication network has a second operating frequency band that overlaps a first operating frequency band of the first RAT. The UE may establish, via the second operating frequency band, a second connection with a second base station using the second RAT based on the dual registration mode and the DSS.",
      "inventors": [
        "Mohammad Suhel Ashfaque",
        "Avinash Dubey",
        "None Sagar"
      ],
      "assignees": [
        "QUALCOMM Incorporated"
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. A method performed by an apparatus of a user equipment (UE) for wireless communication in a dual receive mode using a single radio, comprising: determining that a wireless communication network supports a dual registration mode and dynamic spectrum sharing (DSS); establishing a first connection with a first base station using a first radio access technology (RAT) of the wireless communication network, the first RAT using a first operating frequency band; determining, based on one or more parameters associated with the DSS, that a second RAT of the wireless communication network has a second operating frequency band that overlaps the first operating frequency band of the first RAT; and establishing, via the second operating frequency band, a second connection with a second base station using the second RAT based on the dual registration mode and the DSS.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The method of claim 1 , wherein the first RAT is a 5G New Radio (NR) network and the second RAT is a long term evolution (LTE) network.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The method of claim 1 , further comprising: operating in the dual receive mode, a dual standby mode, and the dual registration mode using the single radio for wireless communications via the first connection using the first RAT and the second connection using the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The method of claim 1 , further comprising: receiving a registration message from the first base station, the registration message indicating that the wireless communication network supports the dual registration mode.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The method of claim 4 , wherein the registration message is a registration accept message, the registration accept message including a dual registration indication that indicates the wireless communication network supports the dual registration mode.",
          "claim_type": "dependent",
          "dependency": "claim 4",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. The method of claim 1 , wherein determining that the wireless communication network supports the DSS comprises: receiving the one or more parameters associated with the DSS from the first base station, the one or more parameters including a rate matching parameter that indicates the wireless communication network supports the DSS.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The method of claim 6 , wherein the rate matching parameter is an LTE cell-specific reference signal (CRS) rate matching parameter that indicates the wireless communication network supports the DSS and indicates the second operating frequency band of the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 6",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The method of claim 6 , wherein establishing the second connection with the second base station using the second RAT based on the dual registration mode and the DSS comprises: determining the second operating frequency band and a center frequency of the second operating frequency band based on the rate matching parameter; and searching for the center frequency of the second operating frequency band for establishing the second connection.",
          "claim_type": "dependent",
          "dependency": "claim 6",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. The method of claim 1 , further comprising: operating in an idle mode or a connected mode for the first connection that uses the first RAT; and operating in an idle mode for the second connection that uses the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. The method of claim 1 , further comprising: receiving a first communication associated with the first RAT from the first base station via the first connection having the first operating frequency band; receiving a second communication associated with the second RAT from the second base station via the second connection having the second operating frequency band; processing the first communication using a first processing unit associated with the first RAT; and processing the second communication using a second processing unit associated with the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. The method of claim 10 , further comprising: operating in an idle mode or a connected mode for the first connection that uses the first RAT; operating in an idle mode for the second connection that uses the second RAT; and receiving the second communication associated with the second RAT without performing a tuneaway operation.",
          "claim_type": "dependent",
          "dependency": "claim 10",
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. The method of claim 10 , further comprising: operating in an idle mode or a connected mode for the first connection that uses the first RAT; operating in an idle mode for the second connection that uses the second RAT; and receiving the first communication associated with the first RAT concurrently with the second communication associated with the second RAT without performing a tuneaway operation.",
          "claim_type": "dependent",
          "dependency": "claim 10",
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. The method of claim 10 , wherein the first RAT is a 5G New Radio (NR) network and the second RAT is a long term evolution (LTE) network, further comprising: operating in an idle mode or a connected mode for the first connection that uses the 5G NR network; operating in an idle mode for the second connection that uses the LTE network; and determining the second communication is an LTE page signal or an LTE cell-specific reference signal (CRS).",
          "claim_type": "dependent",
          "dependency": "claim 10",
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. An apparatus of a user equipment (UE) for wireless communication, comprising: an interface; and one or more processors, which together with the interface, are configured to: determine that a wireless communication network supports a dual registration mode and dynamic spectrum sharing (DSS); establish a first connection with a first base station using a first radio access technology (RAT) of the wireless communication network, the first RAT using a first operating frequency band; determine, based on one or more parameters associated with the DSS, that a second RAT of the wireless communication network has a second operating frequency band that overlaps the first operating frequency band of the first RAT; and establish a second connection with a second base station using the second RAT based on the dual registration mode and the DSS, the second RAT using the second operating frequency band.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00015",
          "claim_text": "15. The apparatus of claim 14 , wherein the interface includes a single radio, and the apparatus is configured to operate in a dual receive mode, a dual standby mode, and the dual registration mode using the single radio for wireless communications via the first connection using the first RAT and the second connection using the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00016",
          "claim_text": "16. The apparatus of claim 14 , wherein the first RAT is a 5G New Radio (NR) network and the second RAT is a long term evolution (LTE) network.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00017",
          "claim_text": "17. The apparatus of claim 14 , wherein the one or more processors, together with the interface, are further configured to: receive a registration message from the first base station, the registration message indicating that the wireless communication network supports the dual registration mode.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00018",
          "claim_text": "18. The apparatus of claim 17 , wherein the registration message is a registration accept message, the registration accept message including a dual registration indication that indicates the wireless communication network supports the dual registration mode.",
          "claim_type": "dependent",
          "dependency": "claim 17",
          "is_exemplary": true
        },
        {
          "claim_number": "00019",
          "claim_text": "19. The apparatus of claim 14 , wherein the one or more processors, together with the interface, are further configured to: receive the one or more parameters associated with the DSS from the first base station, the one or more parameters including a rate matching parameter that indicates the wireless communication network supports the DSS.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00020",
          "claim_text": "20. The apparatus of claim 19 , wherein the rate matching parameter is an LTE cell-specific reference signal (CRS) rate matching parameter that indicates the wireless communication network supports the DSS and indicates the second operating frequency band of the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 19",
          "is_exemplary": true
        },
        {
          "claim_number": "00021",
          "claim_text": "21. The apparatus of claim 19 , wherein the one or more processors, together with the interface, are further configured to: determine the second operating frequency band and a center frequency of the second operating frequency band based on the rate matching parameter; and search for the center frequency of the second operating frequency band to establish the second connection.",
          "claim_type": "dependent",
          "dependency": "claim 19",
          "is_exemplary": true
        },
        {
          "claim_number": "00022",
          "claim_text": "22. The apparatus of claim 14 , wherein the one or more processors, together with the interface, are further configured to: operate in an idle mode or a connected mode for the first connection that uses the first RAT; and operate in an idle mode for the second connection that uses the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00023",
          "claim_text": "23. The apparatus of claim 14 , wherein the one or more processors, together with the interface, are further configured to: receive a first communication associated with first RAT from the first base station via the first connection having the first operating frequency band; receive a second communication associated with the second RAT from the second base station via the second connection having the second operating frequency band; process the first communication associated with the first RAT; and process the second communication associated with the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 14",
          "is_exemplary": true
        },
        {
          "claim_number": "00024",
          "claim_text": "24. The apparatus of claim 23 , wherein the one or more processors, together with the interface, are further configured to: operate in an idle mode or a connected mode for the first connection that uses the first RAT; operate in an idle mode for the second connection that uses the second RAT; and receive the first communication associated with the first RAT concurrently with the second communication associated with the second RAT without performing a tuneaway operation.",
          "claim_type": "dependent",
          "dependency": "claim 23",
          "is_exemplary": true
        },
        {
          "claim_number": "00025",
          "claim_text": "25. An apparatus for wireless communication, comprising: means for determining that a wireless communication network supports a dual registration mode and dynamic spectrum sharing (DSS); means for establishing a first connection with a first base station using a first radio access technology (RAT) of the wireless communication network, the first RAT using a first operating frequency band; means for determining, based on one or more parameters associated with the DSS, that a second RAT of the wireless communication network has a second operating frequency band that overlaps the first operating frequency band of the first RAT; and means for establishing, via the second operating frequency band, a second connection with a second base station using the second RAT based on the dual registration mode and the DSS.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00026",
          "claim_text": "26. The apparatus of claim 25 , further comprising: means for operating in a dual receive mode, a dual standby mode, and the dual registration mode using a single radio for wireless communications via the first connection using the first RAT and the second connection using the second RAT and without performing tuneaway operations.",
          "claim_type": "dependent",
          "dependency": "claim 25",
          "is_exemplary": true
        },
        {
          "claim_number": "00027",
          "claim_text": "27. The apparatus of claim 25 , further comprising: means for receiving a registration message from the first base station, the registration message indicating that the wireless communication network supports the dual registration mode.",
          "claim_type": "dependent",
          "dependency": "claim 25",
          "is_exemplary": true
        },
        {
          "claim_number": "00028",
          "claim_text": "28. The apparatus of claim 25 , further comprising: means for receiving the one or more parameters associated with the DSS from the first base station, the one or more parameters including a rate matching parameter that indicates the wireless communication network supports the DSS.",
          "claim_type": "dependent",
          "dependency": "claim 25",
          "is_exemplary": true
        },
        {
          "claim_number": "00029",
          "claim_text": "29. A non-transitory computer-readable medium having stored therein instructions which, when executed by a processor of a user equipment (UE), cause the UE to: determine that a wireless communication network supports a dual registration mode and dynamic spectrum sharing (DSS); establish a first connection with a first base station using a first radio access technology (RAT) of the wireless communication network, the first RAT using a first operating frequency band; determine, based on one or more parameters associated with the DSS, that a second RAT of the wireless communication network has a second operating frequency band that overlaps the first operating frequency band of the first RAT; and establish, via the second operating frequency band, a second connection with a second base station using the second RAT based on the dual registration mode and the DSS.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00030",
          "claim_text": "30. The non-transitory computer-readable medium of claim 29 , wherein the instructions, when executed by the processor of the UE, further cause the UE to: operate in a dual receive mode, a dual standby mode, and the dual registration mode using a single radio for wireless communications via the first connection using the first RAT and the second connection using the second RAT.",
          "claim_type": "dependent",
          "dependency": "claim 29",
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.8,
      "publication_date": "2022-02-22",
      "patent_year": 2022
    },
    {
      "patent_id": "8892109",
      "title": "Method and apparatus of dynamic spectrum sharing in cellular networks",
      "abstract": "According to a disclosed method, an MME in a network analyzes KPIs from the cells it serves and based on the KPIs, it decides to engage in sharing. The MME then contacts a sharing entity (SE) to announce that it wants to supply spectrum for sharing. The MME obtains terms of a sharing agreement from the SE and the MME obtains the identity of the other network. In response to this information, the MME configures its base stations to support the supplying of spectrum to the other network. The SE applies knowledge of network topology and of services offered. This knowledge is obtained from a sharing database. At the expiration of the sharing agreement, the SE tells the MMEs to deactivate the sharing agreement.",
      "inventors": [
        "Jignesh S. Panchal",
        "Milind M. Buddhikot"
      ],
      "assignees": [
        "Alcatel Lucent"
      ],
      "claims": [],
      "relevance_score": 0.8,
      "publication_date": "2014-11-18",
      "patent_year": 2014
    },
    {
      "patent_id": "9538528",
      "title": "Efficient co-existence method for dynamic spectrum sharing",
      "abstract": "An apparatus defines a set of resources out of a first number of orthogonal radio resources and controls a transmitting means to simultaneously transmit a respective first radio signal for each resource on all resources of the set. A respective estimated interference is estimated on each of the resources of the set when the respective first radio signals are transmitted simultaneously. A first resource of the set is selected if the estimated interference on the first resource exceeds a first predefined level and, in the set, the first resource is replaced by a second resource of the first number of resources not having been part of the set. Each of the controlling and the estimating, the selecting, and the replacing is performed in order, respectively, for a predefined time.",
      "inventors": [
        "Istv\u00e1n Zsolt KOV\u00c1CS",
        "Andrea Cattoni",
        "Gustavo Wagner"
      ],
      "assignees": [
        "Nokia Solutions and Networks Oy"
      ],
      "claims": [],
      "relevance_score": 0.7,
      "publication_date": "2017-01-03",
      "patent_year": 2017
    }
  ],
  "status": "success",
  "search_result": {
    "query": "5G dynamic spectrum sharing",
    "total_found": 20,
    "patents": [
      {
        "patent_id": "12069484",
        "title": "Base station supporting dynamic spectrum sharing between heterogeneous networks and wireless communication system including the same",
        "abstract": "The present disclosure provides a wireless communication system. The wireless communication system includes a base station and a user equipment. The base station is configured to support dynamic spectrum sharing (DSS) between a first network and a second network. The user equipment is configured to communicate with the base station based on the first network. The base station is further configured to puncture allocation of a first reference signal when performing resource allocation on a first control channel in a case where a resource to be allocated to the first reference signal corresponding to the first network overlaps with resource allocated to a second reference signal corresponding to the second network. The user equipment is further configured to receive the first control channel and perform channel estimation for the first network, taking into account the first reference signal that has been punctured.",
        "inventors": [
          "Jinho Kim",
          "Jungmin Park"
        ],
        "assignees": [
          "Samsung Electronics Co., Ltd."
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. A wireless communication system comprising:\na base station configured to support dynamic spectrum sharing (DSS) between a first network and a second network; and\na user equipment configured to communicate with the base station based on the first network,\nwherein the base station is further configured to puncture allocation of a first reference signal when performing resource allocation on a first control channel and when a first resource to be allocated to the first reference signal corresponding to the first network overlaps with a second resource allocated to a second reference signal corresponding to the second network, and\nwherein the user equipment is further configured to receive the first control channel and perform channel estimation for the first network based on the allocation of the first reference signal that has been punctured,\nwherein the base station is further configured to allow at least two time-frequency domains among a plurality of time-frequency domains to overlap with a time-frequency domain allocated to the first control channel of the first network when performing the resource allocation, the plurality of time-frequency domains respectively corresponding to a plurality of carriers of the second network,\nwherein the base station is further configured to puncture the first reference signal on the at least two time-frequency domains according to a same first puncturing pattern when performing the resource allocation, and\nwherein the base station is further configured to allocate, according to a second puncturing pattern, the first reference signal to a time-frequency domain of a guard band between the at least two time-frequency domains.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The wireless communication system of claim 1, wherein:\nthe first network includes a new radio (NR) network,\nthe second network includes a long-term evolution (LTE) network,\nthe first reference signal includes a demodulation reference signal (DMRS), and\nthe second reference signal includes a cell reference signal (CRS).",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The wireless communication system of claim 1, wherein the base station is further configured to allow one time-frequency domain among a plurality of time-frequency domains to overlap with a time-frequency domain allocated to the first control channel of the first network when performing the resource allocation, the plurality of time-frequency domains respectively corresponding to a plurality of carriers of the second network.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The wireless communication system of claim 1, wherein the user equipment is further configured to perform the channel estimation using the second puncturing pattern of the first reference signal allocated to the time-frequency domain of the guard band.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The wireless communication system of claim 1, wherein the user equipment is further configured to perform the channel estimation using a portion of the second puncturing pattern of the first reference signal allocated to the time-frequency domain of the guard band, excluding the first puncturing pattern.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. The wireless communication system of claim 1, wherein the base station is further configured to allocate the first reference signal to some resources among a plurality of consecutive resources on a time axis, the some resources being expected not to overlap with the second resource allocated to the second reference signal, and puncture allocation of the first reference signal in a remaining resource expected to overlap with the second resource allocated to the second reference signal.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The wireless communication system of claim 6, wherein the user equipment is further configured not to use the first reference signal allocated to the some resources, based on the puncture allocation of the first reference signal being punctured as in the remaining resource, when performing the channel estimation.",
            "claim_type": "dependent",
            "dependency": "claim 6",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The wireless communication system of claim 1, wherein, when a demodulation reference signal (DMRS) precoding unit of a second control channel is set to a second control channel allocation region, the base station is further configured to perform resource allocation on the second control channel such that the second resource allocated to the second reference signal does not overlap with the first resource to be allocated to the first reference signal; and\nwherein the user equipment is further configured to receive the second control channel and perform the channel estimation for the first network, taking into account that the first reference signal is not punctured.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. The wireless communication system of claim 1, wherein, when a plurality of second reference signal rate matching patterns applicable to a frequency domain corresponding to a certain carrier are set for resource allocation on a second control channel, the base station is further configured to perform the resource allocation on the second control channel such that the second resource allocated to the second reference signal does not overlap with the first resource to be allocated to the first reference signal; and\nwherein the user equipment is further configured to receive the second control channel and perform the channel estimation for the first network based on the first reference signal not being punctured.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. The wireless communication system of claim 1, wherein the base station is further configured to perform the resource allocation on the first control channel based on a number of supported punctured first reference signal patterns the user equipment supports.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. The wireless communication system of claim 10, wherein the user equipment is further configured to transmit the number of supported punctured first reference signal patterns to the base station via radio resource control (RRC) signaling.",
            "claim_type": "dependent",
            "dependency": "claim 10",
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. An operating method of a base station supporting dynamic spectrum sharing (DSS) between a first network and a second network, the operating method comprising:\ndetermining, based on communication settings, that a first resource element is allocated to a first reference signal corresponding to the first network and to a second reference signal corresponding to the second network; and\nperforming resource allocation on a control channel with a puncture of allocation of the first resource to the first reference signal in response to the determination.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. The operating method of claim 12, wherein determining whether to allow the overlap comprises determining not to allow the overlap when a demodulation reference signal (DMRS) precoding unit of the control channel is set to a control channel allocation region in the communication settings, and\nwherein performing resource allocation on the control channel comprises allocating the first reference signal to a different resource than the second resource allocated to the second reference signal in response to the determination not to allow the overlap.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. The operating method of claim 12, wherein determining whether to allow the overlap comprises determining not to allow the overlap when a plurality of second reference signal rate matching patterns applicable to a frequency domain corresponding to a certain carrier are set in the communication settings; and\nwherein performing resource allocation on the control channel comprises allocating different resources to the first reference signal and the second reference signal, respectively, in response to the determination not to allow the overlap.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00015",
            "claim_text": "15. A wireless communication system comprising:\na base station configured to support dynamic spectrum sharing (DSS) between a first network and a second network; and\na user equipment configured to communicate with the base station based on the first network,\nwherein the base station is further configured to puncture allocation of a first reference signal when performing resource allocation on a first control channel and when a first resource to be allocated to the first reference signal corresponding to the first network overlaps with a second resource allocated to a second reference signal corresponding to the second network, and\nwherein the user equipment is further configured to receive the first control channel and perform channel estimation for the first network based on the allocation of the first reference signal that has been punctured,\nwherein the base station is further configured to perform the resource allocation on the first control channel based on a number of supported punctured first reference signal patterns the user equipment supports.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.9,
        "publication_date": "2024-08-20",
        "patent_year": 2024
      },
      {
        "patent_id": "12192952",
        "title": "Efficient positioning enhancement for dynamic spectrum sharing",
        "abstract": "Techniques are provided for transmitting Positioning Reference Signals (PRSs) in cells supporting two different Radio Access Technologies (RATs), where the two RATs (e.g. 4G LTE and 5G NR) employ dynamic spectrum sharing. To avoid interference between the PRSs and between the two RATs, the PRSs may be time aligned to the same set of PRS positioning occasions, and may be assigned orthogonal characteristics such as different muting patterns, orthogonal code sequences, different frequency shifts or different frequency hopping. UEs supporting both RATs may be enabled to measure PRSs for both RATs. UEs supporting only one RAT (e.g. 4G LTE) may be enabled to measure PRSs for just this RAT. A location server such as an LMF, E-SMLC or SLP may provide assistance data to UEs, and request measurements from UEs, for PRSs in one or both RATs.",
        "inventors": [
          "Stephen William Edge",
          "Bapineedu Chowdary Gummadi",
          "Hem Agnihotri"
        ],
        "assignees": [
          "QUALCOMM Incorporated"
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. A method, at a network server, to support positioning of a mobile device with dynamic spectrum sharing, comprising:\nreceiving a first set of location measurements obtained by the mobile device for first positioning reference signals (PRSs) transmitted in a first plurality of cells, the first plurality of cells using a first radio access technology (RAT);\nreceiving a second set of location measurements obtained by the mobile device for second PRSs transmitted in a second plurality of cells, the second plurality of cells using a second RAT, wherein the first RAT and the second RAT are different radio access technologies operating on the same radio frequency band, with the first set of location measurements corresponding to first PRS positioning occasions of the first PRSs scheduled for occurrence at the same time with second PRS positioning occasions of the second PRSs corresponding to the second set of location measurements; and\ndetermining a location of the mobile device based at least in part on the first set of location measurements and the second set of location measurements.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The method of claim 1, wherein the first RAT is 4G Long Term Evolution (LTE) and the second RAT is 5G New Radio (NR).",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The method of claim 1, wherein the network server comprises a Location Management Function (LMF), an Enhanced Serving Mobile Location Center (E-SMLC), or a Secure User Plane Location (SUPL) Location Platform (SLP).",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The method of claim 1, wherein the first set of location measurements and the second set of location measurements each comprise measurements comprising at least one of a Time of Arrival (TOA), a Received Signal Strength Indication (RSSI), a Round Trip signal propagation Time (RTT), a Reference Signal Time Difference (RSTD), a Reference Signal Received Power (RSRP), a Receive Time-Transmission Time difference (Rx-Tx), a Reference Signal Received Quality (RSRQ), or some combination of these.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The method of claim 1, wherein each PRS in the first PRSs and the second PRSs comprises a sequence of PRS positioning occasions, wherein the sequence of PRS positioning occasions for each PRS occur at the same times as the sequence of PRS positioning occasions for each of other PRSs in the first PRSs and the second PRSs.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. The method of claim 1, wherein each PRS in the first PRSs and the second PRSs includes orthogonal characteristics, wherein the orthogonal characteristics reduce interference between the each PRS and other PRSs in the first PRSs and the second PRSs.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The method of claim 6, wherein the orthogonal characteristics include at least one of a distinct frequency shift, an orthogonal PRS code sequence, a distinct frequency hopping sequence, a distinct muting pattern, or some combination of these.",
            "claim_type": "dependent",
            "dependency": "claim 6",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The method of claim 6, wherein the orthogonal characteristics include a distinct muting pattern, wherein the each PRS is transmitted during PRS positioning occasions in which PRS is not transmitted for some other PRSs in the first PRSs and the second PRSs, wherein the each PRS is not transmitted during PRS positioning occasions in which PRS is transmitted for at least some of the some other PRSs in the first PRSs and the second PRSs.",
            "claim_type": "dependent",
            "dependency": "claim 6",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. The method of claim 8, further comprising sending assistance data to the mobile device, the assistance data including a configuration of each PRS in the first PRSs and the second PRSs, the configuration including an indication of the PRS positioning occasions and the orthogonal characteristics for the each PRS, wherein the first set of location measurements and the second set of location measurements are obtained by the mobile device based in part on the configuration of each PRS in the first PRSs and the second PRSs.",
            "claim_type": "dependent",
            "dependency": "claim 8",
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. The method of claim 1, wherein the radio frequency band includes frequencies in a range of 600 MHz to 700 MHz or in a range of 2.5 GHz to 3.5 GHz.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. An apparatus, comprising:\na memory;\na transceiver;\na processor communicatively coupled to the memory and the transceiver and configured to:\nreceive a first set of location measurements obtained by a mobile device for first positioning reference signals (PRSs) transmitted in a first plurality of cells, the first plurality of cells using a first radio access technology (RAT);\nreceive a second set of location measurements obtained by the mobile device for second PRSs transmitted in a second plurality of cells, the second plurality of cells using a second RAT, wherein the first RAT and the second RAT are different radio access technologies operating on the same radio frequency band, with the first set of location measurements corresponding to first PRS positioning occasions of the first PRSs scheduled for occurrence at the same time with second PRS positioning occasions of the second PRSs corresponding to the second set of location measurements; and\ndetermine a location of the mobile device based at least in part on the first set of location measurements and the second set of location measurements.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. The apparatus of claim 11 wherein the first RAT is 4G Long Term Evolution (LTE) and the second RAT is 5G New Radio (NR).",
            "claim_type": "dependent",
            "dependency": "claim 11",
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. The apparatus of claim 11, wherein the apparatus comprises a Location Management Function (LMF), an Enhanced Serving Mobile Location Center (E-SMLC), or a Secure User Plane Location (SUPL) Location Platform (SLP).",
            "claim_type": "dependent",
            "dependency": "claim 11",
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. The apparatus of claim 11, wherein the first set of location measurements and the second set of location measurements each comprise measurements comprising at least one of a Time of Arrival (TOA), a Received Signal Strength Indication (RSSI), a Round Trip signal propagation Time (RTT), a Reference Signal Time Difference (RSTD), a Reference Signal Received Power (RSRP), a Receive Time-Transmission Time difference (Rx-Tx), a Reference Signal Received Quality (RSRQ), or some combination of these.",
            "claim_type": "dependent",
            "dependency": "claim 11",
            "is_exemplary": true
          },
          {
            "claim_number": "00015",
            "claim_text": "15. The apparatus of claim 11, wherein each PRS in the first PRSs and the second PRSs comprises a sequence of PRS positioning occasions, wherein the sequence of PRS positioning occasions for each PRS occur at the same times as the sequence of PRS positioning occasions for each of other PRSs in the first PRSs and the second PRSs.",
            "claim_type": "dependent",
            "dependency": "claim 11",
            "is_exemplary": true
          },
          {
            "claim_number": "00016",
            "claim_text": "16. The apparatus of claim 11, wherein each PRS in the first PRSs and the second PRSs includes orthogonal characteristics, wherein the orthogonal characteristics reduce interference between the each PRS and other PRSs in the first PRSs and the second PRSs.",
            "claim_type": "dependent",
            "dependency": "claim 11",
            "is_exemplary": true
          },
          {
            "claim_number": "00017",
            "claim_text": "17. The apparatus of claim 16, wherein the orthogonal characteristics include at least one of a distinct frequency shift, an orthogonal PRS code sequence, a distinct frequency hopping sequence, a distinct muting pattern, or some combination of these.",
            "claim_type": "dependent",
            "dependency": "claim 16",
            "is_exemplary": true
          },
          {
            "claim_number": "00018",
            "claim_text": "18. The apparatus of claim 16, wherein the orthogonal characteristics include a distinct muting pattern, wherein the each PRS is transmitted during PRS positioning occasions in which PRS is not transmitted for some other PRSs in the first PRSs and the second PRSs, wherein the each PRS is not transmitted during PRS positioning occasions in which PRS is transmitted for at least some of the some other PRSs in the first PRSs and the second PRSs.",
            "claim_type": "dependent",
            "dependency": "claim 16",
            "is_exemplary": true
          },
          {
            "claim_number": "00019",
            "claim_text": "19. The apparatus of claim 18, wherein the processor is further configured to send assistance data to the mobile device, the assistance data including a configuration of each PRS in the first PRSs and the second PRSs, the configuration including an indication of the sequence of PRS positioning occasions and the orthogonal characteristics for the each PRS, wherein the first set of location measurements and the second set of location measurements are obtained by the mobile device based in part on the configuration of each PRS in the first PRSs and the second PRSs.",
            "claim_type": "dependent",
            "dependency": "claim 18",
            "is_exemplary": true
          },
          {
            "claim_number": "00020",
            "claim_text": "20. The apparatus of claim 11, wherein the radio frequency band includes frequencies in a range of 600 MHz to 700 MHz or in a range of 2.5 GHz to 3.5 GHZ.",
            "claim_type": "dependent",
            "dependency": "claim 11",
            "is_exemplary": true
          },
          {
            "claim_number": "00021",
            "claim_text": "21. An apparatus, comprising:\nmeans for receiving a first set of location measurements obtained by a mobile device for first positioning reference signals (PRSs) transmitted in a first plurality of cells, the first plurality of cells using a first radio access technology (RAT);\nmeans for receiving a second set of location measurements obtained by the mobile device for second PRSs transmitted in a second plurality of cells, the second plurality of cells using a second RAT, wherein the first RAT and the second RAT are different radio access technologies operating on the same radio frequency band, with the first set of location measurements corresponding to first PRS positioning occasions of the first PRSs scheduled for occurrence at the same time with second PRS positioning occasions of the second PRSs corresponding to the second set of location measurements; and\nmeans for determining a location of the mobile device based at least in part on the first set of location measurements and the second set of location measurements.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00022",
            "claim_text": "22. The apparatus of claim 21, wherein the first RAT is 4G Long Term Evolution (LTE) and the second RAT is 5G New Radio (NR).",
            "claim_type": "dependent",
            "dependency": "claim 21",
            "is_exemplary": true
          },
          {
            "claim_number": "00023",
            "claim_text": "23. The apparatus of claim 21, wherein the apparatus comprises a Location Management Function (LMF), an Enhanced Serving Mobile Location Center (E-SMLC), or a Secure User Plane Location (SUPL) Location Platform (SLP).",
            "claim_type": "dependent",
            "dependency": "claim 21",
            "is_exemplary": true
          },
          {
            "claim_number": "00024",
            "claim_text": "24. The apparatus of claim 21, wherein the first set of location measurements and the second set of location measurements each comprise measurements comprising at least one of a Time of Arrival (TOA), a Received Signal Strength Indication (RSSI), a Round Trip signal propagation Time (RTT), a Reference Signal Time Difference (RSTD), a Reference Signal Received Power (RSRP), a Receive Time-Transmission Time difference (Rx-Tx), a Reference Signal Received Quality (RSRQ), or some combination of these.",
            "claim_type": "dependent",
            "dependency": "claim 21",
            "is_exemplary": true
          },
          {
            "claim_number": "00025",
            "claim_text": "25. The apparatus of claim 21, wherein each PRS in the first PRSs and the second PRSs comprises a sequence of PRS positioning occasions, wherein the sequence of PRS positioning occasions for each PRS occur at the same times as the sequence of PRS positioning occasions for each of other PRSs in the first PRSs and the second PRSs.",
            "claim_type": "dependent",
            "dependency": "claim 21",
            "is_exemplary": true
          },
          {
            "claim_number": "00026",
            "claim_text": "26. The apparatus of claim 21, wherein each PRS in the first PRSs and the second PRSs includes orthogonal characteristics, wherein the orthogonal characteristics reduce interference between the each PRS and other PRSs in the first PRSs and the second PRSs.",
            "claim_type": "dependent",
            "dependency": "claim 21",
            "is_exemplary": true
          },
          {
            "claim_number": "00027",
            "claim_text": "27. The apparatus of claim 26, wherein the orthogonal characteristics include at least one of a distinct frequency shift, an orthogonal PRS code sequence, a distinct frequency hopping sequence, a distinct muting pattern, or some combination of these.",
            "claim_type": "dependent",
            "dependency": "claim 26",
            "is_exemplary": true
          },
          {
            "claim_number": "00028",
            "claim_text": "28. The apparatus of claim 26, wherein the orthogonal characteristics include a distinct muting pattern, wherein the each PRS is transmitted during PRS positioning occasions in which PRS is not transmitted for some other PRSs in the first PRSs and the second PRSs, wherein the each PRS is not transmitted during PRS positioning occasions in which PRS is transmitted for at least some of the some other PRSs in the first PRSs and the second PRSs.",
            "claim_type": "dependent",
            "dependency": "claim 26",
            "is_exemplary": true
          },
          {
            "claim_number": "00029",
            "claim_text": "29. The apparatus of claim 28, further comprising means for sending assistance data to the mobile device, the assistance data including a configuration of each PRS in the first PRSs and the second PRSs, the configuration including an indication of the sequence of PRS positioning occasions and the orthogonal characteristics for the each PRS, wherein the first set of location measurements and the second set of location measurements are obtained by the mobile device based in part on the configuration of each PRS in the first PRSs and the second PRSs.",
            "claim_type": "dependent",
            "dependency": "claim 28",
            "is_exemplary": true
          },
          {
            "claim_number": "00030",
            "claim_text": "30. The apparatus of claim 21, wherein the radio frequency band includes frequencies in a range of 600 MHz to 700 MHz or in a range of 2.5 GHz to 3.5 GHz.",
            "claim_type": "dependent",
            "dependency": "claim 21",
            "is_exemplary": true
          },
          {
            "claim_number": "00031",
            "claim_text": "31. A non-transitory processor-readable storage medium comprising processor-readable instructions configured to cause one or more processors to support positioning of a mobile device with dynamic spectrum sharing, comprising:\ncode for receiving a first set of location measurements obtained by the mobile device for first positioning reference signals (PRSs) transmitted in a first plurality of cells, the first plurality of cells using a first radio access technology (RAT);\ncode for receiving a second set of location measurements obtained by the mobile device for second PRSs transmitted in a second plurality of cells, the second plurality of cells using a second RAT, wherein the first RAT and the second RAT are different radio access technologies operating on the same radio frequency band, with the first set of location measurements corresponding to first PRS positioning occasions of the first PRSs scheduled for occurrence at the same time with second PRS positioning occasions of the second PRSs corresponding to the second set of location measurements; and\ncode for determining a location of the mobile device based at least in part on the first set of location measurements and the second set of location measurements.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00032",
            "claim_text": "32. The non-transitory processor-readable storage medium of claim 31, further comprising code for sending assistance data to the mobile device, the assistance data including a configuration of each PRS in the first PRSs and the second PRSs, the configuration including an indication of a sequence of PRS positioning occasions and orthogonal characteristics for the each PRS, wherein the first set of location measurements and the second set of location measurements are obtained by the mobile device based in part on the configuration of each PRS in the first PRSs and the second PRSs.",
            "claim_type": "dependent",
            "dependency": "claim 31",
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.8,
        "publication_date": "2025-01-07",
        "patent_year": 2025
      },
      {
        "patent_id": "12063645",
        "title": "Scheduling restriction enhancements for LTE and 5G NR dynamic spectrum sharing",
        "abstract": "Methods and devices for a base station acting as a primary cell to perform dual spectrum sharing (DSS) with a first user equipment device (UE) over a 5G NR connection and a second UE over an LTE connection. The first UE establishes the 5G NR connection with the primary cell and one or more secondary cells. One of the secondary cells is configured in the 5G NR connection to provide downlink control information to the UE for the primary cell, to avoid collisions by the primary cell with LTE control transmissions.",
        "inventors": [
          "Hong He",
          "Chunhai Yao",
          "Sigen Ye",
          "Dawei Zhang",
          "Chunxuan Ye",
          "Weidong Yang",
          "Wei Zeng",
          "Yushu Zhang",
          "Oghenekome Oteri",
          "Huaning Niu",
          "Haitong Sun",
          "Wei Zhang"
        ],
        "assignees": [
          "Apple Inc."
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. A method comprising:\nby a base station:\nestablishing a connection as a primary cell with a user equipment device (UE);\nproviding a first indication to the UE to monitor a common search space (CSS) for first downlink control information (DCI) from the primary cell, wherein the first DCI is for scheduling of the primary cell for the UE;\nproviding a second indication to the UE to monitor a UE-specific search space (USS) for second DCI from a secondary cell, wherein the second DCI is for cross-carrier scheduling to the primary cell for the UE, wherein the second DCI has a 5G NR DCI format of 0_1, 0_2, 1_1 or 1_2, and wherein, regardless of a monitoring capability of the UE, all physical downlink control channel (PDCCH) monitoring occasions on the secondary cell for DCIs for cross-carrier scheduling to the primary cell for the UE are constrained to be within an initial three symbols of a slot; and\n\noperating the connection according to the first DCI and the second DCI.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The method of claim 1, wherein the connection with the UE utilizes a 5th Generation New Radio (5G NR) radio access technology (RAT), wherein the method further comprises:\nestablishing a second connection with a second UE using a Long Term Evolution (LTE) RAT, wherein the first DCI is scheduled to not overlap with third DCI transmitted for the second connection.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The method of claim 2,\nwherein the base station communicates with the UE and the second UE using a 15 kHz subcarrier spacing, and\nwherein the secondary cell communicates with the UE using either the 15 kHz or a 30 kHz subcarrier spacing.",
            "claim_type": "dependent",
            "dependency": "claim 2",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The method of claim 1, further comprising:\nproviding a third indication to the UE to monitor the USS for third DCI from the secondary cell, wherein the third DCI schedules a communication with a second secondary cell.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The method of claim 1,\nwherein operating the connection according to the first DCI and the second DCI comprises one or more of:\nreceiving one or more uplink communications from the UE according to scheduling information of the first DCI or the second DCI;\ntransmitting one or more downlink communications to the UE according to the scheduling information of the first DCI or the second DCI.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. The method of claim 1,\nwherein the first DCI has:\na 5th Generation New Radio (5G NR) fallback DCI format of 0_0 or 1_0; or\na 5G NR special DCI format of 2_0, 2_1, 2_2, 2_3, 2_4, 2_5 or 2_6.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The method of claim 1,\nwherein the first DCI has:\na 5th Generation New Radio (5G NR) fallback DCI format of 0_0 or 1_0.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The method of claim 1,\nwherein the first indication and the second indication comprise one or more radio resource control (RRC) configuration messages.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. The method of claim 1,\nwherein the first DCI and the second DCI each comprise one or more of:\na scheduling indication for an uplink communication with the primary cell;\na scheduling indication for a downlink communication with the primary cell; and\na control message indicating a behavior modification of the UE.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. A base station, comprising:\na radio;\na processor communicatively coupled to the radio, wherein the base station is configured to:\nestablish a connection as a primary cell with a user equipment device (UE);\nprovide a first indication to the UE to monitor a common search space (CSS) for first downlink control information (DCI) from the primary cell, wherein the first DCI is for scheduling of the primary cell for the UE;\nprovide a second indication to the UE to monitor a UE-specific search space (USS) for second DCI from a secondary cell, wherein the second DCI is for cross-carrier scheduling to the primary cell for the UE, and wherein the second DCI has a 5G NR DCI format of 0_1, 0_2, 1_1 or 1_2, wherein, regardless of a monitoring capability of the UE, all physical downlink control channel (PDCCH) monitoring occasions on the secondary cell for DCIs for cross-carrier scheduling to the primary cell for the UE are constrained to be within an initial three symbols of a slot; and\noperate the connection according to the first DCI and the second DCI.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. The base station of claim 10, wherein the connection with the UE utilizes a 5th Generation New Radio (5G NR) radio access technology (RAT), wherein the base station is further configured to:\nestablish a second connection with a second UE using a Long Term Evolution (LTE) RAT, wherein the first DCI is scheduled to not overlap with third DCI transmitted for the second connection.",
            "claim_type": "dependent",
            "dependency": "claim 10",
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. An apparatus, comprising:\na processor configured to cause a base station to:\nestablish a connection as a primary cell with a user equipment device (UE);\nprovide a first indication to the UE to monitor a common search space (CSS) for first downlink control information (DCI) from the primary cell, wherein the first DCI is for scheduling of the primary cell for the UE;\nprovide a second indication to the UE to monitor a UE-specific search space (USS) for second DCI from a secondary cell, wherein the second DCI is for cross-carrier scheduling to the primary cell for the UE, and wherein the second DCI has a 5G NR DCI format of 0_1, 0_2, 1_1 or 1_2, wherein, regardless of a monitoring capability of the UE, all physical downlink control channel (PDCCH) monitoring occasions on the secondary cell for DCIs for cross-carrier scheduling to the primary cell for the UE are constrained to be within an initial three symbols of a slot; and\noperate the connection according to the first DCI and the second DCI.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. The apparatus of claim 12, wherein the connection with the UE utilizes a 5th Generation New Radio (5G NR) radio access technology (RAT), wherein the processor is further configured to cause the base station to:\nestablish a second connection with a second UE using a Long Term Evolution (LTE) RAT, wherein the first DCI is scheduled to not overlap with third DCI transmitted for the second connection.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. The apparatus of claim 13,\nwherein the base station communicates with the UE and the second UE using a 15 kHz subcarrier spacing, and\nwherein the secondary cell communicates with the UE using either the 15 kHz or a 30 kHz subcarrier spacing.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00015",
            "claim_text": "15. The apparatus of claim 12, wherein the base station is further configured to:\nprovide a third indication to the UE to monitor the USS for third DCI from the secondary cell, wherein the third DCI schedules a communication with a second secondary cell.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00016",
            "claim_text": "16. The apparatus of claim 12,\nwherein in operating the connection according to the first DCI and the second DCI, the processor is further configured to cause the base station to:\nreceive one or more uplink communications from the UE according to scheduling information of the first DCI or the second DCI;\ntransmit one or more downlink communications to the UE according to the scheduling information of the first DCI or the second DCI.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00017",
            "claim_text": "17. The apparatus of claim 12,\nwherein the first DCI has:\na 5th Generation New Radio (5G NR) fallback DCI format of 0_0 or 1_0; or\na 5G NR special DCI format of 2_0, 2_1, 2_2, 2_3, 2_4, 2_5 or 2_6.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00018",
            "claim_text": "18. The apparatus of claim 12,\nwherein the first DCI has:\na 5th Generation New Radio (5G NR) fallback DCI format of 0_0 or 1_0.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00019",
            "claim_text": "19. The apparatus of claim 12,\nwherein the first indication and the second indication comprise one or more radio resource control (RRC) configuration messages.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00020",
            "claim_text": "20. The apparatus of claim 12,\nwherein the first DCI and the second DCI each comprise one or more of:\na scheduling indication for an uplink communication with the primary cell;\na scheduling indication for a downlink communication with the primary cell; and\na control message indicating a behavior modification of the UE.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.8,
        "publication_date": "2024-08-13",
        "patent_year": 2024
      },
      {
        "patent_id": "11888610",
        "title": "Method and apparatus for positioning with LTE-NR dynamic spectrum sharing (DSS)",
        "abstract": "A user equipment (UE) is configured to be connected to a 5G New Radio (NR) network that shares one or more frequency bands using dynamic spectrum sharing (DSS) with a Long Term Evolution (LTE) network that is transmitting LTE positioning reference signal (PRS). The UE may receive LTE PRS rate matching information from the NR network, such as the LTE PRS configuration data or an LTE PRS rate matching pattern. The UE may decode and process NR data signals and control signals transmitted by the NR network while LTE PRS is transmitted by rate matching around the LTE PRS in accordance with the LTE PRS rate matching information. The LTE PRS muting pattern may be adjusted based on NR data or control signals, and the UE may receive and process NR data and control signals transmitted while the LTE PRS is muted.",
        "inventors": [
          "Akash Kumar",
          "Amit Jain",
          "Hargovind Prasad BANSAL"
        ],
        "assignees": [
          "QUALCOMM Incorporated"
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. A method for wireless communications performed by a user equipment (UE) connected to a New Radio (NR) network, the method comprising:\nreceiving, from an entity in the NR network, an NR signal comprising Long Term Evolution (LTE) positioning reference signal (PRS) rate matching information for dynamic LTE PRS transmitted by a first base station in an LTE network in one or more frequency bands shared by the NR network using dynamic spectrum sharing (DSS), wherein the LTE PRS rate matching information comprises an LTE PRS rate matching pattern;\nreceiving NR data signals and control signals transmitted by a second base station in the NR network and the dynamic LTE PRS transmitted by the first base station in the LTE network on the one or more frequency bands; and\ndecoding and processing the NR data signals and control signals from the second base station in the NR network by rate matching around the dynamic LTE PRS in accordance with the LTE PRS rate matching information, wherein rate matching around the dynamic LTE PRS in accordance with the LTE PRS rate matching information comprises applying the LTE PRS rate matching pattern to the NR data signals and control signals to receive NR data.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The method of claim 1, wherein the NR data signals and control signals transmitted by the second base station in the NR network comprise at least one of physical downlink shared channel (PDSCH) transmissions, physical downlink common channel (PDCCH) transmissions, Synchronization Signal Block (SSB) transmissions, or a combination thereof.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The method of claim 1, wherein the LTE PRS rate matching information comprises LTE PRS configuration data to enable the UE to perform PRS positioning measurements.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The method of claim 3, wherein the LTE PRS configuration data comprises one or more of carrier frequency, carrier bandwidth, a number of consecutive PRS sub-frames, a PRS periodicity, a PRS configuration index, a muting pattern, or a combination thereof.",
            "claim_type": "dependent",
            "dependency": "claim 3",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The method of claim 1, further comprising:\ntransmitting an indication to the entity in the NR network of a capability of rate matching around the dynamic LTE PRS in DSS, prior to receiving the LTE PRS rate matching information.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. The method of claim 1, further comprising:\nreceiving a muting pattern for the dynamic LTE PRS or a regularly scheduled LTE PRS in the LTE PRS rate matching information, wherein the muting pattern is at least partly based on a Synchronization Signal Block (SSB) periodicity from the NR network; and\nreceiving SSB transmissions from the second base station in the NR network while the dynamic LTE PRS or the regularly scheduled LTE PRS transmitted by the first base station in the LTE network is muted.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The method of claim 6, further comprising:\nmuting the dynamic LTE PRS or the regularly scheduled LTE PRS for at least two symbols in a physical resource block (PRB) transmitted by the first base station in the LTE network to leave at least four consecutive symbols available for SSB transmissions in the PRB transmitted by the second base station in the NR network.",
            "claim_type": "dependent",
            "dependency": "claim 6",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. A user equipment (UE) configured for wireless communications with a New Radio (NR) network, the UE comprising:\na wireless transceiver configured to wirelessly communicate with network entities in a wireless communication system;\nat least one memory; and\nat least one processor coupled to the wireless transceiver and the at least one memory, wherein the at least one processor is configured to:\nreceive, from an entity in the NR network via the wireless transceiver, an NR signal comprising Long Term Evolution (LTE) positioning reference signal (PRS) rate matching information for dynamic LTE PRS transmitted by a first base station in an LTE network in one or more frequency bands shared by the NR network using dynamic spectrum sharing (DSS), wherein the LTE PRS rate matching information comprises an LTE PRS rate matching pattern;\nreceive, via the wireless transceiver, NR data signals and control signals transmitted by a second base station in the NR network and the dynamic LTE PRS transmitted by the first base station in the LTE network on the one or more frequency bands; and\ndecode and process the NR data signals and control signals from the second base station in the NR network, wherein, to decode and process the NR data signals and control signals from the second base station in the NR network, the at least one processor is configured to rate match around the dynamic LTE PRS in accordance with the LTE PRS rate matching information, wherein, to rate match around the dynamic LTE PRS in accordance with the LTE PRS rate matching information, the at least one processor is configured to apply the LTE PRS rate matching pattern to the NR data signals and control signals to receive NR data.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. The UE of claim 8, wherein the NR data signals and control signals transmitted by the second base station in the NR network comprise at least one of physical downlink shared channel (PDSCH) transmissions, physical downlink common channel (PDCCH) transmissions, Synchronization Signal Block (SSB) transmissions, or a combination thereof.",
            "claim_type": "dependent",
            "dependency": "claim 8",
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. The UE of claim 8, wherein the LTE PRS rate matching information comprises LTE PRS configuration data to enable the UE to perform PRS positioning measurements.",
            "claim_type": "dependent",
            "dependency": "claim 8",
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. The UE of claim 10, wherein the LTE PRS configuration data comprises one or more of carrier frequency, carrier bandwidth, a number of consecutive PRS sub-frames, a PRS periodicity, a PRS configuration index, a muting pattern, or a combination thereof.",
            "claim_type": "dependent",
            "dependency": "claim 10",
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. The UE of claim 8, wherein the at least one processor is further configured to:\ntransmit, via the wireless transceiver, an indication to the entity in the NR network of a capability of rate matching around the dynamic LTE PRS in DSS, prior to receiving the LTE PRS rate matching information.",
            "claim_type": "dependent",
            "dependency": "claim 8",
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. The UE of claim 8, wherein the at least one processor is further configured to:\nreceive, via the wireless transceiver, a muting pattern for the dynamic LTE PRS or a regularly scheduled LTE PRS in the LTE PRS rate matching information, wherein the muting pattern is at least partly based on a Synchronization Signal Block (SSB) periodicity from the NR network; and\nreceive, via the wireless transceiver, SSB transmissions from the second base station in the NR network while the dynamic LTE PRS or the regularly scheduled LTE PRS transmitted by the first base station in the LTE network is muted.",
            "claim_type": "dependent",
            "dependency": "claim 8",
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. The UE of claim 13, wherein the at least one processor is further configured to:\nmute the dynamic LTE PRS or the regularly scheduled LTE PRS for at least two symbols in a physical resource block (PRB) transmitted by the first base station in the LTE network to leave at least four consecutive symbols available for SSB transmissions in the PRB transmitted by the second base station in the NR network.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00015",
            "claim_text": "15. A user equipment (UE) configured for wireless communications with a New Radio (NR) network, the UE comprising:\nmeans for receiving, from an entity in the NR network, an NR signal comprising Long Term Evolution (LTE) positioning reference signal (PRS) rate matching information for dynamic LTE PRS transmitted by a first base station in an LTE network in one or more frequency bands shared by the NR network using dynamic spectrum sharing (DSS), wherein the LTE PRS rate matching information comprises an LTE PRS rate matching pattern;\nmeans for receiving NR data signals and control signals transmitted by a second base station in the NR network and the dynamic LTE PRS transmitted by the base station in the LTE network on the one or more frequency bands; and\nmeans for decoding and processing the NR data signals and control signals from the second base station in the NR network configured to rate match around the dynamic LTE PRS in accordance with the LTE PRS rate matching information, wherein the means for rate matching around the dynamic LTE PRS in accordance with the LTE PRS rate matching information is configured to apply the LTE PRS rate matching pattern to the NR data signals and control signals to receive NR data.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00016",
            "claim_text": "16. The UE of claim 15, wherein the NR data signals and control signals transmitted by the second base station in the NR network comprise at least one of physical downlink shared channel (PDSCH) transmissions, physical downlink common channel (PDCCH) transmissions, Synchronization Signal Block (SSB) transmissions, or a combination thereof.",
            "claim_type": "dependent",
            "dependency": "claim 15",
            "is_exemplary": true
          },
          {
            "claim_number": "00017",
            "claim_text": "17. The UE of claim 15, wherein the LTE PRS rate matching information comprises LTE PRS configuration data to enable the UE to perform PRS positioning measurements.",
            "claim_type": "dependent",
            "dependency": "claim 15",
            "is_exemplary": true
          },
          {
            "claim_number": "00018",
            "claim_text": "18. The UE of claim 17, wherein the LTE PRS configuration data comprises one or more of carrier frequency, carrier bandwidth, a number of consecutive PRS sub-frames, a PRS periodicity, a PRS configuration index, a muting pattern, or a combination thereof.",
            "claim_type": "dependent",
            "dependency": "claim 17",
            "is_exemplary": true
          },
          {
            "claim_number": "00019",
            "claim_text": "19. The UE of claim 15, further comprising:\nmeans for transmitting an indication to the entity in the NR network of a capability of rate matching around the dynamic LTE PRS in DSS, prior to receiving the LTE PRS rate matching information.",
            "claim_type": "dependent",
            "dependency": "claim 15",
            "is_exemplary": true
          },
          {
            "claim_number": "00020",
            "claim_text": "20. The UE of claim 15, further comprising:\nmeans for receiving a muting pattern for the dynamic LTE PRS or a regularly scheduled LTE PRS in the LTE PRS rate matching information, wherein the muting pattern is at least partly based on a Synchronization Signal Block (SSB) periodicity from the NR network; and\nmeans for receiving SSB transmissions from the second base station in the NR network while the dynamic LTE PRS or the regularly scheduled LTE PRS transmitted by the first base station in the LTE network is muted.",
            "claim_type": "dependent",
            "dependency": "claim 15",
            "is_exemplary": true
          },
          {
            "claim_number": "00021",
            "claim_text": "21. The UE of claim 20, further comprising:\nmeans for muting the dynamic LTE PRS or the regularly scheduled LTE PRS for at least two symbols in a physical resource block (PRB) transmitted by the first base station in the LTE network to leave at least four consecutive symbols available for SSB transmissions in the PRB transmitted by the second base station in the NR network.",
            "claim_type": "dependent",
            "dependency": "claim 20",
            "is_exemplary": true
          },
          {
            "claim_number": "00022",
            "claim_text": "22. A non-transitory storage medium including program code stored thereon, the program code is operable to configure at least one processor in a user equipment (UE) for wireless communications with a New Radio (NR) network, the UE comprising:\nprogram code to receive, from an entity in the NR network, an NR signal comprising Long Term Evolution (LTE) positioning reference signal (PRS) rate matching information for dynamic LTE PRS transmitted by a first base station in an LTE network in one or more frequency bands shared by the NR network using dynamic spectrum sharing (DSS), wherein the LTE PRS rate matching information comprises an LTE PRS rate matching pattern;\nprogram code to receive NR data signals and control signals transmitted by a second base station in the NR network and the dynamic LTE PRS transmitted by the first base station in the LTE network on the one or more frequency bands; and\nprogram code to decode and process the NR data signals and control signals from the second base station in the NR network, wherein the program code to decode and process the NR data signals and control signals from the second base station in the NR network is configured to rate match around the dynamic LTE PRS in accordance with the LTE PRS rate matching information, wherein the program code to rate match around the dynamic LTE PRS in accordance with the LTE PRS rate matching information is configured to apply the LTE PRS rate matching pattern to the NR data signals and control signals to receive NR data.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00023",
            "claim_text": "23. The non-transitory storage medium of claim 22, wherein the NR data signals and control signals transmitted by the second base station in the NR network comprise at least one of physical downlink shared channel (PDSCH) transmissions, physical downlink common channel (PDCCH) transmissions, Synchronization Signal Block (SSB) transmissions, or a combination thereof.",
            "claim_type": "dependent",
            "dependency": "claim 22",
            "is_exemplary": true
          },
          {
            "claim_number": "00024",
            "claim_text": "24. The non-transitory storage medium of claim 22, wherein the LTE PRS rate matching information comprises LTE PRS configuration data to enable the UE to perform PRS positioning measurements.",
            "claim_type": "dependent",
            "dependency": "claim 22",
            "is_exemplary": true
          },
          {
            "claim_number": "00025",
            "claim_text": "25. The non-transitory storage medium of claim 22, wherein the UE comprises program code to:\ntransmit an indication to the entity in the NR network of a capability of rate matching around the dynamic LTE PRS in DSS, prior to receiving the LTE PRS rate matching information.",
            "claim_type": "dependent",
            "dependency": "claim 22",
            "is_exemplary": true
          },
          {
            "claim_number": "00026",
            "claim_text": "26. The non-transitory storage medium of claim 22, wherein the UE comprises program code to:\nreceive a muting pattern for the dynamic LTE PRS or a regularly scheduled LTE PRS in the LTE PRS rate matching information, wherein the muting pattern is at least partly based on a Synchronization Signal Block (SSB) periodicity from the NR network; and\nreceive SSB transmissions from the second base station in the NR network while the dynamic LTE PRS or the regularly scheduled LTE PRS transmitted by the first base station in the LTE network is muted.",
            "claim_type": "dependent",
            "dependency": "claim 22",
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.8,
        "publication_date": "2024-01-30",
        "patent_year": 2024
      },
      {
        "patent_id": "11832111",
        "title": "Dynamic spectrum sharing between 4G and 5G wireless networks",
        "abstract": "Aspects of the present disclosure provide various devices, methods, and systems for dynamic spectrum sharing of a spectrum between different radio access technologies and multiple frequency division duplexing modes. Dynamic spectrum sharing (DSS) is a technology that allows wireless network operators to share a spectrum between different radio access technologies (RATs). DSS allows an operator to dynamically allocate some existing 4G spectrum to 5G use to deliver 5G services using a shared spectrum.",
        "inventors": [
          "Wanshi Chen",
          "Huilin XU",
          "Peter Pui Lok Ang",
          "Jing Lei",
          "Runxin WANG"
        ],
        "assignees": [
          "QUALCOMM Incorporated"
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. A method for spectrum sharing in wireless communication at a first scheduling entity, the method comprising:\nexchanging scheduling information with a second scheduling entity, the scheduling information identifying a resource usage of a first radio access technology (RAT) in a resource pool for wireless communication, the second scheduling entity associated with the first RAT;\ndetermining a scheduling constraint imposed by the resource usage of the first RAT for sharing the resource pool for wireless communication using a second RAT, the first scheduling entity associated with the second RAT;\nallocating, based on the scheduling constraint, a resource of the resource pool for wireless communication using the second RAT, the resource comprising a plurality of time-frequency-space resources that are grouped in one or more mini-slots based on a numerology of the second RAT, each mini-slot spanning a time interval corresponding to one or more time domain symbols based on a numerology of the first RAT or the second RAT; and\ncommunicating with a user equipment (UE) using the resource allocated to the second RAT.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The method of claim 1, wherein the communicating with the UE comprises communicating with the UE using half-duplex frequency division duplex (HD-FDD) with the resource allocated to the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The method of claim 2,\nwherein identifying the resource usage comprises identifying a downlink resource usage dedicated to the first RAT as the scheduling constraint for using the second RAT, and the downlink resource usage comprises a resource of the resource pool used for at least one of:\na physical HARQ indicator channel (PHICH);\na physical control format indicator channel (PCFICH);\na physical downlink shared channel (PDSCH);\na channel state information reference signal (CSI-RS); or\na positioning reference signal (PRS).",
            "claim_type": "dependent",
            "dependency": "claim 2",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The method of claim 2,\nwherein identifying the resource usage comprises identifying an uplink resource usage dedicated to the first RAT as the scheduling constraint for using the second RAT, and the uplink resource usage comprises a resource of the resource pool used for at least one of:\na sounding reference signal (SRS);\na physical uplink shared channel (PUSCH); or\na physical uplink control channel (PUCCH).",
            "claim_type": "dependent",
            "dependency": "claim 2",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The method of claim 1, wherein the scheduling constraint comprises a predetermined frequency offset or slot offset from an LTE synchronization signal.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. The method of claim 1, wherein communicating with the UE comprises at least one of:\nrepeating a signal transmission of the second RAT using the one or more mini-slots; or\ntransmitting a signal of the second RAT using frequency hopping in the one or more mini-slots.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The method of claim 1, wherein communicating with the UE comprises:\ntransmitting a synchronization signal block (SSB) of the second RAT that is not punctured by a reference signal of the first RAT, a numerology of the first RAT being different from a numerology of the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The method of claim 1, wherein communicating with the UE comprises:\ntransmitting a synchronization signal block (SSB) of the second RAT that is punctured by or rate-matched around a cell-specific reference signal, a control channel, or a semi-persistently scheduled downlink data channel of the first RAT.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. The method of claim 1, wherein communicating with the UE comprises:\ntransmitting a synchronization signal block (SSB) and a control resource set (CORESET) of the second RAT using time-division multiplexing, frequency-division multiplexing, or space-division-multiplexing, depending on at least one of a bandwidth constraint, a power constraint, or capabilities of the UE.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. The method of claim 9, wherein allocating the resource comprises at least one of:\nallocating the resource to the SSB based on a predetermined frequency offset from a synchronization signal of the first RAT, wherein a numerology of the frequency offset is based on a numerology of the first RAT or a numerology of the second RAT; or\nallocating the resource to the SSB based on a predetermined slot offset from the synchronization signal of the first RAT, wherein a numerology of the slot offset is based on a numerology of the first RAT or a numerology of the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 9",
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. The method of claim 9, wherein transmitting the SSB comprises:\ntransmitting an SSB burst comprising a plurality of SSBs that are time-multiplexed, frequency-multiplexed, or space-multiplexed with resources of the resource pool that are dedicated to the first RAT.",
            "claim_type": "dependent",
            "dependency": "claim 9",
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. The method of claim 1, wherein allocating the resource comprises:\nallocating resources of the resource pool to a random access procedure (RACH) of the second RAT that is time-multiplexed or frequency-multiplexed with one or more RACH occasions of the first RAT.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. The method of claim 1, further comprising:\ndetermining a cell-specific slot format of the second RAT based on the scheduling constraint, wherein the cell-specific slot format comprises information for configuring at least one of a downlink mini-slot, an uplink mini-slot, a guard period mini-slot, and a special mini-slot; and\ntransmitting a radio resource control (RRC) message including the cell-specific slot format to a user equipment using the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. A first scheduling entity for wireless communication, comprising:\na communication interface configured for wireless communication using spectrum sharing between a first radio access technology (RAT) and a second RAT;\na memory; and\na processor coupled with the communication interface and the memory,\nthe processor and the memory being configured to:\nexchange scheduling information with a second scheduling entity, the scheduling information identifying a resource usage of the first RAT in a resource pool for wireless communication, the second scheduling entity associated with the first RAT;\ndetermine a scheduling constraint imposed by the resource usage of the first RAT for sharing the resource pool for wireless communication using the second RAT, the first scheduling entity associated with the second RAT;\nallocate, based on the scheduling constraint, a resource of the resource pool for wireless communication using the second RAT, the resource comprising a plurality of time-frequency-space resources that are grouped in one or more mini-slots based on a numerology of the second RAT, each mini-slot spanning a time interval corresponding to one or more time domain symbols based on a numerology of the first RAT or the second RAT; and\ncommunicate with a user equipment (UE) using the resource allocated to the second RAT.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00015",
            "claim_text": "15. The apparatus of claim 14, wherein the processor and the memory are configured to communicate with the UE using half-duplex frequency division duplex (HD-FDD) with the resource allocated to the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00016",
            "claim_text": "16. The apparatus of claim 15,\nwherein the resource usage comprises a downlink resource usage dedicated to the first RAT as the scheduling constraint for using the second RAT, and the downlink resource usage comprises a resource of the resource pool used for at least one of:\na physical HARQ indicator channel (PHICH);\na physical control format indicator channel (PCFICH);\na physical downlink shared channel (PDSCH);\na channel state information reference signal (CSI-RS); or\na positioning reference signal (PRS).",
            "claim_type": "dependent",
            "dependency": "claim 15",
            "is_exemplary": true
          },
          {
            "claim_number": "00017",
            "claim_text": "17. The apparatus of claim 15,\nwherein the resource usage comprises an uplink resource usage dedicated to the first RAT as the scheduling constraint for using the second RAT, and the uplink resource usage comprises a resource of the resource pool used for at least one of:\na sounding reference signal (SRS);\na physical uplink shared channel (PUSCH); or\na physical uplink control channel (PUCCH).",
            "claim_type": "dependent",
            "dependency": "claim 15",
            "is_exemplary": true
          },
          {
            "claim_number": "00018",
            "claim_text": "18. The apparatus of claim 14, wherein the scheduling constraint comprises a predetermined frequency offset or slot offset from an LTE synchronization signal.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00019",
            "claim_text": "19. The apparatus of claim 14, wherein, for communicating with the UE, the processor and the memory are further configured to at least one of:\nrepeat a signal transmission of the second RAT using the one or more mini-slots; or\ntransmit a signal of the second RAT using frequency hopping using the one or more mini-slots.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00020",
            "claim_text": "20. The apparatus of claim 14, wherein, for communicating with the UE, the processor and the memory are further configured to:\ntransmit a synchronization signal block (SSB) of the second RAT that is not punctured by a reference signal of the first RAT, a numerology of the first RAT being different from a numerology of the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00021",
            "claim_text": "21. The apparatus of claim 14, wherein, for communicating with the UE, the processor and the memory are further configured to:\ntransmit a synchronization signal block (SSB) of the second RAT that is punctured by or rate matched around a cell-specific reference signal, a control channel, or a semi-persistently scheduled downlink data channel of the first RAT.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00022",
            "claim_text": "22. The apparatus of claim 14, wherein, for communicating with the UE, the processor and the memory are further configured to:\ntransmit a synchronization signal block (SSB) and a control resource set (CORESET) of the second RAT using time-division multiplexing, frequency-division multiplexing, or space-division-multiplexing, depending on at least one of a bandwidth constraint, a power constraint, or capabilities of the UE.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00023",
            "claim_text": "23. The apparatus of claim 22, wherein, for allocating the resource, the processor and the memory are further configured to at least one of:\nallocate the resource to the SSB based on a predetermined frequency offset from a synchronization signal of the first RAT, wherein a numerology of the frequency offset is based on a numerology of the first RAT or a numerology of the second RAT; or\nallocate the resource to the SSB based on a predetermined slot offset from the synchronization signal of the first RAT, wherein a numerology of the slot offset is based on a numerology of the first RAT or a numerology of the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 22",
            "is_exemplary": true
          },
          {
            "claim_number": "00024",
            "claim_text": "24. The apparatus of claim 22, wherein, for transmitting the SSB, the processor and the memory are further configured to:\ntransmit an SSB burst comprising a plurality of SSBs that are time-multiplexed, frequency-multiplexed, or space-multiplexed with resources of the resource pool that are dedicated to the first RAT.",
            "claim_type": "dependent",
            "dependency": "claim 22",
            "is_exemplary": true
          },
          {
            "claim_number": "00025",
            "claim_text": "25. The apparatus of claim 14, wherein, for allocating the resource, the processor and the memory are further configured to:\nallocate resources of the resource pool to a random access procedure (RACH) of the second RAT that is time-multiplexed or frequency-multiplexed with one or more RACH occasions of the first RAT.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00026",
            "claim_text": "26. The apparatus of claim 14, wherein the processor and the memory are further configured to:\ndetermine a cell-specific slot format of the second RAT based on the scheduling constraint, wherein the cell-specific slot format comprises information for configuring at least one of a downlink mini-slot, an uplink mini-slot, a guard period mini-slot, and a special mini-slot; and\ntransmit a radio resource control (RRC) message including the cell-specific slot format to a user equipment using the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00027",
            "claim_text": "27. A first scheduling entity for wireless communication using spectrum sharing, comprising:\nmeans for exchanging scheduling information with a second scheduling entity, the scheduling information identifying a resource usage of a first radio access technology (RAT) in a resource pool for wireless communication, the second scheduling entity associated with the first RAT;\nmeans for determining a scheduling constraint imposed by the resource usage of the first RAT for sharing the resource pool for wireless communication using a second RAT, the first scheduling entity associated with the second RAT;\nmeans for allocating, based on the scheduling constraint, a resource of the resource pool for wireless communication using the second RAT, the resource comprising a plurality of time-frequency-space resources that are grouped in one or more mini-slots based on a numerology of the second RAT, each mini-slot spanning a time interval corresponding to one or more time domain symbols based on a numerology of the first RAT or the second RAT; and\nmeans for communicating with a user equipment (UE) using the resource allocated to the second RAT.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00028",
            "claim_text": "28. A non-transitory computer-readable medium storing computer-executable code at a first scheduling entity for wireless communication using dynamic spectrum sharing, comprising code for causing a processor to:\nexchange scheduling information with a second scheduling entity, the scheduling information identifying a resource usage of a first radio access technology (RAT) in a resource pool for wireless communication, the second scheduling entity associated with the first RAT;\ndetermine a scheduling constraint imposed by the resource usage of the first RAT for sharing the resource pool for wireless communication using a second RAT, the first scheduling entity associated with the second RAT;\nallocate, based on the scheduling constraint, a resource of the resource pool for wireless communication using the second RAT, the resource comprising a plurality of time-frequency-space resources that are grouped in one or more mini-slots based on a numerology of the second RAT, each mini-slot spanning a time interval corresponding to one or more time domain symbols based on a numerology of the first RAT or the second RAT; and\ncommunicate with a user equipment (UE) using the resource allocated to the second RAT.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.8,
        "publication_date": "2023-11-28",
        "patent_year": 2023
      },
      {
        "patent_id": "11044693",
        "title": "Efficient positioning enhancement for dynamic spectrum sharing",
        "abstract": "Techniques are provided for transmitting Positioning Reference Signals (PRSs) in cells supporting two different Radio Access Technologies (RATs), where the two RATs (e.g. 4G LTE and 5G NR) employ dynamic spectrum sharing. To avoid interference between the PRSs and between the two RATs, the PRSs may be time aligned to the same set of PRS positioning occasions, and may be assigned orthogonal characteristics such as different muting patterns, orthogonal code sequences, different frequency shifts or different frequency hopping. UEs supporting both RATs may be enabled to measure PRSs for both RATs. UEs supporting only one RAT (e.g. 4G LTE) may be enabled to measure PRSs for just this RAT. A location server such as an LMF, E-SMLC or SLP may provide assistance data to UEs, and request measurements from UEs, for PRSs in one or both RATs.",
        "inventors": [
          "Stephen William Edge",
          "Bapineedu Chowdary Gummadi",
          "Hem Agnihotri"
        ],
        "assignees": [
          "QUALCOMM Incorporated"
        ],
        "claims": [],
        "relevance_score": 0.8,
        "publication_date": "2021-06-22",
        "patent_year": 2021
      },
      {
        "patent_id": "10849180",
        "title": "Dynamic spectrum sharing in 4G and 5G",
        "abstract": "Techniques for dynamically allocating frequency resources in accordance with wireless access technologies are discussed herein. For example, a base station can determine whether user equipment (UE) requesting communications at the base station are configured to operate in accordance with 4th Generation (5G) radio access technologies and/or in accordance with 5th Generation (5G) radio access technologies. Based on the number of 5G UEs and 4G UEs, a first portion of a frequency resource can be allocated to 5G and a second portion of the frequency resource can be allocated to 4G. In some examples, a first allocation strategy for a first frequency resource (e.g., Band 71) can be used to generate a second allocation strategy for a partially overlapping second frequency resource (e.g., Band 41).",
        "inventors": [
          "Yasmin Karimli",
          "Gunjan Nimbavikar"
        ],
        "assignees": [
          "T-Mobile USA, Inc."
        ],
        "claims": [],
        "relevance_score": 0.8,
        "publication_date": "2020-11-24",
        "patent_year": 2020
      },
      {
        "patent_id": "11716124",
        "title": "Dynamic spectrum sharing with spatial division multiplexing",
        "abstract": "Methods, systems, and devices for wireless communications are described. A base station to communicate with a set of user equipments (UEs) in a spatial division multiplexing (SDM) configuration for dynamic spectrum sharing (DSS) communications. One or more first UEs of the set of UEs may communicate via a first radio access technology (RAT), and one or more second UEs may communicate via a second RAT in a multiple-user multiple-input multiple output (MU-MIMO) configuration. The base station may indicate the SDM configuration to one or more of the set of UEs. In some examples, the base station may transmit an indication to the set of UEs which may indicate a set of resources to be used for DSS communications. In some examples, the SDM configuration may specify one or more reference signal patterns for communicating in the set of resources.",
        "inventors": [
          "Tao Luo",
          "Wooseok Nam",
          "Kausik Ray Chaudhuri"
        ],
        "assignees": [
          "QUALCOMM Incorporated"
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. A method for wireless communications at a user equipment (UE), comprising:\nreceiving, from a network device, an indication of a set of resources to be used for dynamic spectrum sharing communications with the network device;\ndetermining, based at least in part on the indication, a spatial division multiplexing configuration comprising interference measurement resources for the set of resources, rate matching resources for the set of resources, or both;\nreceiving a notification that a first communication between the UE and the network device applies the spatial division multiplexing configuration; and\nperforming, based at least in part on the notification, the first communication on the set of resources via a first spatial layer associated with the first radio access technology in accordance with the spatial division multiplexing configuration, the first communication being multiplexed on the set of resources with a second communication between a second UE and the network device via a second radio access technology using a second spatial layer associated with the second radio access technology.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The method of claim 1, further comprising:\nreceiving, via explicit signaling, the notification that the first communication applies the spatial division multiplexing configuration.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The method of claim 2, wherein the notification indicates that the first communication with the UE via the first radio access technology is multiplexed with the second communication with the second UE via the second radio access technology in accordance with the spatial division multiplexing configuration.",
            "claim_type": "dependent",
            "dependency": "claim 2",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The method of claim 2, wherein the notification includes a location, a scrambling sequence, a transmission power, or any combination thereof, for one or more reference signals configured for the transmission in the set of resources.",
            "claim_type": "dependent",
            "dependency": "claim 2",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The method of claim 1, further comprising:\nreceiving, via implicit signaling, the notification that the first communication applies the spatial division multiplexing configuration.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. The method of claim 1, further comprising:\ndetermining one or more reference signal patterns associated with the set of resources, wherein the one or more reference signal patterns comprise the interference measurement resources, the rate matching resources, or both.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The method of claim 6, wherein the one or more reference signal patterns further comprise a set of antenna ports associated with one or more demodulation reference signals shared between the first communication via the first radio access technology and the second communication via the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 6",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The method of claim 6, wherein the indication comprises a configuration associated with the one or more reference signal patterns.",
            "claim_type": "dependent",
            "dependency": "claim 6",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. The method of claim 1, wherein the interference measurement resources are associated with the first communication via the first radio access technology and the second communication via the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. The method of claim 1, wherein the interference measurement resources include a New Radio (NR) interference measurement resource, or a resource for measuring interference from a Long Term Evolution (LTE) cell-specific reference signal, an LTE non-zero power channel state information reference signal, an LTE sounding reference signal, or any combination thereof.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. The method of claim 1, wherein the rate matching resources are associated with a Long Term Evolution (LTE) demodulation reference signal, an LTE cell-specific reference signal, a zero power channel state information reference signal (CSI-RS) associated with LTE CSI-RS resources, or any combination thereof.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. The method of claim 1, further comprising:\nidentifying, in the indication, a configuration associated with a rate matching pattern for one or more reference signals configured for transmission in the set of resources, wherein the rate matching pattern is based at least in part on a first numerology associated with the first radio access technology and a second numerology associated with the second radio access technology, and wherein performing the first communication with the network device is further in accordance with the rate matching pattern.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. A method for wireless communications at a network device, comprising:\ndetermining a spatial division multiplexing configuration for dynamic spectrum sharing communications with one or more first user equipments (UEs) communicating via a first radio access technology and with one or more second UEs communicating via a second radio access technology;\ntransmitting, to at least the one or more first UEs, an indication of a set of resources associated with a spatial division multiplexing configuration to be used for the dynamic spectrum sharing communications, wherein the spatial division multiplexing configuration comprises interference measurement resources for the set of resources, rate matching resources for the set of resources, or both;\ntransmitting, to at least the one or more first UEs, a notification that the first communication applies the spatial division multiplexing configuration; and\nperforming, based at least in part on the notification, the first communication on the set of resources via a first spatial layer associated with the first radio access technology in accordance with the spatial division multiplexing configuration and a second communication between the one or more second UEs and the network device via the second radio access technology on a second spatial layer associated with the second radio access technology, the first communication being multiplexed on the set of resources with the second communication.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. The method of claim 13, further comprising:\ntransmitting, via explicit signaling, the notification that the first communication applies the spatial division multiplexing configuration.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00015",
            "claim_text": "15. The method of claim 14, wherein the notification indicates that the first communication with the one or more first UEs via the first radio access technology is multiplexed with the second communication with the one or more second UEs via the second radio access technology in accordance with the spatial division multiplexing configuration.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00016",
            "claim_text": "16. The method of claim 14, wherein the notification includes a location, a scrambling sequence, a transmission power, or any combination thereof, for one or more reference signals configured for the transmission in the set of resources.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00017",
            "claim_text": "17. The method of claim 13, further comprising:\ntransmitting, via implicit signaling, the notification that the first communication applies the spatial division multiplexing configuration.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00018",
            "claim_text": "18. The method of claim 13, further comprising:\ndetermining one or more reference signal patterns associated with the set of resources, wherein the one or more reference signal patterns comprise the interference measurement resources, the rate matching resources, or both.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00019",
            "claim_text": "19. The method of claim 18, wherein the one or more reference signal patterns further comprise a set of antenna ports associated with one or more demodulation reference signals shared between the first communication via the first radio access technology and the second communication via the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 18",
            "is_exemplary": true
          },
          {
            "claim_number": "00020",
            "claim_text": "20. The method of claim 13, wherein the interference measurement resources are associated with the first communication via the first radio access technology and the second communication via the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00021",
            "claim_text": "21. The method of claim 13, wherein the interference measurement resources include a New Radio (NR) interference measurement resource, or a resource for measuring interference from a Long Term Evolution (LTE) cell-specific reference signal, an LTE non-zero power channel state information reference signal, an LTE sounding reference signal, or any combination thereof.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00022",
            "claim_text": "22. The method of claim 13, wherein the rate matching resources are associated with a Long Term Evolution (LTE) demodulation reference signal, an LTE cell-specific reference signal, a zero power channel state information reference signal (CSI-RS) associated with LTE CSI-RS resources, or any combination thereof.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00023",
            "claim_text": "23. The method of claim 13, further comprising:\ndetermining a first numerology associated with the first radio access technology and a second numerology associated with the second radio access technology; and\ndetermining a rate matching pattern for one or more reference signals configured for transmission in the set of resources based at least in part on the first numerology and the second numerology, wherein the indication comprises a configuration associated with the rate matching pattern.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00024",
            "claim_text": "24. The method of claim 23, wherein the rate matching pattern comprises a New Radio (NR) demodulation reference signal rate matching pattern associated with interference between the first communication via the first radio access technology and the second communication via the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 23",
            "is_exemplary": true
          },
          {
            "claim_number": "00025",
            "claim_text": "25. The method of claim 13, further comprising:\npuncturing one or more resource elements of the set of resources based at least in part on interference between the first communication via the first radio access technology and the second communication via the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00026",
            "claim_text": "26. An apparatus for wireless communications, comprising:\na processor;\nmemory coupled with the processor; and\ninstructions stored in the memory and executable by the processor to cause the apparatus to:\nreceive, from a network device, an indication of a set of resources to be used for dynamic spectrum sharing communications with the network device;\ndetermine, based at least in part on the indication, a spatial division multiplexing configuration comprising interference measurement resources for the set of resources, rate matching resources for the set of resources, or both;\nreceive a notification that a first communication between the UE and the network device applies the spatial division multiplexing configuration; and\nperform, based at least in part on the notification, a first communication on the set of resources via a first spatial layer associated with the first radio access technology in accordance with the spatial division multiplexing configuration, the first communication being multiplexed on the set of resources with a second communication between a second apparatus and the network device via a second radio access technology using a second spatial layer associated with the second radio access technology.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00027",
            "claim_text": "27. An apparatus for wireless communications, comprising:\na processor;\nmemory coupled with the processor; and\ninstructions stored in the memory and executable by the processor to cause the apparatus to:\ndetermine a spatial division multiplexing configuration for dynamic spectrum sharing communications with one or more first user equipments (UEs) communicating via a first radio access technology and with one or more second UEs communicating via a second radio access technology;\ntransmit, to at least the one or more first UEs, an indication of a set of resources associated with a spatial division multiplexing configuration to be used for the dynamic spectrum sharing communications, wherein the spatial division multiplexing configuration comprises interference measurement resources for the set of resources, rate matching resources for the set of resources, or both;\ntransmit, to at least the one or more first UEs, a notification that a first communication applies the spatial division multiplexing configuration; and\nperform, based at least in part on the notification, the first communication on the set of resources via a first spatial layer associated with the first radio access technology in accordance with the spatial division multiplexing configuration and a second communication between the one or more second UEs and the apparatus via the second radio access technology on a second spatial layer associated with the second radio access technology, the first communication being multiplexed on the set of resources with the second communication.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.8,
        "publication_date": "2023-08-01",
        "patent_year": 2023
      },
      {
        "patent_id": "11943204",
        "title": "Method and systems for dynamic spectrum sharing with a spectrum management firewall",
        "abstract": "Methods and systems for dynamically sharing spectrum between a commercial network and a protected system network. A spectrum management firewall (SMF) computing device may receive information from the commercial network, receive characteristic information identifying one or more characteristics of a resource or entity in the protected system network, determine a class of system (COS) and an area of operation (AOO) for the resource or entity based on the characteristic information received from the protected system network, and determine potential interference based on the information received from the commercial network and the characteristic information received from the protected system network. The SMF may determine which frequencies may be suppressed on which cells in the commercial network based on the determined potential interference, generate a suppression message that identifies the determined frequencies per cell, and send the generated suppression message to a component in the commercial network.",
        "inventors": [
          "John Arpee"
        ],
        "assignees": [
          "RIVADA NETWORKS, LLC"
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. A method of dynamically sharing spectrum between a commercial network and a protected system network, comprising:\nreceiving, by a processor a spectrum management firewall (SMF) computing device, information from the commercial network;\nreceiving, by the processor, characteristic information identifying one or more characteristics of a resource or entity in the protected system network;\ndetermining, by the processor, a class of system (COS) and an area of operation (AOO) for the resource or entity based on the characteristic information received from the protected system network;\ndetermining, by the processor, potential interference based on the information received from the commercial network and the characteristic information received from the protected system network;\ndetermining, by the processor, which frequencies may be suppressed on which cells in the commercial network based on the determined potential interference;\ngenerating, by the processor, a suppression message that identifies the determined frequencies per cell; and\nsending, by the processor, the generated suppression message to a component in the commercial network to cause that component to suppress the identified frequencies in the identified cells.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The method of claim 1, wherein generating the suppression message that identifies the determined frequencies per cell that mask the activities, operations, communications, locations, features, properties, or characteristics of the resource or entity in the protected system network.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The method of claim 2, wherein generating the obfuscated message comprises adding additional frequencies that mask the activities, operations, communications, locations, features, properties, or characteristics of the resource or entity in the protected system network to the suppression message.",
            "claim_type": "dependent",
            "dependency": "claim 2",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The method of claim 1, further comprising:\nusing a generative adversarial network (GAN) that includes a deep neural network and a generator to produce fake data;\ninserting the generated fake data into the suppression message prior to sending the generated suppression message to the component in the commercial network; or\nusing the generated fake data to generate additional suppression messages that are intentionally misleading and sending the additional suppression messages to the component in the commercial network.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The method of claim 1, further comprising using a generative adversarial network (GAN) that includes a deep neural network and a generator to create credible fake activities of the resource or entities in the protected systems network including movement patterns, emissions spectrums, frequency blanking patterns and realistic activity schedules.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. The method of claim 1, wherein:\nreceiving characteristic information from the protected system network comprises:\nreceiving detected activity information, signal level information and frequency information collected by sensors within a vicinity of the resource or entity in the protected systems network in response to detecting that the resource or entity recently became active; and\ndetermining the COS and the PAOO based on the characteristic information received from the protected system network comprises:\ndetermining the COS and an approximate area associated with the recently active resource or entity based on the received activity information, signal level information, and frequency information.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The method of claim 1, wherein receiving characteristic information from the protected system network comprises:\nreceiving a spectrum reservation message from the protected system network indicating that the resource or entity is anticipated to become or is becoming active in an area; and\nwherein determining the COS and the AOO based on the characteristic information received from the protected system network comprises:\ndetermining the COS and an approximate area of the resource or entity that is anticipated to become or is becoming active based on the received spectrum reservation message.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The method of claim 1, wherein sending the generated message to the component in the commercial network to cause that component to suppress the identified frequencies in the identified cells comprises sending the generated message to the component in the commercial network to cause that component to:\nstop all transmissions on the identified frequencies;\nreduce power on the identified frequencies;\nreorient antennas to direct power away from the resource or entity in the protected systems network; or\ndown-tilt or direct the antennas into focused areas that only allow the power to be transmitted in the immediate vicinity of the identified cells.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. The method of claim 1, further comprising:\nreceiving, by the processor, a notification message from the protected system network indicating that a detected activity identified in the received characteristic information has ceased; and\ncausing, by the processor, the component in the commercial network to cease suppressing the identified frequencies in the identified cells and restore power levels in response to the processor receiving the notification message from the protected system network indicating that the detected activity identified in the received characteristic information has ceased.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. The method of claim 9, wherein causing the component in the commercial network to cease suppressing the identified frequencies in the identified cells and restore power levels comprises sending a communication message to the component that causes the component to reorient and uptilt antennas back to configurations that are optimized for full utilization of the identified frequencies on the commercial network.",
            "claim_type": "dependent",
            "dependency": "claim 9",
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. The method of claim 1, wherein determining potential interference based on the information received from the commercial network and the characteristic information received from the protected system network comprises:\ndetermining the cell sites and frequencies that would result in interference between the resource or entity within the protected systems network and specific cells and attached mobiles in the commercial network.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. A server computing device implementing a spectrum management firewall (SMF), comprising:\na processor configured with processor-executable instructions to perform operations comprising:\nreceiving information from a commercial network;\n\nreceiving characteristic information identifying one or more characteristics of a resource or entity in a protected system network;\ndetermining a class of system (COS) and a planned area of operation (AOO) for the resource or entity based on the characteristic information received from the protected system network;\ndetermining potential interference based on the information received from the commercial network and the characteristic information received from the protected system network;\ndetermining which frequencies may be suppressed on which cells in the commercial network based on the determined potential interference;\ngenerating a suppression message that identifies the determined frequencies per cell; and\nsending the generated suppression message to a component in the commercial network to cause that component to suppress the identified frequencies in the identified cells.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. The server computing device of claim 12, wherein the processor is configured with processor executable instructions to perform operations such that generating the suppression message that identifies the determined frequencies per cell comprises generating an obfuscation message that mask the activities, operations, communications, locations, features, properties, or characteristics of the resource or entity in the protected system network.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. The server computing device of claim 13, wherein the processor is configured with processor executable instructions to perform operations such that generating the obfuscation message comprises adding additional frequencies that mask the activities, operations, communications, locations, features, properties, or characteristics of the resource or entity in the protected system network to the suppression message.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00015",
            "claim_text": "15. The server computing device of claim 12, wherein the processor is configured with processor executable instructions to perform operations further comprising:\nusing a generative adversarial network (GAN) that includes a deep neural network and a generator to produce fake data;\ninserting the generated fake data into the suppression message prior to sending the generated suppression message to the component in the commercial network; or\nusing the generated fake data to generate additional suppression messages that are intentionally misleading and sending the additional suppression messages to the component in the commercial network.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00016",
            "claim_text": "16. The server computing device of claim 12, wherein the processor is configured with processor executable instructions to perform operations further comprising using a generative adversarial network (GAN) that includes a deep neural network and a generator to detect and differentiate between real and fake activities of the resource or entities in the protected systems network.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00017",
            "claim_text": "17. The server computing device of claim 12, wherein the processor is configured with processor executable instructions to perform operations such that:\nreceiving characteristic information from the protected system network comprises:\nreceiving detected activity information, signal level information and frequency information collected by sensors within a vicinity of the resource or entity in the protected systems network in response to detecting that the resource or entity recently became active; and\ndetermining the COS and the PAOO based on the characteristic information received from the protected system network comprises:\ndetermining the COS and an approximate area associated with the recently active resource or entity based on the received activity information, signal level information, and frequency information.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00018",
            "claim_text": "18. The server computing device of claim 12, wherein the processor is configured with processor executable instructions to perform operations such that receiving characteristic information from the protected system network comprises:\nreceiving a spectrum reservation message from the protected system network indicating that the resource or entity is anticipated to become active in an area; and\nwherein the processor is configured with processor executable instructions to perform operations such that determining the COS and the AOO based on the characteristic information received from the protected system network comprises:\ndetermining the COS and an approximate area of the resource or entity that is anticipated to become active based on the received spectrum reservation message.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00019",
            "claim_text": "19. The server computing device of claim 12, wherein the processor is configured with processor executable instructions to perform operations such that sending the generated message to the component in the commercial network to cause that component to suppress the identified frequencies in the identified cells comprises sending the generated message to the component in the commercial network to cause that component to:\nstop all transmissions on the identified frequencies;\nreduce power on the identified frequencies;\nreorient antennas to direct power away from the resource or entity in the protected systems network; or\ndown-tilt or direct the antennas into focused areas that only allow the power to be transmitted in the immediate vicinity of the identified cells.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00020",
            "claim_text": "20. The server computing device of claim 12, wherein the processor is configured with processor executable instructions to perform operations further comprising:\nreceiving a notification message from the protected system network indicating that a detected activity identified in the received characteristic information has ceased; and\ncausing the component in the commercial network to cease suppressing the identified frequencies in the identified cells and restore power levels in response to the processor receiving the notification message from the protected system network indicating that the detected activity identified in the received characteristic information has ceased.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00021",
            "claim_text": "21. The server computing device of claim 20, wherein the processor is configured with processor executable instructions to perform operations such that causing the component in the commercial network to cease suppressing the identified frequencies in the identified cells and restore power levels comprises sending a communication message to the component that causes the component to reorient and uptilt antennas back to configurations that are optimized for full utilization of the identified frequencies on the commercial network.",
            "claim_type": "dependent",
            "dependency": "claim 20",
            "is_exemplary": true
          },
          {
            "claim_number": "00022",
            "claim_text": "22. The server computing device of claim 12, wherein the processor is configured with processor executable instructions to perform operations such that determining potential interference based on the information received from the commercial network and the characteristic information received from the protected system network comprises:\ndetermining the cell sites and frequencies that would result in interference between the resource or entity within the protected systems network and specific cells and attached mobiles in the commercial network.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00023",
            "claim_text": "23. A non-transitory computer readable storage medium having stored thereon processor-executable software instructions configured to cause a processor of a server computing device perform operations for dynamically sharing spectrum between a commercial network and a protected system network, the operations comprising:\nreceiving information from the commercial network;\nreceiving characteristic information identifying one or more characteristics of a resource or entity in the protected system network;\ndetermining a class of system (COS) and a area of operation (AOO) for the resource or entity based on the characteristic information received from the protected system network;\ndetermining potential interference based on the information received from the commercial network and the characteristic information received from the protected system network;\ndetermining which frequencies may be suppressed on which cells in the commercial network based on the determined potential interference;\ngenerating a suppression message that identifies the determined frequencies per cell; and\nsending the generated suppression message to a component in the commercial network to cause that component to suppress the identified frequencies in the identified cells.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00024",
            "claim_text": "24. The non-transitory computer readable storage medium of claim 23, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations such that generating the suppression message that identifies the determined frequencies per cell comprises generating an obfuscation message that mask the activities, operations, communications, locations, features, properties, or characteristics of the resource or entity in the protected system network.",
            "claim_type": "dependent",
            "dependency": "claim 23",
            "is_exemplary": true
          },
          {
            "claim_number": "00025",
            "claim_text": "25. The non-transitory computer readable storage medium of claim 24, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations such that generating the obfuscation message comprises adding additional frequencies that mask the activities, operations, communications, locations, features, properties, or characteristics of the resource or entity in the protected system network to the suppression message.",
            "claim_type": "dependent",
            "dependency": "claim 24",
            "is_exemplary": true
          },
          {
            "claim_number": "00026",
            "claim_text": "26. The non-transitory computer readable storage medium of claim 23, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations further comprising:\nusing a generative adversarial network (GAN) that includes a deep neural network and a generator to produce fake data;\ninserting the generated fake data into the suppression message prior to sending the generated suppression message to the component in the commercial network; or\nusing the generated fake data to generate additional suppression messages that are intentionally misleading and sending the additional suppression messages to the component in the commercial network.",
            "claim_type": "dependent",
            "dependency": "claim 23",
            "is_exemplary": true
          },
          {
            "claim_number": "00027",
            "claim_text": "27. The non-transitory computer readable storage medium of claim 23, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations further comprising using a generative adversarial network (GAN) that includes a deep neural network and a generator to detect and differentiate between real and fake activities of the resource or entities in the protected systems network.",
            "claim_type": "dependent",
            "dependency": "claim 23",
            "is_exemplary": true
          },
          {
            "claim_number": "00028",
            "claim_text": "28. The non-transitory computer readable storage medium of claim 23, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations such that:\nreceiving characteristic information from the protected system network comprises:\nreceiving detected activity information, signal level information and frequency information collected by sensors within a vicinity of the resource or entity in the protected systems network in response to detecting that the resource or entity recently became active; and\ndetermining the COS and the AOO based on the characteristic information received from the protected system network comprises:\ndetermining the COS and an approximate area associated with the recently active resource or entity based on the received activity information, signal level information, and frequency information.",
            "claim_type": "dependent",
            "dependency": "claim 23",
            "is_exemplary": true
          },
          {
            "claim_number": "00029",
            "claim_text": "29. The non-transitory computer readable storage medium of claim 23, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations such that receiving characteristic information from the protected system network comprises:\nreceiving a spectrum reservation message from the protected system network indicating that the resource or entity is anticipated to become active in an area; and\nwherein the stored processor-executable software instructions are configured to cause a processor to perform operations such that determining the COS and the AOO based on the characteristic information received from the protected system network comprises:\ndetermining the COS and an approximate area of the resource or entity that is anticipated to become active based on the received spectrum reservation message.",
            "claim_type": "dependent",
            "dependency": "claim 23",
            "is_exemplary": true
          },
          {
            "claim_number": "00030",
            "claim_text": "30. The non-transitory computer readable storage medium of claim 23, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations such that sending the generated message to the component in the commercial network to cause that component to suppress the identified frequencies in the identified cells comprises sending the generated message to the component in the commercial network to cause that component to:\nstop all transmissions on the identified frequencies;\nreduce power on the identified frequencies;\nreorient antennas to direct power away from the resource or entity in the protected systems network; or\ndown-tilt or direct the antennas into focused areas that only allow the power to be transmitted in the immediate vicinity of the identified cells.",
            "claim_type": "dependent",
            "dependency": "claim 23",
            "is_exemplary": true
          },
          {
            "claim_number": "00031",
            "claim_text": "31. The non-transitory computer readable storage medium of claim 23, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations further comprising:\nreceiving a notification message from the protected system network indicating that a detected activity identified in the received characteristic information has ceased; and\ncausing the component in the commercial network to cease suppressing the identified frequencies in the identified cells and restore power levels in response to the processor receiving the notification message from the protected system network indicating that the detected activity identified in the received characteristic information has ceased.",
            "claim_type": "dependent",
            "dependency": "claim 23",
            "is_exemplary": true
          },
          {
            "claim_number": "00032",
            "claim_text": "32. The non-transitory computer readable storage medium of claim 31, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations such that causing the component in the commercial network to cease suppressing the identified frequencies in the identified cells and restore power levels comprises sending a communication message to the component that causes the component to reorient and uptilt antennas back to configurations that are optimized for full utilization of the identified frequencies on the commercial network.",
            "claim_type": "dependent",
            "dependency": "claim 31",
            "is_exemplary": true
          },
          {
            "claim_number": "00033",
            "claim_text": "33. The non-transitory computer readable storage medium of claim 23, wherein the stored processor-executable software instructions are configured to cause a processor to perform operations such that determining potential interference based on the information received from the commercial network and the characteristic information received from the protected system network comprises:\ndetermining the cell sites and frequencies that would result in interference between the resource or entity within the protected systems network and specific cells and attached mobiles in the commercial network.",
            "claim_type": "dependent",
            "dependency": "claim 23",
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.8,
        "publication_date": "2024-03-26",
        "patent_year": 2024
      },
      {
        "patent_id": "11638169",
        "title": "First radio access technology (RAT) channel state feedback (CSF) to increase accuracy of interference estimates from second RAT neighbor cells with dynamic spectrum sharing (DSS)",
        "abstract": "A user equipment (UE) receives, from a base station, a message including at least one reporting configuration and resource configuration for a number of channel state information-interference measurement (CSI-IM) resource patterns associated with a first radio access technology (RAT). Each of the configured CSI-IM resource patterns corresponds to a time and frequency location in a resource block of a neighbor cell associated with a second RAT. The UE transmits one or more CSI reports based on the reporting configuration(s) and the resource configuration(s).",
        "inventors": [
          "Alexei Yurievitch Gorokhov",
          "Hobin Kim",
          "Hari Sankar",
          "Faris RASSAM"
        ],
        "assignees": [
          "QUALCOMM Incorporated"
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. A method for wireless communication performed by a user equipment (UE), comprising:\nreceiving, from a base station, a message comprising at least one reporting configuration and at least one resource configuration for a plurality of channel state information-interference measurement (CSI-IM) resource patterns associated with a first radio access technology (RAT), each CSI-IM resource pattern of the plurality of CSI-IM resource patterns corresponding to a time and frequency location in a resource block of a neighbor cell associated with a second RAT; and\ntransmitting at least one CSI report based on the at least one reporting configuration and the at least one resource configuration.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The method of claim 1, in which:\nthe at least one reporting configuration configures reporting for a plurality of CSI reports, each CSI report of the plurality of CSI reports corresponding to a CSI-IM resource pattern of the plurality of CSI-IM resource patterns;\nan interference measurement of each CSI report comprises a total interference power of a set of resource elements (REs) of the resource blocks aligned with a time and frequency location of the CSI-IM resource pattern corresponding to the CSI report; and\nthe set of REs comprises at least one of a cell-specific reference signal (CRS) RE, a first physical downlink shared channel (PDSCH) RE in a symbol including CRS REs, or a second PDSCH RE in a symbol without CRS REs.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The method of claim 2, in which:\nthe at least one reporting configuration indicates a periodic reporting periodicity;\nthe transmitting the at least one CSI report comprises transmitting each CSI report of the plurality of CSI reports according to the periodic reporting periodicity; and\nthe method further comprises measuring the interference measurement for each CSI-IM resource pattern of the plurality of CSI-IM resource patterns.",
            "claim_type": "dependent",
            "dependency": "claim 2",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The method of claim 2, in which:\nthe at least one reporting configuration indicates a semi-persistent reporting periodicity;\nthe transmitting the at least one CSI report comprises transmitting each CSI report of a set of CSI reports from the plurality of CSI reports according to the semi-persistent reporting periodicity; and\nthe method further comprises:\nreceiving a signal for activating the set of CSI reports and a set of CSI-IM resource patterns corresponding to the set of CSI reports; and\nmeasuring the interference power for each CSI-IM resource pattern of the set of CSI-IM resource patterns.",
            "claim_type": "dependent",
            "dependency": "claim 2",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The method of claim 4, in which CSI resources are semi-persistent resources or periodic resources.",
            "claim_type": "dependent",
            "dependency": "claim 4",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. The method of claim 2, in which:\nthe at least one reporting configuration indicates an aperiodic reporting periodicity;\ntransmitting the at least one CSI report comprises transmitting each CSI report of a set of CSI reports from the plurality of CSI reports in response to a trigger; and\nthe method further comprises:\nreceiving the trigger for triggering the set of CSI reports and a set of CSI-IM resource patterns corresponding to the set of CSI reports; and\nmeasuring the interference power for each CSI-IM resource pattern of the set of CSI-IM resource patterns.",
            "claim_type": "dependent",
            "dependency": "claim 2",
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The method of claim 6, in which CSI resources are periodic resources, semi-persistent resources or aperiodic resources.",
            "claim_type": "dependent",
            "dependency": "claim 6",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The method of claim 1, in which a first frequency shift parameter (vShift) of cell-specific reference signal (CRS) resource elements (REs) of a serving cell of the second RAT is different from a second vShift of CRS REs of the neighbor cell.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. A method for wireless communication performed by a base station associated with a first radio access technology (RAT), comprising:\nconfiguring at least one reporting configuration and at least one resource configuration for a plurality of channel state information-interference measurement (CSI-IM) resource patterns associated with the first RAT, each CSI-IM resource pattern of the plurality of CSI-IM resource patterns corresponding to a time and frequency location in a resource block of a neighbor cell associated with a second RAT;\ntransmitting, to a user equipment (UE), a message comprising the at least one reporting configuration and the at least one resource configuration; and\nreceiving, from the UE, at least one CSI report based on the transmitted message.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. The method of claim 9, in which:\nthe at least one reporting configuration configures reporting for a plurality of CSI reports, each CSI report of the plurality of CSI reports corresponding to a CSI-IM resource pattern of the plurality of CSI-IM resource patterns;\neach CSI report comprises an interference measurement based on a total interference power of a set of resource elements (REs) of the resource blocks aligned with a time and frequency location of a CSI-IM resource pattern corresponding to the CSI report;\nthe set of REs comprises at least one of a cell-specific reference signal (CRS) RE, a first physical downlink shared channel (PDSCH) RE in a symbol including CRS REs, or a second PDSCH RE in a symbol without CRS REs; and\nthe method further comprises receiving, from the UE, a signal strength measurement of the neighbor cell.",
            "claim_type": "dependent",
            "dependency": "claim 9",
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. The method of claim 10, in which:\nthe at least one reporting configuration indicates a periodic reporting periodicity;\nthe receiving the at least one CSI report comprises receiving each CSI report of the plurality of CSI reports according to the periodic reporting periodicity; and\nthe method further comprises:\nselecting one or more CSI reports from the plurality of CSI reports based on the signal strength measurement of the neighbor cell; and\nscheduling the UE based on the interference measurement of the one or more CSI reports.",
            "claim_type": "dependent",
            "dependency": "claim 10",
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. The method of claim 10, in which:\nthe at least one reporting configuration indicates a semi-persistent reporting periodicity;\nthe receiving the at least one CSI report comprises receiving each CSI report of a set of CSI reports from the plurality of CSI reports according to the semi-persistent reporting periodicity; and\nthe method further comprises transmitting a signal for activating the set of CSI reports and a set of CSI-IM resource patterns corresponding to the set of CSI reports based on the signal strength measurement of the neighbor cell.",
            "claim_type": "dependent",
            "dependency": "claim 10",
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. The method of claim 12, in which CSI resources are semi-persistent resources or periodic resources.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. The method of claim 10, in which:\nthe at least one reporting configuration indicates an aperiodic reporting periodicity;\nthe receiving the at least one CSI report comprises receiving each CSI report of a set of CSI reports from the plurality of CSI reports in response to a trigger; and\nthe method further comprises transmitting the trigger to trigger the set of CSI reports and a set of CSI-IM resource patterns corresponding to the set of CSI reports based on the signal strength measurement of the neighbor cell.",
            "claim_type": "dependent",
            "dependency": "claim 10",
            "is_exemplary": true
          },
          {
            "claim_number": "00015",
            "claim_text": "15. The method of claim 14, in which CSI resources are periodic resources, semi-persistent resources or aperiodic resources.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00016",
            "claim_text": "16. The method of claim 9, in which a first frequency shift parameter (vShift) of cell-specific reference signal (CRS) resource elements (REs) of a serving cell of the second RAT is different from a second vShift of CRS REs of the neighbor cell.",
            "claim_type": "dependent",
            "dependency": "claim 9",
            "is_exemplary": true
          },
          {
            "claim_number": "00017",
            "claim_text": "17. An apparatus for wireless communications at a user equipment (UE), comprising:\na processor,\nmemory coupled with the processor; and\ninstructions stored in the memory and operable, when executed by the processor, to cause the apparatus:\nto receive, from a base station, a message comprising at least one reporting configuration and at least one resource configuration for a plurality of channel state information-interference measurement (CSI-IM) resource patterns associated with a first radio access technology (RAT), each CSI-IM resource pattern of the plurality of CSI-IM resource patterns corresponding to a time and frequency location in a resource block of a neighbor cell associated with a second RAT; and\nto transmit at least one CSI report based on the at least one reporting configuration and the at least one resource configuration.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00018",
            "claim_text": "18. The apparatus of claim 17, in which:\nthe at least one reporting configuration configures reporting for a plurality of CSI reports, each CSI report of the plurality of CSI reports corresponding to a CSI-IM resource pattern of the plurality of CSI-IM resource patterns;\nan interference measurement of each CSI report comprises a total interference power of a set of resource elements (REs) of the resource blocks aligned with a time and frequency location of a CSI-IM resource pattern corresponding to the CSI report; and\nthe set of REs comprises at least one of a cell-specific reference signal (CRS) RE, a first physical downlink shared channel (PDSCH) RE in a symbol including CRS REs, or a second PDSCH RE in a symbol without CRS REs.",
            "claim_type": "dependent",
            "dependency": "claim 17",
            "is_exemplary": true
          },
          {
            "claim_number": "00019",
            "claim_text": "19. The apparatus of claim 18, in which:\nthe at least one reporting configuration indicates a periodic reporting periodicity; and\nthe processor causes the apparatus:\nto transmit the at least one CSI report by transmitting each CSI report of the plurality of CSI reports according to the periodic reporting periodicity; and\nto measure the interference measurement for each CSI-IM resource pattern of the plurality of CSI-IM resource patterns.",
            "claim_type": "dependent",
            "dependency": "claim 18",
            "is_exemplary": true
          },
          {
            "claim_number": "00020",
            "claim_text": "20. The apparatus of claim 18, in which:\nthe at least one reporting configuration indicates a semi-persistent reporting periodicity; and\nthe processor causes the apparatus:\nto transmit the at least one CSI report by transmitting each CSI report of a set of CSI reports from the plurality of CSI reports according to the semi-persistent reporting periodicity;\nto receive a signal for activating the set of CSI reports and a set of CSI-IM resource patterns corresponding to the set of CSI reports; and\nto measure the interference power for each CSI-IM resource pattern of the set of CSI-IM resource patterns.",
            "claim_type": "dependent",
            "dependency": "claim 18",
            "is_exemplary": true
          },
          {
            "claim_number": "00021",
            "claim_text": "21. The apparatus of claim 18, in which:\nthe at least one reporting configuration indicates an aperiodic reporting periodicity; and\nthe processor causes the apparatus:\nto transmit the at least one CSI report by transmitting each CSI report of a set of CSI reports from the plurality of CSI reports in response to a trigger; and\nto receive the trigger for triggering the set of CSI reports and a set of CSI-IM resource patterns corresponding to the set of CSI reports; and\nto measure the interference power for each CSI-IM resource pattern of the set of CSI-IM resource patterns.",
            "claim_type": "dependent",
            "dependency": "claim 18",
            "is_exemplary": true
          },
          {
            "claim_number": "00022",
            "claim_text": "22. The apparatus of claim 17, in which a first frequency shift parameter (vShift) of cell-specific reference signal (CRS) resource elements (REs) of a serving cell of the second RAT is different from a second vShift of CRS REs of the neighbor cell.",
            "claim_type": "dependent",
            "dependency": "claim 17",
            "is_exemplary": true
          },
          {
            "claim_number": "00023",
            "claim_text": "23. An apparatus for wireless communications at a base station associated with a first radio access technology (RAT), comprising:\na processor,\nmemory coupled with the processor; and\ninstructions stored in the memory and operable, when executed by the processor, to cause the apparatus:\nto configure at least one reporting configuration and at least one resource configuration for a plurality of channel state information-interference measurement (CSI-IM) resource patterns associated with the first RAT, each CSI-IM resource pattern of the plurality of CSI-IM resource patterns corresponding to a time and frequency location in a resource block of a neighbor cell associated with a second RAT;\nto transmit, to a user equipment (UE), a message comprising the at least one reporting configuration and the at least one resource configuration; and\nto receive, from the UE, at least one CSI report based on the transmitted message.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00024",
            "claim_text": "24. The apparatus of claim 23, in which:\nthe at least one reporting configuration configures reporting for a plurality of CSI reports, each CSI report of the plurality of CSI reports corresponding to a CSI-IM resource pattern of the plurality of CSI-IM resource patterns;\neach CSI report comprises an interference measurement based on a total interference power of a set of resource elements (REs) of the resource blocks aligned with a time and frequency location of a CSI-IM resource pattern corresponding to the CSI report;\nthe set of REs comprise at least one of a cell-specific reference signal (CRS) RE, a first physical downlink shared channel (PDSCH) RE in a symbol including CRS REs, or a second PDSCH RE in a symbol without CRS REs; and\nthe processor causes the apparatus to receive, from the UE, a signal strength measurement of the neighbor cell.",
            "claim_type": "dependent",
            "dependency": "claim 23",
            "is_exemplary": true
          },
          {
            "claim_number": "00025",
            "claim_text": "25. The apparatus of claim 24, in which CSI resources are semi-persistent resources or periodic resources.",
            "claim_type": "dependent",
            "dependency": "claim 24",
            "is_exemplary": true
          },
          {
            "claim_number": "00026",
            "claim_text": "26. The apparatus of claim 24, in which:\nthe at least one reporting configuration indicates a periodic reporting periodicity; and\nthe processor causes the apparatus:\nto receive the at least one CSI report by receiving each CSI report of the plurality of CSI reports according to the periodic reporting periodicity;\nto select one or more CSI reports from the plurality of CSI reports based on the signal strength measurement of the neighbor cell; and\nto schedule the UE based on the interference measurement of the one or more CSI reports.",
            "claim_type": "dependent",
            "dependency": "claim 24",
            "is_exemplary": true
          },
          {
            "claim_number": "00027",
            "claim_text": "27. The apparatus of claim 24, in which:\nthe at least one reporting configuration indicates a semi-persistent reporting periodicity; and\nthe processor causes the apparatus:\nto receive the at least one CSI report by receiving each CSI report of a set of CSI reports from the plurality of CSI reports according to the semi-persistent reporting periodicity; and\nto transmit a signal for activating the set of CSI reports and a set of CSI-IM resource patterns corresponding to the set of CSI reports based on the signal strength measurement of the neighbor cell.",
            "claim_type": "dependent",
            "dependency": "claim 24",
            "is_exemplary": true
          },
          {
            "claim_number": "00028",
            "claim_text": "28. The apparatus of claim 26, in which CSI resources are periodic resources, semi-persistent resources or aperiodic resources.",
            "claim_type": "dependent",
            "dependency": "claim 26",
            "is_exemplary": true
          },
          {
            "claim_number": "00029",
            "claim_text": "29. The apparatus of claim 24, in which:\nthe at least one reporting configuration indicates an aperiodic reporting periodicity; and\nthe processor causes the apparatus:\nto receive the at least one CSI report by receiving each CSI report of a set of CSI reports from the plurality of CSI reports in response to a trigger; and\nto transmit the trigger for triggering the set of CSI reports and a set of CSI-IM resource patterns corresponding to the set of CSI reports based on the signal strength measurement of the neighbor cell.",
            "claim_type": "dependent",
            "dependency": "claim 24",
            "is_exemplary": true
          },
          {
            "claim_number": "00030",
            "claim_text": "30. The apparatus of claim 23, in which a first frequency shift parameter (vShift) of cell-specific reference signal (CRS) resource elements (REs) of a serving cell of the second RAT is different from a second vShift of CRS REs of the neighbor cell.",
            "claim_type": "dependent",
            "dependency": "claim 23",
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.8,
        "publication_date": "2023-04-25",
        "patent_year": 2023
      },
      {
        "patent_id": "7450947",
        "title": "Method and apparatus for dynamic spectrum sharing",
        "abstract": "A technique for dynamic spectrum sharing includes identifying (705) a plurality of radio nodes (115, 120), measuring (710) a local signal value (SV) at each radio node (110, 200), and determining (715) a transmit decision. Each radio node can measure a local signal value (SV) of a protected transmission and the radio nodes are within a uniform SV region of the protected transmission. The transmit decision is determined for at least one of the plurality of radio nodes based on the SV of each radio node in the plurality of radio nodes and at least one threshold value that is related to statistical characteristics of the protected transmission at an interference boundary (105) of the protected transmission and a desired probability of non-interference with the protected transmission at the interference boundary.",
        "inventors": [
          "Eugene Visotsky",
          "Stephen L. Kuffner",
          "Roger L. Peterson"
        ],
        "assignees": [
          "Motorola, Inc."
        ],
        "claims": [],
        "relevance_score": 0.8,
        "publication_date": "2008-11-11",
        "patent_year": 2008
      },
      {
        "patent_id": "12238529",
        "title": "Electronic device and method of controlling electronic device in communication network supporting dynamic spectrum sharing",
        "abstract": "An electronic device is provided. The electronic device includes a communication processor, at least one Radio Frequency Integrated Circuit (RFIC) connected thereto, and an antenna connected through the at least one RFIC and configured to transmit and receive a signal corresponding to at least one communication network. The communication processor is configured to control the electronic device to receive a signal corresponding to a first communication network from a first base station corresponding to the first communication network supporting a first frequency band through the antenna, identify information related to a second communication network supporting a second frequency band including at least a portion of the first frequency band, identify a time interval allocated for transmission of data corresponding to the second communication network on the basis of the information related to the second communication network, and operate in a sleep state in the identified time interval.",
        "inventors": [
          "Dooyoung KIM",
          "Euichang JUNG",
          "Sunmin HWANG"
        ],
        "assignees": [
          "Samsung Electronics Co., Ltd."
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. An electronic device comprising:\na communication processor;\nat least one radio frequency integrated circuit (RFIC) connected to the communication processor;\nan antenna connected to the at least one RFIC and configured to transmit and receive a signal corresponding to at least one communication network, and\nmemory storing instructions,\nwherein the instructions, when executed by the communication processor, cause the electronic device to:\ncontrol the electronic device to receive a signal corresponding to a first communication network from a first base station corresponding to the first communication network supporting a first frequency band, through the antenna,\nidentify information related to a second communication network supporting a second frequency band including at least a portion of the first frequency band,\nidentify a time interval allocated for transmission of data corresponding to the second communication network, based on the information related to the second communication network, and\ncontrol the electronic device to operate in a sleep state in the identified time interval,\n\nwherein, when the first base station corresponding to a long term evolution (LTE) communication network does not transmit broadcast service data through predetermined subframes configured as multimedia broadcast multicast service single frequency network (MBSFN) subframes or does not transmit any data, dynamic spectrum sharing (DSS) in a time division multiplexing scheme is applied through the predetermined subframes.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The electronic device of claim 1, wherein the instructions further cause the electronic device to control to refrain from identifying control data corresponding to the first communication network while in the sleep state.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The electronic device of claim 1, wherein the instructions further cause the electronic device to identify the time interval allocated for transmission of the data corresponding to the second communication network when there is the second communication network supporting the second frequency band including at least the portion of the first frequency band.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The electronic device of claim 1, wherein the instructions further cause the electronic device to:\nreceive a signal transmitted from a second base station corresponding to the second communication network for a preset time, and\nidentify the time interval allocated for transmission of the data corresponding to the second communication network from the received signal.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The electronic device of claim 1, wherein the first base station corresponds to new radio (NR) communication network data in at least one subframe in which the LTE communication network data is not transmitted among predetermined subframes which are not configured as the MBSFN subframes and which are allocated for use by a second base station of the LTE communication network.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. One or more non-transitory computer-readable storage media storing one or more programs including computer-executable instructions that, when executed by one or more processors of an electronic device individually or collectively, cause to the electronic to perform operations, the operations comprising:\nreceiving a signal corresponding to a first communication network from a first base station corresponding to the first communication network supporting a first frequency band through an antenna;\nidentifying information related to a second communication network supporting a second frequency band including at least a portion of the first frequency band;\nidentifying a time interval allocated for transmission of data corresponding to the second communication network, based on the information related to the second communication network; and\ncontrolling the electronic device to operate in a sleep state in the identified time interval,\nwherein, when the first base station corresponding to a long term evolution (LTE) communication network does not transmit broadcast service data through predetermined subframes configured as multimedia broadcast multicast service single frequency network (MBSFN) subframes or does not transmit any data, dynamic spectrum sharing (DSS) in a time division multiplexing scheme is applied through the predetermined subframes.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The one or more non-transitory computer-readable storage media of claim 6, the operations further comprise controlling the electronic device to refrain from identifying control data corresponding to the first communication network while in the sleep state.",
            "claim_type": "dependent",
            "dependency": "claim 6",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The one or more non-transitory computer-readable storage media of claim 6, the operations further comprise identifying the time interval allocated for transmission of the data corresponding to the second communication network when there is the second communication network supporting the second frequency band including at least the portion of the first frequency band.",
            "claim_type": "dependent",
            "dependency": "claim 6",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. The one or more non-transitory computer-readable storage media of claim 8, the operations further comprise identifying whether there is the second communication network, based on frequency band information related to a neighbor base station of the first base station.",
            "claim_type": "dependent",
            "dependency": "claim 8",
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. The one or more non-transitory computer-readable storage media of claim 6, wherein the first base station corresponds to new radio (NR) communication network data in at least one subframe in which the LTE communication network data is not transmitted among predetermined subframes which are not configured as the MBSFN subframes and which are allocated for use by a second base station of the LTE communication network.",
            "claim_type": "dependent",
            "dependency": "claim 6",
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.8,
        "publication_date": "2025-02-25",
        "patent_year": 2025
      },
      {
        "patent_id": "12185118",
        "title": "Dual connectivity cell selection with dynamic spectrum sharing",
        "abstract": "The disclosed technology is directed towards avoiding a misconfiguration that uses a Long Term Evolution (LTE) and new radio dynamic spectrum sharing (DSS) carrier as an LTE carrier and new radio primary secondary cell carrier concurrently for a dual connectivity mobile device. Network equipment can detect the misconfiguration and prevent its usage, or if already configured, deconfigure the LTE DSS secondary cell during setup of a dual connectivity mobile device. Alternatively a dual connectivity mobile device can detect the misconfiguration and notify the network to terminate one of the carriers. Information regarding the misconfiguration can be saved in the mobile device to proactively avoid the dual misconfiguration going forward. Such information can be communicated to other mobile devices, as well as the network.",
        "inventors": [
          "Yupeng Jia"
        ],
        "assignees": [
          "AT&T Intellectual Property I, L.P."
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. A first mobile device, comprising:\na processor; and\na memory that stores executable instructions which, when executed by the processor of the first mobile device, facilitate performance of operations, the operations comprising:\ndetermining whether first dynamic spectrum sharing data corresponding to a long term evolution secondary cell of a communication network and second dynamic spectrum sharing data corresponding to a new radio primary secondary cell of the communication network have been concurrently received by the first mobile device via a frequency carrier;\nin response to the first dynamic spectrum sharing data and the second dynamic spectrum sharing data being determined to have been concurrently received by the first mobile device via the frequency carrier, performing an action to prevent a future reception, via the frequency carrier, of one of: the first dynamic spectrum sharing data or the second dynamic spectrum sharing data by the first mobile device; and\nsending a first dynamic spectrum sharing cell misconfiguration message to a second mobile device, wherein the first dynamic spectrum sharing cell misconfiguration message causes the communication network to drop the one of: the first dynamic spectrum sharing data or the second dynamic spectrum sharing data and to record, in a storage accessible to the first mobile device, a network identifier of the long term evolution secondary cell to avoid, based on the identifier, the future reception of the first dynamic spectrum sharing data by the first mobile device.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The first mobile device of claim 1, wherein the performing the action comprises terminating a usage of a long term evolution carrier associated with the long term evolution secondary cell.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The first mobile device of claim 2, wherein the terminating the usage of the long term evolution carrier comprises sending a long term evolution radio link failure message to network equipment of the communication network.",
            "claim_type": "dependent",
            "dependency": "claim 2",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The first mobile device of claim 2, wherein the terminating the usage of the long term evolution carrier comprises sending a second dynamic spectrum sharing cell misconfiguration message to network equipment of the communication network.",
            "claim_type": "dependent",
            "dependency": "claim 2",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The first mobile device of claim 1, wherein the performing the action comprises terminating a usage of a new radio carrier associated with the new radio primary secondary cell.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. The first mobile device of claim 5, wherein the terminating the usage of the new radio carrier comprises sending a secondary cell group radio link failure message to network equipment of the communication network.",
            "claim_type": "dependent",
            "dependency": "claim 5",
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The first mobile device of claim 5, wherein the terminating the usage of the new radio carrier comprises sending a second dynamic spectrum sharing cell misconfiguration message to network equipment of the communication network.",
            "claim_type": "dependent",
            "dependency": "claim 5",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The first mobile device of claim 1, wherein the sending comprises:\ncommunicating the first dynamic spectrum sharing cell misconfiguration message to the second mobile device via direct device-to-device communication.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. The first mobile device of claim 1, further comprising:\nbroadcasting the identifier of the long term evolution secondary cell to a third mobile device.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. Network equipment, comprising:\na processor; and\na memory that stores executable instructions which, when executed by the processor of the network equipment, facilitate performance of operations, the operations comprising:\nreceiving, from a dual connectivity mobile device, a dynamic spectrum sharing cell misconfiguration message;\ndetermining, in response to the receiving, that a long term evolution secondary cell of a communication network has been configured for a concurrent communication, via a carrier frequency, with the dual connectivity mobile device;\ndetermining, in response to the receiving, that a new radio primary secondary cell of the communication network has been configured for the concurrent communication with the dual connectivity mobile device;\ndetermining, in response to the receiving, that the dual connectivity mobile device has recorded, in a storage accessible to the dual connectivity mobile device, a network identifier of the long term evolution secondary cell to avoid, based on the identifier, a future reception of the concurrent communication by the dual connectivity mobile device; and\nin response to the determining that the long term evolution secondary cell and the new radio primary secondary cell have been configured for the concurrent communication, performing an action with respect to blocking a reception by the dual connectivity mobile device of dynamic spectrum sharing data corresponding to one of: the long term evolution secondary cell or the new radio primary secondary cell based on an indication in the dynamic spectrum sharing cell misconfiguration message that the dual connectivity mobile device has dropped the dynamic spectrum sharing data.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. The network equipment of claim 10, wherein the blocking the reception of the concurrent communication by the dual connectivity mobile device comprises: deconfiguring the long term evolution secondary cell in response to an indication in the dynamic spectrum sharing cell misconfiguration message.",
            "claim_type": "dependent",
            "dependency": "claim 10",
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. The network equipment of claim 11, wherein the deconfiguring the long term evolution secondary cell is performed during a dual connectivity setup of the dual connectivity mobile device.",
            "claim_type": "dependent",
            "dependency": "claim 11",
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. The network equipment of claim 11, wherein the blocking the reception of the concurrent communication by the dual connectivity mobile device comprises:\nexcluding the long term evolution secondary cell for usage by the dual connectivity mobile device until the new radio primary secondary cell is released by the dual connectivity mobile device.",
            "claim_type": "dependent",
            "dependency": "claim 11",
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. The network equipment of claim 10, wherein the blocking the reception of the concurrent communication by the dual connectivity mobile device comprises:\npreventing the long term evolution secondary cell from being utilized in concurrent communications comprising the concurrent communication corresponding to respective carrier frequencies comprising the carrier frequency.",
            "claim_type": "dependent",
            "dependency": "claim 10",
            "is_exemplary": true
          },
          {
            "claim_number": "00015",
            "claim_text": "15. The first mobile device of claim 10, wherein the second mobile device is a dual connectivity mobile device.",
            "claim_type": "dependent",
            "dependency": "claim 10",
            "is_exemplary": true
          },
          {
            "claim_number": "00016",
            "claim_text": "16. A non-transitory machine-readable medium, comprising executable instructions that, when executed by a processor of a first mobile device that is a dual connectivity mobile device, facilitate performance of operations of the processor, the operations comprising:\ndetermining that a long term evolution secondary cell of a cellular network and a new radio primary secondary cell of the cellular network have been misconfigured for a concurrent communication using a single carrier frequency;\nin response to the determining that the long term evolution secondary cell and the new radio primary secondary cell have been misconfigured, storing, in a data storage device of the dual connectivity mobile device, an identifier representing the long term evolution secondary cell;\nin response to detecting that the dual connectivity mobile device has left and subsequently re-entered a wireless coverage area of the long term evolution secondary cell, determining, based on the identifier that is stored, that a reception of the concurrent communication by the dual connectivity mobile device should be prevented while the dual connectivity mobile device remains within the wireless coverage area of the long term evolution secondary cell; and;\nand\ncommunicating, to a second mobile device, a dynamic spectrum sharing cell misconfiguration message that indicates that the long term evolution secondary cell and the new radio primary secondary cell have been misconfigured for the concurrent communication using the single carrier frequency, that the first mobile device has dropped dynamic spectrum sharing data corresponding to one of: the long term evolution secondary cell or the new radio primary secondary cell, and that the identifier has been recorded by the first mobile device to avoid the reception of the dynamic spectrum sharing data by the first mobile device while the first mobile device remains within the wireless coverage area of the long term evolution secondary cell.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00017",
            "claim_text": "17. The non-transitory machine-readable medium of claim 16, wherein the determining that the long term evolution secondary cell and the new radio primary secondary cell have been misconfigured comprises:\ncommunicating with network equipment of the cellular network to cease a long term evolution communication of the long term evolution secondary cell.",
            "claim_type": "dependent",
            "dependency": "claim 16",
            "is_exemplary": true
          },
          {
            "claim_number": "00018",
            "claim_text": "18. The non-transitory machine-readable medium of claim 16, wherein the operations further comprise:\nin response to entering the wireless coverage area of the long term evolution secondary cell, determining whether the identifier has been stored in the data storage device.",
            "claim_type": "dependent",
            "dependency": "claim 16",
            "is_exemplary": true
          },
          {
            "claim_number": "00019",
            "claim_text": "19. The non-transitory machine-readable medium of claim 16, wherein the second mobile device is a dual connectivity mobile device.",
            "claim_type": "dependent",
            "dependency": "claim 16",
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.8,
        "publication_date": "2024-12-31",
        "patent_year": 2024
      },
      {
        "patent_id": "12120531",
        "title": "Methods, systems, and apparatuses for handling dynamic spectrum sharing with uplink subcarrier shift",
        "abstract": "Embodiments described herein include methods, systems, and apparatuses for allowing a user equipment (UE) that supports dynamic spectrum sharing (DSS) with uplink (UL)-shift to access a cell and barring UEs that do not support DSS with UL-shift. Embodiments may use a cell barring field in a master information block and additional filters to indicate a barring state for a network node.",
        "inventors": [
          "Yuqin Chen",
          "Zhibin Wu",
          "Leilei Song",
          "Anatoliy Sergey Ioffe",
          "Fangli Xu",
          "Haijing Hu",
          "Sarma V. Vangala",
          "Naveen Kumar R Palle Venkata",
          "Ralf Rossbach",
          "Alexander Sayenko",
          "Ruoheng Liu"
        ],
        "assignees": [
          "Apple Inc."
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. A method for a user equipment (UE) that supports dynamic spectrum sharing (DSS) with uplink (UL)-shift, the method comprising:\nreceiving a first message from a network node, the first message comprising a cell barred field;\ndecoding the first message and determining status of the cell barred field;\nreceiving a second message from the network node comprising a second field related to barring UEs that support DSS with uplink-shift, and a third field related to support of UL-shift;\ndecoding the second message and determining status of the second field and the third field, wherein the second field is an exemption field which explicitly expresses whether UEs which support DSS with UL-shift are allowed to camp or not when the cell barred field is set to barred, and wherein the third field is a frequnecyShift7p5khz field; and\naccessing a cell when the cell barred field is set to barred and the second field indicates that the UEs which support DSS with UL-shift are allowed to access the cell, and the third field is set to true.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The method of claim 1, further comprising checking that the UE supports UL-shift only for an initial bandwidth part (BWP) against a particular sub-carrier spacing (SCS) the initial BWP is configured with, and wherein the UE accesses the cell when the UE supports UL-shift for the initial BWP.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The method of claim 1, further comprising checking that the UE supports UL shift for all the BWPs against a SCS broadcasted information provides, and wherein the UE accesses the cell only when the UE supports UL-shift for all BWPs.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The method of claim 1, wherein the first message is a master information block (MIB) and the second message is a system information block 1 (SIB1).",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The method of claim 1, wherein the second field is provided in a FrequencyInfoUL information element.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. The method of claim 1, further comprising reporting to the network node UL-shifting capability for each band that the UE supports.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. A user equipment (UE) that supports dynamic spectrum sharing (DSS) with uplink (UL)-shift, the UE comprising:\na baseband processing unit; and\na memory storing instructions that, when executed by the baseband processing unit, configure the UE to:\nreceive a first message from a network node, the first message comprising a cell barred field;\ndecode the first message and determining status of the cell barred field;\nreceive a second message from the network node comprising a second field related to barring UEs that support DSS with uplink-shift, and a third field related to support of UL-shift;\ndecode the second message and determining status of the second field and the third field, wherein the second field is an exemption field which explicitly expresses whether UEs which support DSS with UL-shift are allowed to camp or not when the cell barred field is set to barred, and wherein the third field is a frequencyShift7p5 hz field;\naccess a cell when the cell barred field is set to barred and the second field indicates that the UEs which support DSS with UL-shift are allowed to access the cell, and the third field is set to true.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The UE of claim 7, wherein the instructions further configure the baseband processing unit to check that the UE supports UL-shift only for an initial bandwidth part (BWP) against a particular sub-carrier spacing (SCS) the initial BWP is configured with, and wherein the UE accesses the cell when the UE supports UL-shift for the initial BWP.",
            "claim_type": "dependent",
            "dependency": "claim 7",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. The UE of claim 7, wherein the instructions further configure the baseband processing unit to check that the UE supports UL shift for all the BWPs against a SCS broadcasted information provides, and wherein the UE accesses the cell only when the UE supports UL-shift for all BWPs.",
            "claim_type": "dependent",
            "dependency": "claim 7",
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. The UE of claim 7, wherein the first message is a master information block (MIB) and the second message is a system information block 1 (SIB1).",
            "claim_type": "dependent",
            "dependency": "claim 7",
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. The UE of claim 7, wherein the second field is provided in a FrequencyInfoUL information element.",
            "claim_type": "dependent",
            "dependency": "claim 7",
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. The UE of claim 7, wherein the instructions further configure the baseband processing unit to report to the network node UL-shifting capability for each band that the UE supports.",
            "claim_type": "dependent",
            "dependency": "claim 7",
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. A non-transitory computer-readable storage medium of a user equipment (UE) that supports dynamic spectrum sharing (DSS) with uplink (UL)-shift, the computer-readable storage medium having computer-readable instructions stored thereon, the computer-readable instructions configured to instruct one or more processors to:\nreceive a first message from a network node, the first message comprising a cell barred field;\ndecode the first message and determining status of the cell barred field;\nreceive a second message from the network node comprising a second field related to barring UEs that support DSS with uplink-shift, and a third field related to support of UL-shift;\ndecode the second message and determining status of the second field and the third field, wherein the second field is an exemption field which explicitly expresses whether UEs which support DSS with UL-shift are allowed to camp or not when the cell barred field is set to barred, and wherein the third field is a frequencyShift7p5khz field;\naccess a cell when the cell barred field is set to barred and the second field indicates that the UEs which support DSS with UL-shift are allowed to access the cell, and the third field is set to true.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. The non-transitory computer-readable storage medium of claim 13, wherein the computer-readable instructions are configured to instruct the one or more processors to check that the UE supports UL-shift only for an initial bandwidth part (BWP) against a particular sub-carrier spacing (SCS) the initial BWP is configured with, and wherein the UE accesses the cell when the UE supports UL-shift for the initial BWP.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.8,
        "publication_date": "2024-10-15",
        "patent_year": 2024
      },
      {
        "patent_id": "12003975",
        "title": "Channel state information (CSI) measurement and report for dynamic spectrum sharing (DSS) in a wireless wide area network (WWAN)",
        "abstract": "This disclosure provides systems, methods, and apparatus, including computer programs encoded on computer-readable media, for implementing a channel state information (CSI) measurement and reporting protocol for dynamic spectrum sharing (DSS) in a wireless communication network. In some aspects, a BS may transmit control messages periodically and aperiodically that configure a UE to perform signal quality measurements and transmit signal quality reports. When the UE receives a periodic control message, the UE may perform signal quality measurements on both a multimedia broadcast single frequency network (MBSFN) subframe and a non-MBSFN subframe of a frame received from the BS. When the UE receives an aperiodic control message, the UE may perform a signal quality measurement on either a MBSFN subframe or a non-MBSFN subframe. The UE may generate and transmit signal quality reports to the BS periodically and aperiodically corresponding to the received periodic and aperiodic control messages, respectively.",
        "inventors": [
          "Juan Montojo",
          "Ming Yang",
          "Kausik Ray Chaudhuri"
        ],
        "assignees": [
          "QUALCOMM Incorporated"
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. A method for dynamic spectrum sharing (DSS) in a wireless wide area network (WWAN) performed by a first node, comprising:\nperforming a first signal quality measurement associated with a first subframe of a frame received from a second node, wherein the first subframe is associated with a first subframe type;\nperforming a second signal quality measurement associated with a second subframe of the frame, wherein the second subframe is associated with a second subframe type;\nidentifying that a first percentage of the frame includes subframes of the first subframe type, wherein the first signal quality measurement is associated with the subframes of the first subframe type;\nidentifying that a second percentage of the frame includes subframes of the second subframe type, wherein the second signal quality measurement is associated with the subframes of the second subframe type;\nweighing the first signal quality measurement according to the first percentage and the second signal quality measurement according to the second percentage;\ncalculating a third signal quality measurement using the weighted first signal quality measurement and the weighted second signal quality measurement; and\ntransmitting, to the second node, a first signal quality report associated with at least one of the first signal quality measurement and the second signal quality measurement and including the third signal quality measurement that is calculated using the weighted first signal quality measurement and the weighted second signal quality measurement.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The method of claim 1, wherein the first signal quality report is a channel state information (CSI) report, and performing the first signal quality measurement associated with the first subframe includes:\nperforming the first signal quality measurement on CSI reference signals (CSI-RSs) included in the first subframe, or\nperforming the first signal quality measurement on data included in the first subframe.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The method of claim 2, wherein:\nthe data includes data of a Physical Downlink Shared Channel (PDSCH).",
            "claim_type": "dependent",
            "dependency": "claim 2",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The method of claim 1, wherein performing the second signal quality measurement associated with the second subframe includes:\nperforming the second signal quality measurement on channel state information (CSI) reference signals (CSI-RSs) included in the second subframe, or\nperforming the second signal quality measurement on data included in the second subframe.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The method of claim 4, wherein:\nthe data includes data of a Physical Downlink Shared Channel (PDSCH).",
            "claim_type": "dependent",
            "dependency": "claim 4",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. The method of claim 4, wherein the first signal quality report is a CSI report.",
            "claim_type": "dependent",
            "dependency": "claim 4",
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The method of claim 1, wherein transmitting the first signal quality report including the third signal quality measurement comprises:\ntransmitting the first signal quality report including the third signal quality measurement periodically according to a time interval.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The method of claim 1, further comprising:\ngenerating one or more additional signal quality reports;\nindicating either the first signal quality measurement or the second signal quality measurement; and\ntransmitting the one or more additional signal quality reports to the second node.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. The method of claim 8, wherein transmitting the one or more additional signal quality reports comprises:\ntransmitting the one or more additional signal quality reports periodically according to a time interval.",
            "claim_type": "dependent",
            "dependency": "claim 8",
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. The method of claim 1, further comprising:\nreceiving a radio resource control (RRC) message from the second node; and\nperforming the first signal quality measurement and the second signal quality measurement based on receiving the RRC message from the second node.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. The method of claim 1, wherein the first subframe type is a multimedia broadcast single frequency network (MBSFN) subframe type and the second subframe type is a non-MBSFN subframe type.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. A method for dynamic spectrum sharing (DSS) in a wireless wide area network (WWAN) performed by a first node, comprising:\ntransmitting, to a second node, a control message that indicates one of a first subframe of a frame or a second subframe of the frame in which one or more channel state information (CSI) reference signals (CSI-RSs) are to be provided to the second node, wherein the first subframe is associated with a first subframe type and the second subframe is associated with a second subframe type;\nreceiving a first signal quality report from the second node, the first signal quality report indicating a third signal quality measurement that is a combination of a first signal quality measurement weighted by a percentage of the frame that includes subframes of the first subframe type and a second signal quality measurement weighted by a percentage of the frame that includes subframes of the second subframe type; and\nscheduling a data transmission in at least one of the first subframe and the second subframe, the scheduling being associated with the third signal quality measurement.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. The method of claim 12, wherein scheduling the data transmission in at least one of the first subframe and the second subframe includes at least one of:\nscheduling a first data transmission in the first subframe, the scheduling being associated with the first signal quality measurement; and\nscheduling a second data transmission in the second subframe, the scheduling being associated with the second signal quality measurement.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. The method of claim 13, wherein the first signal quality report further indicates at least one of the first signal quality measurement and the second signal quality measurement.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00015",
            "claim_text": "15. The method of claim 12, wherein receiving the first signal quality report indicating the third signal quality measurement comprises:\nreceiving the first signal quality report indicating the third signal quality measurement periodically according to a time interval.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00016",
            "claim_text": "16. The method of claim 12, wherein the first subframe type is a multimedia broadcast single frequency network (MBSFN) subframe type and the second subframe type is a non-MBSFN subframe type.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00017",
            "claim_text": "17. An apparatus of a first node configured to implement dynamic spectrum sharing (DSS) in a wireless wide area network (WWAN), the apparatus comprising:\none or more processors;\none or more memories coupled with the one or more processors; and\none or more processor-readable instructions stored in the one or more memories and executable by the one or more processors individually or collectively to cause the apparatus to:\nperform a first signal quality measurement associated with a first subframe of a frame received from a second node, and perform a second signal quality measurement associated with a second subframe of the frame, wherein the first subframe is associated with a first subframe type and the second subframe is associated with a second subframe type;\nidentify that a first percentage of the frame includes subframes of the first subframe type, wherein the first signal quality measurement is associated with the subframes of the first subframe type;\nidentify that a second percentage of the frame includes subframes of the second subframe type, wherein the second signal quality measurement is associated with the subframes of the second subframe type;\nweigh the first signal quality measurement according to the first percentage and the second signal quality measurement according to the second percentage;\ncalculate a third signal quality measurement using the weighted first signal quality measurement and the weighted second signal quality measurement; and\ntransmit, to the second node, a first signal quality report associated with at least one of the first signal quality measurement and the second signal quality measurement, and including the third signal quality measurement that is calculated using the weighted first signal quality measurement and the weighted second signal quality measurement.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00018",
            "claim_text": "18. The apparatus of claim 17, wherein the first signal quality report is a channel state information (CSI) report, and wherein, to perform the first signal quality measurement associated with the first subframe, the one or more processor-readable instructions are executable by the one or more processors individually or collectively to cause the apparatus to:\nperform the first signal quality measurement on CSI reference signals (CSI-RSs) included in the first subframe, or\nperform the first signal quality measurement on data included in the first subframe.",
            "claim_type": "dependent",
            "dependency": "claim 17",
            "is_exemplary": true
          },
          {
            "claim_number": "00019",
            "claim_text": "19. The apparatus of claim 18, wherein the data includes data of a Physical Downlink Shared Channel (PDSCH).",
            "claim_type": "dependent",
            "dependency": "claim 18",
            "is_exemplary": true
          },
          {
            "claim_number": "00020",
            "claim_text": "20. The apparatus of claim 17, wherein, to perform the second signal quality measurement associated with the second subframe, the one or more processor-readable instructions are executable by the one or more processors individually or collectively to cause the apparatus to:\nperform the second signal quality measurement on channel state information (CSI) reference signals (CSI-RSs) included in the second subframe, or\nperform the second signal quality measurement on data included in the second subframe.",
            "claim_type": "dependent",
            "dependency": "claim 17",
            "is_exemplary": true
          },
          {
            "claim_number": "00021",
            "claim_text": "21. The apparatus of claim 20, wherein the first signal quality report is a CSI report.",
            "claim_type": "dependent",
            "dependency": "claim 20",
            "is_exemplary": true
          },
          {
            "claim_number": "00022",
            "claim_text": "22. The apparatus of claim 20, wherein the data includes data of a Physical Downlink Shared Channel (PDSCH).",
            "claim_type": "dependent",
            "dependency": "claim 20",
            "is_exemplary": true
          },
          {
            "claim_number": "00023",
            "claim_text": "23. The apparatus of claim 17, wherein, to transmit the first signal quality report including the third signal quality measurement, the one or more processor-readable instructions are executable by the one or more processors individually or collectively to cause the apparatus to:\ntransmit the first signal quality report including the third signal quality measurement periodically according to a time interval.",
            "claim_type": "dependent",
            "dependency": "claim 17",
            "is_exemplary": true
          },
          {
            "claim_number": "00024",
            "claim_text": "24. The apparatus of claim 17, wherein the one or more processor-readable instructions are further executable by the one or more processors individually or collectively to cause the apparatus to:\ngenerate one or more additional signal quality reports; indicating either the first signal quality measurement or the second signal quality measurement; and\ntransmit the one or more additional signal quality reports to the second node.",
            "claim_type": "dependent",
            "dependency": "claim 17",
            "is_exemplary": true
          },
          {
            "claim_number": "00025",
            "claim_text": "25. The apparatus of claim 24, wherein, to transmit the one or more additional signal quality reports, the one or more processor-readable instructions are executable by the one or more processors individually or collectively to cause the apparatus to:\ntransmit the one or more additional signal quality reports periodically according to a time interval.",
            "claim_type": "dependent",
            "dependency": "claim 24",
            "is_exemplary": true
          },
          {
            "claim_number": "00026",
            "claim_text": "26. The apparatus of claim 17, wherein the one or more processor-readable instructions are further executable by the one or more processors individually or collectively to cause the apparatus to:\nreceive a radio resource control (RRC) message from the second node; and\nperform the first signal quality measurement and the second signal quality measurement based on reception of the RRC message from the second node.",
            "claim_type": "dependent",
            "dependency": "claim 17",
            "is_exemplary": true
          },
          {
            "claim_number": "00027",
            "claim_text": "27. The apparatus of claim 17, wherein the first subframe type is a multimedia broadcast single frequency network (MBSFN) subframe type and the second subframe type is a non-MBSFN subframe type.",
            "claim_type": "dependent",
            "dependency": "claim 17",
            "is_exemplary": true
          },
          {
            "claim_number": "00028",
            "claim_text": "28. An apparatus of a first node configured to implement dynamic spectrum sharing (DSS) in a wireless wide area network (WWAN), the apparatus comprising:\none or more processors;\none or more memories coupled with the one or more processors; and\none or more processor-readable instructions stored in the one or more memories and executable by the one or more processors individually or collectively to cause the apparatus to:\ntransmit, to a second node, a control message that indicates one of a first subframe of a frame or a second subframe of the frame in which one or more channel state information (CSI) reference signals (CSI-RSs) are to be provided to the second node, wherein the first subframe is associated with a first subframe type and the second subframe is associated with a second subframe type;\nreceive, from the second node, a first signal quality report indicating a third signal quality measurement that is a combination of a first signal quality measurement weighted by a percentage of the frame that includes subframes of the first subframe type and a second signal quality measurement weighted by a percentage of the frame that includes subframes of the second subframe type; and\nschedule a data transmission in at least one of the first subframe and the second subframe, the scheduled data transmission being associated with the third signal quality measurement.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00029",
            "claim_text": "29. The apparatus of claim 28, wherein, to schedule the data transmission in at least one of the first subframe and the second subframe, the one or more memories are executable by the one or more processors individually or collectively to cause the apparatus to:\nschedule a first data transmission in the first subframe, the scheduled first transmission being associated with the first signal quality measurement; and\nschedule a second data transmission in the second subframe, the scheduled second transmission being associated with the second signal quality measurement,\nwherein the first signal quality report further indicates at least one of the first signal quality measurement and the second signal quality measurement.",
            "claim_type": "dependent",
            "dependency": "claim 28",
            "is_exemplary": true
          },
          {
            "claim_number": "00030",
            "claim_text": "30. The apparatus of claim 28, wherein, to receive the first signal quality report indicating the third signal quality measurement, the one or more processor-readable instructions are executable by the one or more processors individually or collectively to cause the apparatus to:\nreceive the first signal quality report indicating the third signal quality measurement periodically according to a time interval.",
            "claim_type": "dependent",
            "dependency": "claim 28",
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.8,
        "publication_date": "2024-06-04",
        "patent_year": 2024
      },
      {
        "patent_id": "11943630",
        "title": "Enhancements for multiple radio protocol dynamic spectrum sharing",
        "abstract": "Methods, systems, and devices for wireless communications are described. Some wireless communications systems may support dynamic spectrum sharing for multiple radio protocols, such as New Radio and Long Term Evolution. Systems may implement a number of techniques to improve spectrum use by user equipment in dynamically shared frequency spectrums. In some aspects, the network may assign a user equipment to a specific bandwidth part based on a rate matching capability of the user equipment. Additionally or alternatively, the network may activate a specific bandwidth part based on the frequency of handover for a user equipment. In some aspects, the network may support dual registration (e.g., registration in a same frequency spectrum using different radio protocols) for a user equipment operating on a dynamically shared spectrum. To reduce the control overhead for such a user equipment, the network may use a single control channel to schedule data for multiple radio protocols.",
        "inventors": [
          "Akash Kumar"
        ],
        "assignees": [
          "QUALCOMM Incorporated"
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. A method for wireless communications implemented by a user equipment (UE), comprising:\nregistering, with a network entity, on a first cell supporting a first radio access technology in a frequency spectrum;\nregistering, with the network entity, on a second cell supporting a second radio access technology different from the first radio access technology and at least partially overlapping with the first cell in the frequency spectrum based at least in part on the network entity supporting dynamic sharing of the frequency spectrum between the first radio access technology and the second radio access technology;\nreceiving, via a control channel for the first radio access technology, a control message indicating a first set of resources in the frequency spectrum for communications using the first radio access technology and a second set of resources in the frequency spectrum for communications using the second radio access technology, wherein the first set of resources and the second set of resources are multiplexed according to a time division multiplexing scheme; and\ncommunicating with the network entity based at least in part on the registering on the first cell supporting the first radio access technology and the registering on the second cell supporting the second radio access technology.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The method of claim 1, further comprising:\nreceiving a cell identifier for the first cell, wherein the cell identifier indicates that the network entity supports the dynamic sharing of the frequency spectrum between the first radio access technology and the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The method of claim 1, wherein the communicating comprises:\nperforming data communications on the first cell using the first radio access technology; and\nperforming, at least partially concurrent to the performing the data communications, voice communications on the second cell using the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The method of claim 1, further comprising:\nestablishing a first radio bearer for the communicating with the network entity using the first radio access technology and a second radio bearer for the communicating with the network entity using the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The method of claim 1, further comprising:\ncaching, in local memory at the UE, an indication that the network entity supports the dynamic sharing of the frequency spectrum between the first radio access technology and the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. The method of claim 1, wherein the control message is received on a primary carrier corresponding to the first radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The method of claim 1, further comprising:\nusing a single radio frequency transceiver to receive the first set of resources and the second set of resources.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The method of claim 1, wherein the registering on the first cell supporting the first radio access technology and the registering on the second cell supporting the second radio access technology comprise a dual registration procedure.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. The method of claim 1, further comprising:\ndisplaying, in a user interface of the UE, an icon indicating that the UE supports the dynamic sharing of the frequency spectrum between the first radio access technology and the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. The method of claim 1, wherein the communicating comprises:\ncommunicating with the network entity on a first carrier using the first radio access technology based at least in part on the registering on the first cell supporting the first radio access technology; and\ncommunicating with the network entity on a second carrier using the second radio access technology based at least in part on the registering on the second cell supporting the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. The method of claim 10, wherein the first carrier and the second carrier are a same carrier.",
            "claim_type": "dependent",
            "dependency": "claim 10",
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. The method of claim 1, wherein:\nthe first radio access technology comprises a fifth generation radio technology; and\nthe second radio access technology comprises a long term evolution technology.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. A method for wireless communications implemented by a network entity, comprising:\nconfiguring a frequency spectrum for dynamic sharing between a first radio access technology and a second radio access technology;\nregistering a user equipment (UE) on a first cell supporting the first radio access technology in the frequency spectrum;\nregistering the UE on a second cell supporting the second radio access technology different from the first radio access technology and at least partially overlapping with the first cell in the frequency spectrum based at least in part on the configuring;\ntransmitting, via a control channel for the first radio access technology, a control message indicating a first set of resources in the frequency spectrum for communications using the first radio access technology and a second set of resources in the frequency spectrum for communications using the second radio access technology, wherein the first set of resources and the second set of resources are multiplexed according to a time division multiplexing scheme; and\ncommunicating with the UE based at least in part on the registering the UE on the first cell supporting the first radio access technology and the registering the UE on the second cell supporting the second radio access technology.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. The method of claim 13, further comprising:\ntransmitting a cell identifier for the first cell, the second cell, or both, wherein the cell identifier is associated with support of the dynamic sharing between the first radio access technology and the second radio access technology, wherein the registering the UE on the second cell supporting the second radio access technology is based at least in part on the cell identifier.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00015",
            "claim_text": "15. The method of claim 13, wherein the communicating comprises:\nperforming data communications on the first cell using the first radio access technology; and\nperforming, at least partially concurrent to the performing the data communications, voice communications on the second cell using the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00016",
            "claim_text": "16. The method of claim 15, further comprising:\ndirecting traffic associated with the voice communications to the second radio access technology based at least in part on the second radio access technology supporting a threshold quality of service for the voice communications.",
            "claim_type": "dependent",
            "dependency": "claim 15",
            "is_exemplary": true
          },
          {
            "claim_number": "00017",
            "claim_text": "17. The method of claim 15, further comprising:\nmaintaining data connectivity using the first radio access technology during the performing the voice communications using the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 15",
            "is_exemplary": true
          },
          {
            "claim_number": "00018",
            "claim_text": "18. The method of claim 13, wherein the registering the UE on the first cell supporting the first radio access technology and the registering the UE on the second cell supporting the second radio access technology comprise a dual registration procedure for the UE.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00019",
            "claim_text": "19. The method of claim 13, wherein the communicating comprises:\ncommunicating with the UE on a first carrier using the first radio access technology based at least in part on the registering the UE on the first cell supporting the first radio access technology; and\ncommunicating with the UE on a second carrier using the second radio access technology based at least in part on the registering the UE on the second cell supporting the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00020",
            "claim_text": "20. The method of claim 19, wherein the first carrier and the second carrier are a same carrier.",
            "claim_type": "dependent",
            "dependency": "claim 19",
            "is_exemplary": true
          },
          {
            "claim_number": "00021",
            "claim_text": "21. The method of claim 13, wherein:\nthe first radio access technology comprises a fifth generation radio technology; and\nthe second radio access technology comprises a long term evolution technology.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00022",
            "claim_text": "22. An apparatus for wireless communications implemented by a user equipment (UE), comprising:\na processor;\nmemory coupled with the processor; and\ninstructions stored in the memory and executable by the processor to cause the apparatus to:\nregister, with a network entity, on a first cell supporting a first radio access technology in a frequency spectrum;\nregister, with the network entity, on a second cell supporting a second radio access technology different from the first radio access technology and at least partially overlapping with the first cell in the frequency spectrum based at least in part on the network entity supporting dynamic sharing of the frequency spectrum between the first radio access technology and the second radio access technology;\nreceive, via a control channel for the first radio access technology, a control message indicating a first set of resources in the frequency spectrum for communications using the first radio access technology and a second set of resources in the frequency spectrum for communications using the second radio access technology, wherein the first set of resources and the second set of resources are multiplexed according to a time division multiplexing scheme; and\ncommunicate with the network entity based at least in part on the registering on the first cell supporting the first radio access technology and the registering on the second cell supporting the second radio access technology.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00023",
            "claim_text": "23. The apparatus of claim 22, wherein the instructions are further executable by the processor to cause the apparatus to receive a cell identifier for the first cell, wherein the cell identifier indicates that the network entity supports the dynamic sharing of the frequency spectrum between the first radio access technology and the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 22",
            "is_exemplary": true
          },
          {
            "claim_number": "00024",
            "claim_text": "24. The apparatus of claim 22, wherein the instructions to communicate are further executable by the processor to cause the apparatus to:\nperform data communications on the first cell using the first radio access technology; and\nperform, at least partially concurrent to the performing the data communications, voice communications on the second cell using the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 22",
            "is_exemplary": true
          },
          {
            "claim_number": "00025",
            "claim_text": "25. The apparatus of claim 22, wherein the instructions are further executable by the processor to cause the apparatus to cache, in local memory at the UE, an indication that the network entity supports the dynamic sharing of the frequency spectrum between the first radio access technology and the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 22",
            "is_exemplary": true
          },
          {
            "claim_number": "00026",
            "claim_text": "26. An apparatus for wireless communications implemented by a network entity, comprising:\na processor;\nmemory coupled with the processor; and\ninstructions stored in the memory and executable by the processor to cause the apparatus to:\nconfigure a frequency spectrum for dynamic sharing between a first radio access technology and a second radio access technology;\nregister a user equipment (UE) on a first cell supporting the first radio access technology in the frequency spectrum;\nregister the UE on a second cell supporting the second radio access technology different from the first radio access technology and at least partially overlapping with the first cell in the frequency spectrum based at least in part on the configuring;\ntransmit, via a control channel for the first radio access technology, a control message indicating a first set of resources in the frequency spectrum for communications using the first radio access technology and a second set of resources in the frequency spectrum for communications using the second radio access technology, wherein the first set of resources and the second set of resources are multiplexed according to a time division multiplexing scheme; and\ncommunicate with the UE based at least in part on the registering the UE on the first cell supporting the first radio access technology and the registering the UE on the second cell supporting the second radio access technology.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00027",
            "claim_text": "27. The apparatus of claim 26, wherein the instructions are further executable by the processor to cause the apparatus to transmit a cell identifier for the first cell, the second cell, or both, wherein the cell identifier is associated with support of the dynamic sharing between the first radio access technology and the second radio access technology, wherein the registering the UE on the second cell supporting the second radio access technology is based at least in part on the cell identifier.",
            "claim_type": "dependent",
            "dependency": "claim 26",
            "is_exemplary": true
          },
          {
            "claim_number": "00028",
            "claim_text": "28. The apparatus of claim 26, wherein the instructions to communicate are further executable by the processor to cause the apparatus to:\nperform data communications on the first cell using the first radio access technology; and\nperform, at least partially concurrent to the performing the data communications, voice communications on the second cell using the second radio access technology.",
            "claim_type": "dependent",
            "dependency": "claim 26",
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.8,
        "publication_date": "2024-03-26",
        "patent_year": 2024
      },
      {
        "patent_id": "11490381",
        "title": "Systems and methods for dynamic spectrum sharing (\u201cDSS\u201d) interleaving and pre-scheduling to optimize resource utilization",
        "abstract": "A system described herein may provide a scheduling technique for physical radio frequency (\u201cRF\u201d) resources of a base station of a radio access network (\u201cRAN\u201d) of a wireless network. Resources for a first group of User Equipment (\u201cUEs\u201d) may be allocated during or prior to a first time slot, and the UEs may be notified during the first time slot of the allocated resources. The allocated resources may be provided during a subsequent second time slot. A second group of UEs may be notified, during the first time slot, of physical RF resources allocated for downlink data for the second group of resources, and such downlink data may be provided to the second group of UEs during the first time slot via the allocated physical RF resources. The assignments of the UEs to the respective groups may change over time based on network load or other metrics.",
        "inventors": [
          "Xin Wang",
          "Susan Wu Sanders",
          "Nischal Patel",
          "Monte Giles"
        ],
        "assignees": [
          "Verizon Patent and Licensing Inc."
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. A device, comprising:\none or more processors configured to:\nreceive a request to allocate, for a User Equipment (\u201cUE\u201d), physical downlink radio frequency (\u201cRF\u201d) resources of a base station associated with a radio access network (\u201cRAN\u201d) of a wireless network;\nallocate, based on the request, a first set of downlink Physical Resource Blocks (\u201cPRBs\u201d) at a first time slot to indicate, to the UE, a second set of downlink PRBs, at a subsequent second time slot, that will be used to provide downlink data to the UE,\nwherein the first and second time slots are each subdivided into a plurality of symbols, and wherein allocating the first set of PRBs includes allocating the first set of PRBs at a last symbol of the plurality of symbols of the first time slot; and\n\nallocate, at the second subsequent time slot, the second set of downlink PRBs to provide the downlink data to the UE.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The device of claim 1, wherein the plurality of symbols consist of fourteen symbols, and wherein the last symbol is a fourteenth symbol of the fourteen symbols of the first time slot.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The device of claim 2, wherein allocating the second set of downlink PRBs includes allocating PRBs on symbols other than the first, second, third and fourteenth symbols of the fourteen symbols of the second time slot for the downlink data for the UE.",
            "claim_type": "dependent",
            "dependency": "claim 2",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. A device, comprising:\none or more processors configured to:\nreceive a first request to allocate, for a first User Equipment (\u201cUE\u201d), physical downlink radio frequency (\u201cRF\u201d) resources of a base station associated with a radio access network (\u201cRAN\u201d) of a wireless network;\nallocate, based on the first request, a first set of downlink Physical Resource Blocks (\u201cPRBs\u201d) at a first time slot to indicate, to the first UE, a second set of downlink PRBs, at a subsequent second time slot, that will be used to provide downlink data to the first UE;\nallocate, at the second subsequent time slot, the second set of downlink PRBs to provide the downlink data to the first UE;\nreceive a second request to allocate, for a second UE, physical downlink RF resources of the base station;\nallocate, based on the second request, a third set of PRBs at the first time slot to indicate, to the second UE, a fourth set of downlink PRBs, at the first time slot, that will be used to provide downlink data to the second UE; and\nallocate, at the first time slot, the fourth set of downlink PRBs to provide the downlink data to the second UE.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The device of claim 4, wherein the allocated first set of PRBs correspond to a Physical Downlink Control Channel (\u201cPDCCH\u201d), and wherein the allocated second set of PRBs correspond to a Physical Downlink Shared Channel (\u201cPDSCH\u201d).",
            "claim_type": "dependent",
            "dependency": "claim 4",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. A device, comprising:\none or more processors configured to:\nreceive a first request to allocate, for a first User Equipment (\u201cUE\u201d), physical downlink radio frequency (\u201cRF\u201d) resources of a base station associated with a radio access network (\u201cRAN\u201d) of a wireless network;\nallocate, based on the first request, a first set of downlink Physical Resource Blocks (\u201cPRBs\u201d) at a first time slot to indicate, to the first UE, a second set of downlink PRBs, at a subsequent second time slot, that will be used to provide downlink data to the first UE;\nallocate, at the second subsequent time slot, the second set of downlink PRBs to provide the downlink data to the first UE;\nidentify a second request, pending during the second time slot, to allocate physical RF resources for a second UE;\nallocate, based on the second request, a third set of PRBs at the second time slot to indicate, to the second UE, a fourth set of downlink PRBs, at the second time slot, that will be used to provide downlink data to the second UE; and\nallocate, at the second time slot, the fourth set of downlink PRBs to provide the downlink data to the second UE.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The device of claim 6, wherein allocating the second set of downlink PRBs includes allocating PRBs on symbols other than first and last symbols of the second time slot for the downlink data for the first UE.",
            "claim_type": "dependent",
            "dependency": "claim 6",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The device of claim 6, wherein the allocated first set of PRBs correspond to a Physical Downlink Control Channel (\u201cPDCCH\u201d), and wherein the allocated second set of PRBs correspond to a Physical Downlink Shared Channel (\u201cPDSCH\u201d).",
            "claim_type": "dependent",
            "dependency": "claim 6",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. A non-transitory computer-readable medium, storing a plurality of processor-executable instructions to:\nreceive a request to allocate, for a User Equipment (\u201cUE\u201d), physical downlink radio frequency (\u201cRF\u201d) resources of a base station associated with a radio access network (\u201cRAN\u201d) of a wireless network;\nallocate, based on the request, a first set of downlink Physical Resource Blocks (\u201cPRBs\u201d) at a first time slot to indicate, to the UE, a second set of downlink PRBs, at a subsequent second time slot, that will be used to provide downlink data to the UE,\nwherein the first and second time slots are each subdivided into a plurality of symbols, and wherein allocating the first set of PRBs includes allocating the first set of PRBs at a last symbol of the plurality of symbols of the first time slot; and\n\nallocate, at the second subsequent time slot, the second set of downlink PRBs to provide the downlink data to the UE.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. The non-transitory computer-readable medium of claim 9, wherein the plurality of symbols consist of fourteen symbols, and wherein the last symbol is a fourteenth symbol of the fourteen symbols of the first time slot.",
            "claim_type": "dependent",
            "dependency": "claim 9",
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. The non-transitory computer-readable medium of claim 10, wherein allocating the second set of downlink PRBs includes allocating PRBs on symbols other than the first, second, third and fourteenth symbols of the fourteen symbols of the second time slot for the downlink data for the UE.",
            "claim_type": "dependent",
            "dependency": "claim 10",
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. The non-transitory computer-readable medium of claim 9, wherein the allocated first set of PRBs correspond to a Physical Downlink Control Channel (\u201cPDCCH\u201d), and wherein the allocated second set of PRBs correspond to a Physical Downlink Shared Channel (\u201cPDSCH\u201d).",
            "claim_type": "dependent",
            "dependency": "claim 9",
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. The non-transitory computer-readable medium of claim 9, wherein the UE is a first UE, wherein the request is a first request, wherein the plurality of processor-executable instructions further include processor-executable instructions to:\nreceive a second request to allocate, for a second UE, physical downlink RF resources of the base station;\nallocate, based on the second request, a third set of PRBs at the first time slot to indicate, to the second UE, a fourth set of downlink PRBs, at the first time slot, that will be used to provide downlink data to the second UE; and\nallocate, at the first time slot, the fourth set of downlink PRBs to provide the downlink data to the second UE.",
            "claim_type": "dependent",
            "dependency": "claim 9",
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. The non-transitory computer-readable medium of claim 9, wherein the request is a first request, wherein the UE is a first UE, wherein the plurality of processor-executable instructions further include processor-executable instructions to:\nidentify a second request, pending during the second time slot, to allocate physical RF resources for a second UE;\nallocate, based on the second request, a third set of PRBs at the second time slot to indicate, to the second UE, a fourth set of downlink PRBs, at the second time slot, that will be used to provide downlink data to the second UE; and\nallocate, at the second time slot, the fourth set of downlink PRBs to provide the downlink data to the second UE.",
            "claim_type": "dependent",
            "dependency": "claim 9",
            "is_exemplary": true
          },
          {
            "claim_number": "00015",
            "claim_text": "15. A method, comprising:\nreceiving a first request to allocate, a first User Equipment (\u201cUE\u201d), physical downlink radio frequency (\u201cRF\u201d) resources of a base station associated with a radio access network (\u201cRAN\u201d) of a wireless network;\nallocating, based on the first request, a first set of downlink Physical Resource Blocks (\u201cPRBs\u201d) at a first time slot to indicate, to the first UE, a second set of downlink PRBs, at a subsequent second time slot, that will be used to provide downlink data to the first UE;\nallocating, at the second subsequent time slot, the second set of downlink PRBs to provide the downlink data to the UE;\nreceiving a second request to allocate, for a second UE, physical downlink RF resources of the base station;\nallocating, based on the second request, a third set of PRBs at the first time slot to indicate, to the second UE, a fourth set of downlink PRBs, at the first time slot, that will be used to provide downlink data to the second UE; and\nallocating, at the first time slot, the fourth set of downlink PRBs to provide the downlink data to the second UE.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00016",
            "claim_text": "16. The method of claim 15, wherein the first and second time slots are each subdivided into a fourteen symbols, wherein allocating the first set of PRBs includes allocating the first set of PRBs at a fourteenth symbol of the first time slot.",
            "claim_type": "dependent",
            "dependency": "claim 15",
            "is_exemplary": true
          },
          {
            "claim_number": "00017",
            "claim_text": "17. The method of claim 16, wherein allocating the second set of downlink PRBs includes allocating PRBs on symbols other than the first, second, third and fourteenth symbols of the fourteen symbols of the second time slot for the downlink data for the first UE.",
            "claim_type": "dependent",
            "dependency": "claim 16",
            "is_exemplary": true
          },
          {
            "claim_number": "00018",
            "claim_text": "18. A method, comprising:\nreceiving a first request to allocate, for a first User Equipment (\u201cUE\u201d), physical downlink radio frequency (\u201cRF\u201d) resources of a base station associated with a radio access network (\u201cRAN\u201d) of a wireless network;\nallocating, based on the first request, a first set of downlink Physical Resource Blocks (\u201cPRBs\u201d) at a first time slot to indicate, to the first UE, a second set of downlink PRBs, at a subsequent second time slot, that will be used to provide downlink data to the first UE;\nallocating, at the second subsequent time slot, the second set of downlink PRBs to provide the downlink data to the first UE;\nidentifying a second request, pending during the second time slot, to allocate physical RF resources for a second UE;\nallocating, based on the second request, a third set of PRBs at the second time slot to indicate, to the second UE, a fourth set of downlink PRBs, at the second time slot, that will be used to provide downlink data to the second UE; and\nallocating, at the second time slot, the fourth set of downlink PRBs to provide the downlink data to the second UE.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00019",
            "claim_text": "19. The method of claim 18, wherein the allocated first set of PRBs correspond to a Physical Downlink Control Channel (\u201cPDCCH\u201d), and wherein the allocated second set of PRBs correspond to a Physical Downlink Shared Channel (\u201cPDSCH\u201d).",
            "claim_type": "dependent",
            "dependency": "claim 18",
            "is_exemplary": true
          },
          {
            "claim_number": "00020",
            "claim_text": "20. The method of claim 18, wherein allocating the second set of downlink PRBs includes allocating PRBs on symbols other than first and last symbols of the second time slot for the downlink data for the first UE.",
            "claim_type": "dependent",
            "dependency": "claim 18",
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.7,
        "publication_date": "2022-11-01",
        "patent_year": 2022
      },
      {
        "patent_id": "11259263",
        "title": "Dual registration using dynamic spectrum sharing (DSS) in a wide area network (WAN)",
        "abstract": "This disclosure provides systems, methods, and apparatus, including computer programs encoded on computer-readable media, for implementing a dual registration mode and a dual receive mode using a single radio for wireless communications. A UE may determine that a wireless communication network supports the dual registration mode and dynamic spectrum sharing (DSS). The UE may establish a first connection with a first base station using a first radio access technology (RAT) of the wireless communication network. The UE may determine, based on one or more parameters associated with the DSS, that a second RAT of the wireless communication network has a second operating frequency band that overlaps a first operating frequency band of the first RAT. The UE may establish, via the second operating frequency band, a second connection with a second base station using the second RAT based on the dual registration mode and the DSS.",
        "inventors": [
          "Mohammad Suhel Ashfaque",
          "Avinash Dubey",
          "None Sagar"
        ],
        "assignees": [
          "QUALCOMM Incorporated"
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. A method performed by an apparatus of a user equipment (UE) for wireless communication in a dual receive mode using a single radio, comprising: determining that a wireless communication network supports a dual registration mode and dynamic spectrum sharing (DSS); establishing a first connection with a first base station using a first radio access technology (RAT) of the wireless communication network, the first RAT using a first operating frequency band; determining, based on one or more parameters associated with the DSS, that a second RAT of the wireless communication network has a second operating frequency band that overlaps the first operating frequency band of the first RAT; and establishing, via the second operating frequency band, a second connection with a second base station using the second RAT based on the dual registration mode and the DSS.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The method of claim 1 , wherein the first RAT is a 5G New Radio (NR) network and the second RAT is a long term evolution (LTE) network.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The method of claim 1 , further comprising: operating in the dual receive mode, a dual standby mode, and the dual registration mode using the single radio for wireless communications via the first connection using the first RAT and the second connection using the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The method of claim 1 , further comprising: receiving a registration message from the first base station, the registration message indicating that the wireless communication network supports the dual registration mode.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The method of claim 4 , wherein the registration message is a registration accept message, the registration accept message including a dual registration indication that indicates the wireless communication network supports the dual registration mode.",
            "claim_type": "dependent",
            "dependency": "claim 4",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. The method of claim 1 , wherein determining that the wireless communication network supports the DSS comprises: receiving the one or more parameters associated with the DSS from the first base station, the one or more parameters including a rate matching parameter that indicates the wireless communication network supports the DSS.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The method of claim 6 , wherein the rate matching parameter is an LTE cell-specific reference signal (CRS) rate matching parameter that indicates the wireless communication network supports the DSS and indicates the second operating frequency band of the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 6",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The method of claim 6 , wherein establishing the second connection with the second base station using the second RAT based on the dual registration mode and the DSS comprises: determining the second operating frequency band and a center frequency of the second operating frequency band based on the rate matching parameter; and searching for the center frequency of the second operating frequency band for establishing the second connection.",
            "claim_type": "dependent",
            "dependency": "claim 6",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. The method of claim 1 , further comprising: operating in an idle mode or a connected mode for the first connection that uses the first RAT; and operating in an idle mode for the second connection that uses the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. The method of claim 1 , further comprising: receiving a first communication associated with the first RAT from the first base station via the first connection having the first operating frequency band; receiving a second communication associated with the second RAT from the second base station via the second connection having the second operating frequency band; processing the first communication using a first processing unit associated with the first RAT; and processing the second communication using a second processing unit associated with the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. The method of claim 10 , further comprising: operating in an idle mode or a connected mode for the first connection that uses the first RAT; operating in an idle mode for the second connection that uses the second RAT; and receiving the second communication associated with the second RAT without performing a tuneaway operation.",
            "claim_type": "dependent",
            "dependency": "claim 10",
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. The method of claim 10 , further comprising: operating in an idle mode or a connected mode for the first connection that uses the first RAT; operating in an idle mode for the second connection that uses the second RAT; and receiving the first communication associated with the first RAT concurrently with the second communication associated with the second RAT without performing a tuneaway operation.",
            "claim_type": "dependent",
            "dependency": "claim 10",
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. The method of claim 10 , wherein the first RAT is a 5G New Radio (NR) network and the second RAT is a long term evolution (LTE) network, further comprising: operating in an idle mode or a connected mode for the first connection that uses the 5G NR network; operating in an idle mode for the second connection that uses the LTE network; and determining the second communication is an LTE page signal or an LTE cell-specific reference signal (CRS).",
            "claim_type": "dependent",
            "dependency": "claim 10",
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. An apparatus of a user equipment (UE) for wireless communication, comprising: an interface; and one or more processors, which together with the interface, are configured to: determine that a wireless communication network supports a dual registration mode and dynamic spectrum sharing (DSS); establish a first connection with a first base station using a first radio access technology (RAT) of the wireless communication network, the first RAT using a first operating frequency band; determine, based on one or more parameters associated with the DSS, that a second RAT of the wireless communication network has a second operating frequency band that overlaps the first operating frequency band of the first RAT; and establish a second connection with a second base station using the second RAT based on the dual registration mode and the DSS, the second RAT using the second operating frequency band.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00015",
            "claim_text": "15. The apparatus of claim 14 , wherein the interface includes a single radio, and the apparatus is configured to operate in a dual receive mode, a dual standby mode, and the dual registration mode using the single radio for wireless communications via the first connection using the first RAT and the second connection using the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00016",
            "claim_text": "16. The apparatus of claim 14 , wherein the first RAT is a 5G New Radio (NR) network and the second RAT is a long term evolution (LTE) network.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00017",
            "claim_text": "17. The apparatus of claim 14 , wherein the one or more processors, together with the interface, are further configured to: receive a registration message from the first base station, the registration message indicating that the wireless communication network supports the dual registration mode.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00018",
            "claim_text": "18. The apparatus of claim 17 , wherein the registration message is a registration accept message, the registration accept message including a dual registration indication that indicates the wireless communication network supports the dual registration mode.",
            "claim_type": "dependent",
            "dependency": "claim 17",
            "is_exemplary": true
          },
          {
            "claim_number": "00019",
            "claim_text": "19. The apparatus of claim 14 , wherein the one or more processors, together with the interface, are further configured to: receive the one or more parameters associated with the DSS from the first base station, the one or more parameters including a rate matching parameter that indicates the wireless communication network supports the DSS.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00020",
            "claim_text": "20. The apparatus of claim 19 , wherein the rate matching parameter is an LTE cell-specific reference signal (CRS) rate matching parameter that indicates the wireless communication network supports the DSS and indicates the second operating frequency band of the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 19",
            "is_exemplary": true
          },
          {
            "claim_number": "00021",
            "claim_text": "21. The apparatus of claim 19 , wherein the one or more processors, together with the interface, are further configured to: determine the second operating frequency band and a center frequency of the second operating frequency band based on the rate matching parameter; and search for the center frequency of the second operating frequency band to establish the second connection.",
            "claim_type": "dependent",
            "dependency": "claim 19",
            "is_exemplary": true
          },
          {
            "claim_number": "00022",
            "claim_text": "22. The apparatus of claim 14 , wherein the one or more processors, together with the interface, are further configured to: operate in an idle mode or a connected mode for the first connection that uses the first RAT; and operate in an idle mode for the second connection that uses the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00023",
            "claim_text": "23. The apparatus of claim 14 , wherein the one or more processors, together with the interface, are further configured to: receive a first communication associated with first RAT from the first base station via the first connection having the first operating frequency band; receive a second communication associated with the second RAT from the second base station via the second connection having the second operating frequency band; process the first communication associated with the first RAT; and process the second communication associated with the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 14",
            "is_exemplary": true
          },
          {
            "claim_number": "00024",
            "claim_text": "24. The apparatus of claim 23 , wherein the one or more processors, together with the interface, are further configured to: operate in an idle mode or a connected mode for the first connection that uses the first RAT; operate in an idle mode for the second connection that uses the second RAT; and receive the first communication associated with the first RAT concurrently with the second communication associated with the second RAT without performing a tuneaway operation.",
            "claim_type": "dependent",
            "dependency": "claim 23",
            "is_exemplary": true
          },
          {
            "claim_number": "00025",
            "claim_text": "25. An apparatus for wireless communication, comprising: means for determining that a wireless communication network supports a dual registration mode and dynamic spectrum sharing (DSS); means for establishing a first connection with a first base station using a first radio access technology (RAT) of the wireless communication network, the first RAT using a first operating frequency band; means for determining, based on one or more parameters associated with the DSS, that a second RAT of the wireless communication network has a second operating frequency band that overlaps the first operating frequency band of the first RAT; and means for establishing, via the second operating frequency band, a second connection with a second base station using the second RAT based on the dual registration mode and the DSS.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00026",
            "claim_text": "26. The apparatus of claim 25 , further comprising: means for operating in a dual receive mode, a dual standby mode, and the dual registration mode using a single radio for wireless communications via the first connection using the first RAT and the second connection using the second RAT and without performing tuneaway operations.",
            "claim_type": "dependent",
            "dependency": "claim 25",
            "is_exemplary": true
          },
          {
            "claim_number": "00027",
            "claim_text": "27. The apparatus of claim 25 , further comprising: means for receiving a registration message from the first base station, the registration message indicating that the wireless communication network supports the dual registration mode.",
            "claim_type": "dependent",
            "dependency": "claim 25",
            "is_exemplary": true
          },
          {
            "claim_number": "00028",
            "claim_text": "28. The apparatus of claim 25 , further comprising: means for receiving the one or more parameters associated with the DSS from the first base station, the one or more parameters including a rate matching parameter that indicates the wireless communication network supports the DSS.",
            "claim_type": "dependent",
            "dependency": "claim 25",
            "is_exemplary": true
          },
          {
            "claim_number": "00029",
            "claim_text": "29. A non-transitory computer-readable medium having stored therein instructions which, when executed by a processor of a user equipment (UE), cause the UE to: determine that a wireless communication network supports a dual registration mode and dynamic spectrum sharing (DSS); establish a first connection with a first base station using a first radio access technology (RAT) of the wireless communication network, the first RAT using a first operating frequency band; determine, based on one or more parameters associated with the DSS, that a second RAT of the wireless communication network has a second operating frequency band that overlaps the first operating frequency band of the first RAT; and establish, via the second operating frequency band, a second connection with a second base station using the second RAT based on the dual registration mode and the DSS.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00030",
            "claim_text": "30. The non-transitory computer-readable medium of claim 29 , wherein the instructions, when executed by the processor of the UE, further cause the UE to: operate in a dual receive mode, a dual standby mode, and the dual registration mode using a single radio for wireless communications via the first connection using the first RAT and the second connection using the second RAT.",
            "claim_type": "dependent",
            "dependency": "claim 29",
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.8,
        "publication_date": "2022-02-22",
        "patent_year": 2022
      },
      {
        "patent_id": "8892109",
        "title": "Method and apparatus of dynamic spectrum sharing in cellular networks",
        "abstract": "According to a disclosed method, an MME in a network analyzes KPIs from the cells it serves and based on the KPIs, it decides to engage in sharing. The MME then contacts a sharing entity (SE) to announce that it wants to supply spectrum for sharing. The MME obtains terms of a sharing agreement from the SE and the MME obtains the identity of the other network. In response to this information, the MME configures its base stations to support the supplying of spectrum to the other network. The SE applies knowledge of network topology and of services offered. This knowledge is obtained from a sharing database. At the expiration of the sharing agreement, the SE tells the MMEs to deactivate the sharing agreement.",
        "inventors": [
          "Jignesh S. Panchal",
          "Milind M. Buddhikot"
        ],
        "assignees": [
          "Alcatel Lucent"
        ],
        "claims": [],
        "relevance_score": 0.8,
        "publication_date": "2014-11-18",
        "patent_year": 2014
      },
      {
        "patent_id": "9538528",
        "title": "Efficient co-existence method for dynamic spectrum sharing",
        "abstract": "An apparatus defines a set of resources out of a first number of orthogonal radio resources and controls a transmitting means to simultaneously transmit a respective first radio signal for each resource on all resources of the set. A respective estimated interference is estimated on each of the resources of the set when the respective first radio signals are transmitted simultaneously. A first resource of the set is selected if the estimated interference on the first resource exceeds a first predefined level and, in the set, the first resource is replaced by a second resource of the first number of resources not having been part of the set. Each of the controlling and the estimating, the selecting, and the replacing is performed in order, respectively, for a predefined time.",
        "inventors": [
          "Istv\u00e1n Zsolt KOV\u00c1CS",
          "Andrea Cattoni",
          "Gustavo Wagner"
        ],
        "assignees": [
          "Nokia Solutions and Networks Oy"
        ],
        "claims": [],
        "relevance_score": 0.7,
        "publication_date": "2017-01-03",
        "patent_year": 2017
      }
    ],
    "search_strategies": [
      {
        "name": "5G Dynamic Spectrum Sharing Overview",
        "description": "This strategy targets patents that specifically mention both '5G' and 'dynamic spectrum sharing' to capture a broad overview of innovations in this area.",
        "query": {
          "_and": [
            {
              "_text_phrase": {
                "patent_title": "dynamic spectrum sharing"
              }
            },
            {
              "_text_phrase": {
                "patent_abstract": "5G"
              }
            }
          ]
        },
        "expected_results": 20,
        "priority": 1
      },
      {
        "name": "Technical Innovations in Dynamic Spectrum Sharing",
        "description": "This strategy focuses on patents that discuss dynamic spectrum sharing along with specific technical terms like 'OFDMA' and 'MIMO' to identify innovative methods and systems.",
        "query": {
          "_and": [
            {
              "_text_phrase": {
                "patent_abstract": "dynamic spectrum sharing"
              }
            },
            {
              "_text_any": {
                "patent_abstract": "OFDMA MIMO"
              }
            }
          ]
        },
        "expected_results": 15,
        "priority": 2
      },
      {
        "name": "5G Spectrum Management Techniques",
        "description": "This strategy aims to find patents that describe techniques for managing spectrum in 5G networks, focusing on the combination of dynamic spectrum sharing and interference management.",
        "query": {
          "_and": [
            {
              "_text_phrase": {
                "patent_title": "dynamic spectrum sharing"
              }
            },
            {
              "_text_any": {
                "patent_abstract": "interference management"
              }
            }
          ]
        },
        "expected_results": 18,
        "priority": 3
      },
      {
        "name": "5G Dynamic Spectrum Sharing Algorithms",
        "description": "This strategy targets patents that focus on algorithms related to dynamic spectrum sharing in 5G networks, ensuring the inclusion of specific algorithmic terms.",
        "query": {
          "_and": [
            {
              "_text_phrase": {
                "patent_abstract": "dynamic spectrum sharing"
              }
            },
            {
              "_text_any": {
                "patent_abstract": "algorithm optimization"
              }
            }
          ]
        },
        "expected_results": 12,
        "priority": 4
      },
      {
        "name": "5G Network Architecture for Spectrum Sharing",
        "description": "This strategy seeks patents that discuss the architectural aspects of 5G networks in relation to dynamic spectrum sharing, focusing on structural innovations.",
        "query": {
          "_and": [
            {
              "_text_phrase": {
                "patent_title": "dynamic spectrum sharing"
              }
            },
            {
              "_text_any": {
                "patent_abstract": "network architecture"
              }
            }
          ]
        },
        "expected_results": 10,
        "priority": 5
      }
    ],
    "timestamp": "2025-08-22T23:55:30.679362",
    "metadata": {
      "relevance_threshold": 0.3,
      "max_results": 20,
      "unique_patents_found": 30,
      "strategies_executed": 5
    }
  }
}
```

---
Generated by Direct Prior Art API Tester
