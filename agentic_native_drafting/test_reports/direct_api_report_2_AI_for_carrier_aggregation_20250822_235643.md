# Direct Prior Art API Test Report

## Test Information
- **Query**: AI for carrier aggregation
- **Test Index**: 2
- **Timestamp**: 2025-08-22T23:56:43.649467
- **Duration**: 69.9 seconds
- **Total Results**: 10
- **Backend URL**: http://localhost:8000

## Search Results Summary
Found 10 relevant patents

## Patent Analysis Report


## Raw API Response
```json
{
  "query": "AI for carrier aggregation",
  "total_results": 10,
  "results": [
    {
      "patent_id": "12113614",
      "title": "AIML positioning receiver for flexible carrier aggregation",
      "abstract": "An apparatus comprising circuitry configured to: receive a plurality of signal samples, wherein at least two of the signal samples are received on different carrier frequencies or over different durations; convert the plurality of signal samples to a common data format that stores as entries the samples, a stored entry corresponding to a sample measured with a carrier frequency, a time, and a receive antenna; generate entries of the common data format that are missing due to a sample not being measured with a carrier frequency, time, and receive antenna; wherein the entries of the common data format are ranked, wherein a higher ranking entry is considered more relevant than a relatively lower ranking entry; and generate at least one positioning measurement with a machine learning model, based on the entries of the common data format and the ranking of the entries of the common data format.",
      "inventors": [
        "Oana-Elena BARBU",
        "Sajad REZAIE"
      ],
      "assignees": [
        "Nokia Solutions and Networks Oy",
        "NOKIA TECHNOLOGIES OY"
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. An apparatus comprising:\nat least one processor; and\nat least one memory storing instructions that, when executed by the at least one processor, cause the apparatus at least to:\nreceive a plurality of signal samples, wherein at least two of the signal samples are received on different carrier frequencies, or wherein at least two of the signal samples are received over different durations;\nconvert the plurality of signal samples to a common data format that stores as entries the plurality of signal samples, a stored entry corresponding to a signal sample measured with a carrier frequency, a time, and a receive antenna;\ngenerate entries of the common data format that are missing due to a signal sample not being measured with a carrier frequency, time, and receive antenna;\nwherein the entries of the common data format are ranked, wherein a higher ranking entry is considered more relevant than a relatively lower ranking entry; and\ngenerate at least one positioning measurement with a machine learning model, based on the entries of the common data format and the ranking of the entries of the common data format.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The apparatus of claim 1, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\ngenerate the entries of the common data format that are missing with accounting for:\na frequency, time, and space selectivity of a channel response, and\nan identifier of a transmitter of the signal samples.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The apparatus of claim 1, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\nestimate a channel response between a respective network node that transmits at least a portion of the signal samples and a respective receive antenna, at resource elements of the common data format; and\ngenerate the entries of the common data format that are missing based on the respective estimated channel response.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The apparatus of claim 3, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\nestimate the channel response using linear mean squared error estimation given a respective signal vector at a respective receive antenna; or\ntrain a machine learning channel estimation model with a dataset comprising measured channel responses and unmeasured channel responses, the labels of the dataset comprising the measured channel responses, and estimate the channel response using the machine learning channel estimation model.",
          "claim_type": "dependent",
          "dependency": "claim 3",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The apparatus of claim 1, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\ndiscard or set to zero at least one entry of the common data format corresponding to an unused resource; or\nreshape the common data format to be of a size of the machine learning model used to generate the at least one positioning measurement.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. The apparatus of claim 1, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\nrank the entries of the common data format based on at least one of: a noise level of a resource element corresponding to an entry, or an interference level of the resource element corresponding to the entry.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The apparatus of claim 1, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\nrank the entries of the common data format using a data structure;\nwherein at least one entry within the data structure corresponds to a weight of a carrier frequency, wherein a first weight of a first carrier frequency is ranked higher than a second weight of a second carrier frequency when the first carrier frequency has over a period of time provided a more accurate positioning accuracy than the second carrier frequency;\nwherein at least one entry within the data structure corresponds to a weight of an orthogonal frequency division multiplexing symbol.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The apparatus of claim 1, wherein the at least one positioning measurement comprises at least one of:\na location of a user equipment,\ncoordinates of a location of a user equipment,\na line of sight indicator,\na non-line of sight indicator,\na set of mappings between a respective line of sight and a respective signal source, or\na combination of at least two of a location of a user equipment, coordinates of a location of a user equipment, a line of sight indicator, a non-line of sight indicator, or a set of mappings between a respective line of sight and a respective signal source.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. The apparatus of claim 1, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\ntrain the machine learning model using a loss function based on a mean squared error of a location of a user equipment and a cross entropy of a line of sight.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. The apparatus of claim 1, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\nin response to the at least one positioning measurement not being within a range given with at least one first threshold expected positioning measurement and at least one second threshold expected positioning measurement, modify the ranking of the entries of the common data format, and regenerate the at least one positioning measurement with the machine learning model based on the entries of the common data format and the modified ranking of the entries of the common data format.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. An apparatus comprising:\nat least one processor; and\nat least one memory storing instructions that, when executed by the at least one processor, cause the apparatus at least to:\nreceive a plurality of signal samples, wherein at least two of the signal samples are received with different resource elements;\nconvert the plurality of signal samples to a common data format that stores as entries the plurality of signal samples, a stored entry corresponding to a signal sample measured with a resource element;\ngenerate entries of the common data format that are missing due to a signal sample not being measured with a resource element;\nwherein the entries of the common data format are ranked, wherein a higher ranking entry is considered more relevant than a relatively lower ranking entry; and\ngenerate at least one positioning measurement with a machine learning model, based on the entries of the common data format and the ranking of the entries of the common data format.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. The apparatus of claim 11, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\ngenerate the entries of the common data format that are missing with accounting for:\na frequency, time, and space selectivity of a channel response, and\nan identifier of a transmitter of the signal samples.",
          "claim_type": "dependent",
          "dependency": "claim 11",
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. The apparatus of claim 11, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\nestimate a channel response between a respective network node that transmits at least a portion of the signal samples and a respective receive antenna, at resource elements of the common data format; and\ngenerate the entries of the common data format that are missing based on the respective estimated channel response.",
          "claim_type": "dependent",
          "dependency": "claim 11",
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. The apparatus of claim 11, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\nrank the entries of the common data format based on at least one of: a noise level of a resource element corresponding to an entry, or an interference level of the resource element corresponding to the entry.",
          "claim_type": "dependent",
          "dependency": "claim 11",
          "is_exemplary": true
        },
        {
          "claim_number": "00015",
          "claim_text": "15. The apparatus of claim 11, wherein the at least one positioning measurement comprises at least one of:\na location of a user equipment,\ncoordinates of a location of a user equipment,\na line of sight indicator,\na non-line of sight indicator,\na set of mappings between a respective line of sight and a respective signal source, or\na combination of at least two of a location of a user equipment, coordinates of a location of a user equipment, a line of sight indicator, a non-line of sight indicator, or a set of mappings between a respective line of sight and a respective signal source.",
          "claim_type": "dependent",
          "dependency": "claim 11",
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.8,
      "publication_date": "2024-10-08",
      "patent_year": 2024
    },
    {
      "patent_id": "9736741",
      "title": "Method, apparatus and system for cell handover in communication system supporting carrier aggregation",
      "abstract": "A method, apparatus and system for cell handover in the communication system supporting Carrier Aggregation (CA). The method includes: after receiving a performance measurement report for one or more neighboring cells from the served terminal, according to the performance measurement report, and basing on the CA mode for one or more candidate BSs corresponding to the one or more neighboring cells, a source Base Station (BS) in a communications system selects an algorithm suitable for the CA mode to calculate the priority levels of the one or more candidate BSs; from the one or more candidate BSs, selecting the BS having the highest priority as a target BS; and selecting one more cells to access from all cells being subject to the target BS in the one or more neighboring cells.",
      "inventors": [
        "Yuxin WEI"
      ],
      "assignees": [
        "SONY GROUP CORPORATION"
      ],
      "claims": [],
      "relevance_score": 0.8,
      "publication_date": "2017-08-15",
      "patent_year": 2017
    },
    {
      "patent_id": "9210637",
      "title": "Method, apparatus and system for cell handover in communication system supporting carrier aggregation",
      "abstract": "A method, apparatus and system for cell handover in the communication system supporting Carrier Aggregation (CA). The method includes: after receiving a performance measurement report for one or more neighboring cells from the served terminal, according to the performance measurement report, and basing on the CA mode for one or more candidate BSs corresponding to the one or more neighboring cells, a source Base Station (BS) in a communications system selects an algorithm suitable for the CA mode to calculate the priority levels of the one or more candidate BSs; from the one or more candidate BSs, selecting the BS having the highest priority as a target BS; and selecting one more cells to access from all cells being subject to the target BS in the one or more neighboring cells.",
      "inventors": [
        "Yuxin WEI"
      ],
      "assignees": [
        "SONY GROUP CORPORATION"
      ],
      "claims": [],
      "relevance_score": 0.8,
      "publication_date": "2015-12-08",
      "patent_year": 2015
    },
    {
      "patent_id": "9025446",
      "title": "Carrier selection policy for joint scheduling for carrier aggregation in an LTE-advanced system",
      "abstract": "Various embodiments of a semi-joint scheduling algorithm for carrier aggregation in an LTE-Advanced system are provided. The proposed semi-joint scheduling algorithm combines the advantages of independent scheduling and joint scheduling while avoiding the respective shortcomings, and provides a technical foundation for a wide adoption of the carrier aggregation technology. This Abstract is submitted with the understanding that it will not be used to interpret or limit the scope or meaning of the claims.",
      "inventors": [
        "Anpeng Huang"
      ],
      "assignees": [
        "Empire Technology Development LLC"
      ],
      "claims": [],
      "relevance_score": 0.8,
      "publication_date": "2015-05-05",
      "patent_year": 2015
    },
    {
      "patent_id": "10050761",
      "title": "System and method for user equipment initiated management of carrier aggregation",
      "abstract": "Methods that are performed by a user equipment (UE) and corresponding methods of base stations that allow a UE to determine whether the UE is in a carrier aggregation enabled or disabled state. One exemplary embodiment of a method performed by a UE determines a first artificial value for a first parameter and a second artificial value for a power headroom (PHR) for a secondary component carrier (SCC), the first and second artificial values being substantially low relative to a configuration of the network, generates an artificial report including the first and second artificial values, transmits the artificial report to a primary cell providing a primary component carrier (PCC) and receives an indication that the UE is placed in a carrier aggregation disabled state.",
      "inventors": [
        "Sarma V. Vangala",
        "Swaminathan Balakrishnan",
        "Tarik Tabet",
        "Rafael L. Rivera-Barreto",
        "Samy Khay-Ibbat",
        "Sree Ram Kodali"
      ],
      "assignees": [
        "Apple Inc."
      ],
      "claims": [],
      "relevance_score": 0.7,
      "publication_date": "2018-08-14",
      "patent_year": 2018
    },
    {
      "patent_id": "9479315",
      "title": "System and method for user equipment initiated management of carrier aggregation",
      "abstract": "Methods that are performed by a user equipment (UE) and corresponding methods of base stations that allow a UE to determine whether the UE is in a carrier aggregation enabled or disabled state. One exemplary embodiment of a method performed by a UE determines a first artificial value for a first parameter and a second artificial value for a power headroom (PHR) for a secondary component carrier (SCC), the first and second artificial values being substantially low relative to a configuration of the network, generates an artificial report including the first and second artificial values, transmits the artificial report to a primary cell providing a primary component carrier (PCC) and receives an indication that the UE is placed in a carrier aggregation disabled state.",
      "inventors": [
        "Sarma V. Vangala",
        "Swaminathan Balakrishnan",
        "Tarik Tabet",
        "Rafael L. Rivera-Barreto",
        "Samy Khay-Ibbat",
        "Sree Ram Kodali"
      ],
      "assignees": [
        "Apple Inc."
      ],
      "claims": [],
      "relevance_score": 0.7,
      "publication_date": "2016-10-25",
      "patent_year": 2016
    },
    {
      "patent_id": "11817986",
      "title": "Carrier aggregation peak to average power ratio reduction using peak reduction tones",
      "abstract": "Peak to average power ratio (PAPR) reduction with respect to signals of component carriers of a carrier aggregation configuration may be provided using preconfigured or fixed PRT location sequences (e.g., fixing the number and location of PRTs). A device transmitting signals of component carriers of a carrier aggregation configuration may perform PRT magnitude and phase optimization processing with respect to PRTs of a PRT location sequence using techniques, such as may use a signal to clipping noise ratio, tone reservation (SCR-TR) algorithm. Various PRT location sequence configurations, such as PRT sideband location sequence configurations, PRT inband location sequence configurations, etc., may be selected to facilitate reduction of PAPR associated with the data tones of one or more carrier aggregation component carriers, such as to satisfy a PAPR threshold. Other aspects and features are also claimed and described.",
      "inventors": [
        "Krishna Kiran Mukkavilli",
        "Wei Yang",
        "Gokul Sridharan",
        "Saeid SAHRAEI"
      ],
      "assignees": [
        "QUALCOMM Incorporated"
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. A method of wireless communication, comprising:\nreceiving, by a user equipment (UE), resource allocation indicating data tones and peak reduction tones (PRTs) with respect to each component carrier (CC) of a plurality of CCs, wherein the resource allocation indicates data tone locations within a first bandwidth of a first CC of the plurality of CCs and within a second bandwidth of a second CC of the plurality of CCs, and wherein the resource allocation indicates PRT locations within at least one of the first bandwidth or the second bandwidth according to one or more PRT location sequences; and\ntransmitting, by the UE, a data transmission comprising one or more waveforms configured according to the resource allocation.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The method of claim 1, wherein the one or more PRT location sequences provide a PRT sideband location configuration relative to data tones of the first CC, the second CC, or both.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The method of claim 1, wherein the one or more PRT location sequences include a first PRT location sequence of a plurality of contiguously located PRTs, and wherein the contiguously located PRTs of the first PRT location sequence are located within the first bandwidth of the first CC and are configured such that peak to average power ratio (PAPR) of a waveform of the one or more waveforms corresponding to the first CC and of a waveform of the one or more waveforms corresponding to the second CC satisfies a PAPR threshold.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The method of claim 3, wherein the one or more PRT location sequences include a second PRT location sequence of a plurality of contiguously located PRTs.",
          "claim_type": "dependent",
          "dependency": "claim 3",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The method of claim 4, wherein the contiguously located PRTs of the second PRT location sequence are located within the second bandwidth of the second CC and are configured such that PAPR of the waveform of the one or more waveforms corresponding to the second CC satisfies the PAPR threshold.",
          "claim_type": "dependent",
          "dependency": "claim 4",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. The method of claim 1, wherein the one or more PRT location sequences provide a PRT inband location configuration relative to data tones of the first CC.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The method of claim 1, wherein the one or more PRT location sequences include a first PRT location sequence of a plurality of distributively located PRTs, and wherein the distributively located PRTs of the first PRT location sequence include PRTs located within the first bandwidth of the first CC interleaved with data tones of the first CC and are configured such that peak to average power ratio (PAPR) of a waveform of the one or more waveforms corresponding to the first CC satisfies a PAPR threshold.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The method of claim 7, wherein the distributively located PRTs of the first PRT location sequence include PRTs located within the second bandwidth of the second CC interleaved with data tones of the second CC and are configured such that PAPR of the waveform of the one or more waveforms corresponding to the first CC and of a waveform of the one or more waveforms corresponding to the second CC satisfies a PAPR threshold.",
          "claim_type": "dependent",
          "dependency": "claim 7",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. The method of claim 7, wherein the one or more PRT location sequences include a second PRT location sequence of a plurality of distributively located PRTs, and wherein the distributively located PRTs of the second PRT location sequence are located within the second bandwidth of the second CC interleaved with data tones of the second CC and are configured such that PAPR of a waveform of the one or more waveforms corresponding to the second CC satisfies the PAPR threshold.",
          "claim_type": "dependent",
          "dependency": "claim 7",
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. The method of claim 1, wherein the first CC and the second CC are CCs of an intra-band carrier aggregation (CA) configuration, and wherein the first bandwidth of the first CC and the second bandwidth of the second CC are within a first frequency range predefined for the intra-band CA configuration.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. The method of claim 1, wherein the first CC and the second CC are CCs of a carrier aggregation (CA) configuration, and wherein a frequency range of the first bandwidth of the first CC and a frequency range of the second bandwidth of the second CC are contiguous.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. An apparatus configured for wireless communication, the apparatus comprising:\na memory; and\nat least one processor in electrical communication with the memory, wherein the at least one processor is configured to cause the apparatus to:\nreceive, by a user equipment (UE), resource allocation indicating data tones and peak reduction tones (PRTs) with respect to each component carrier (CC) of a plurality of CCs, wherein the resource allocation indicates data tone locations within a first bandwidth of a first CC of the plurality of CCs and within a second bandwidth of a second CC of the plurality of CCs, and wherein the resource allocation indicates PRT locations within at least one of the first bandwidth or the second bandwidth according to one or more PRT location sequences; and\ntransmit, by the UE, a data transmission comprising one or more waveforms configured according to the resource allocation.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. The apparatus of claim 12, wherein the one or more PRT location sequences provide a PRT sideband location configuration relative to data tones of the first CC, the second CC, or both.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. The apparatus of claim 12, wherein the one or more PRT location sequences include a first PRT location sequence of a plurality of contiguously located PRTs, and wherein the contiguously located PRTs of the first PRT location sequence are located within the first bandwidth of the first CC and are configured such that peak to average power ratio (PAPR) of a waveform of the one or more waveforms corresponding to the first CC and of a waveform of the one or more waveforms corresponding to the second CC satisfies a PAPR threshold.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00015",
          "claim_text": "15. The apparatus of claim 12, wherein the one or more PRT location sequences provide a PRT inband location configuration relative to data tones of the first CC, the second CC, or both.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00016",
          "claim_text": "16. The apparatus of claim 12, wherein the one or more PRT location sequences include a first PRT location sequence of a plurality of distributively located PRTs, and wherein the distributively located PRTs of the first PRT location sequence are located within the first bandwidth of the first CC interleaved with data tones of the first CC and are configured such that peak to average power ratio (PAPR) of a waveform of the one or more waveforms corresponding to the first CC satisfies a PAPR threshold.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00017",
          "claim_text": "17. The apparatus of claim 12, wherein the first CC and the second CC are CCs of an intra-band carrier aggregation (CA) configuration, and wherein the first bandwidth of the first CC and the second bandwidth of the second CC are within a first frequency range predefined for the intra-band CA configuration.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00018",
          "claim_text": "18. The apparatus of claim 12, wherein the first CC and the second CC are CCs of a carrier aggregation (CA) configuration, and wherein a frequency range of the first bandwidth of the first CC and a frequency range of the second bandwidth of the second CC are contiguous.",
          "claim_type": "dependent",
          "dependency": "claim 12",
          "is_exemplary": true
        },
        {
          "claim_number": "00019",
          "claim_text": "19. A method of wireless communication, comprising:\ntransmitting, by a base station, resource allocation indicating data tones and peak reduction tones (PRTs) with respect to each component carrier (CC) of a plurality of CCs, wherein the resource allocation indicates data tone locations within a first bandwidth of a first CC of the plurality of CCs and within a second bandwidth of a second CC of the plurality of CCs, and wherein the resource allocation indicates PRT locations within at least one of the first bandwidth or the second bandwidth according to one or more PRT location sequences; and\nreceiving, by the base station, a data transmission comprising one or more waveforms configured according to the resource allocation.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00020",
          "claim_text": "20. The method of claim 19, wherein the one or more PRT location sequences provide a PRT sideband location configuration relative to data tones of the first CC, the second CC, or both.",
          "claim_type": "dependent",
          "dependency": "claim 19",
          "is_exemplary": true
        },
        {
          "claim_number": "00021",
          "claim_text": "21. The method of claim 19, wherein the one or more PRT location sequences include a first PRT location sequence of a plurality of contiguously located PRTs, and wherein the contiguously located PRTs of the first PRT location sequence are located within the first bandwidth of the first CC and are configured such that peak to average power ratio (PAPR) of a waveform of the one or more waveforms corresponding to the first CC and of a waveform of the one or more waveforms corresponding to the second CC satisfies a PAPR threshold.",
          "claim_type": "dependent",
          "dependency": "claim 19",
          "is_exemplary": true
        },
        {
          "claim_number": "00022",
          "claim_text": "22. The method of claim 21, wherein the one or more PRT location sequences include a second PRT location sequence of a plurality of contiguously located PRTs.",
          "claim_type": "dependent",
          "dependency": "claim 21",
          "is_exemplary": true
        },
        {
          "claim_number": "00023",
          "claim_text": "23. The method of claim 22, wherein the contiguously located PRTs of the second PRT location sequence are located within the second bandwidth of the second CC and are configured such that PAPR of the waveform of the one or more waveforms corresponding to the second CC satisfies the PAPR threshold.",
          "claim_type": "dependent",
          "dependency": "claim 22",
          "is_exemplary": true
        },
        {
          "claim_number": "00024",
          "claim_text": "24. The method of claim 19, wherein the one or more PRT location sequences provide a PRT inband location configuration relative to data tones of the first CC.",
          "claim_type": "dependent",
          "dependency": "claim 19",
          "is_exemplary": true
        },
        {
          "claim_number": "00025",
          "claim_text": "25. The method of claim 19, wherein the one or more PRT location sequences include a first PRT location sequence of a plurality of distributively located PRTs, and wherein the distributively located PRTs of the first PRT location sequence include PRTs located within the first bandwidth of the first CC interleaved with data tones of the first CC and are configured such that peak to average power ratio (PAPR) of a waveform of the one or more waveforms corresponding to the first CC satisfies a PAPR threshold.",
          "claim_type": "dependent",
          "dependency": "claim 19",
          "is_exemplary": true
        },
        {
          "claim_number": "00026",
          "claim_text": "26. The method of claim 25, wherein the distributively located PRTs of the first PRT location sequence include PRTs located within the second bandwidth of the second CC interleaved with data tones of the second CC and are configured such that PAPR of the waveform of the one or more waveforms corresponding to the first CC and of a waveform of the one or more waveforms corresponding to the second CC satisfies a PAPR threshold.",
          "claim_type": "dependent",
          "dependency": "claim 25",
          "is_exemplary": true
        },
        {
          "claim_number": "00027",
          "claim_text": "27. The method of claim 25, wherein the one or more PRT location sequences include a second PRT location sequence of a plurality of distributively located PRTs, and wherein the distributively located PRTs of the second PRT location sequence are located within the second bandwidth of the second CC interleaved with data tones of the second CC and are configured such that PAPR of a waveform of the one or more waveforms corresponding to the second CC satisfies the PAPR threshold.",
          "claim_type": "dependent",
          "dependency": "claim 25",
          "is_exemplary": true
        },
        {
          "claim_number": "00028",
          "claim_text": "28. The method of claim 19, wherein the first CC and the second CC are CCs of an intra-band carrier aggregation (CA) configuration, and wherein the first bandwidth of the first CC and the second bandwidth of the second CC are within a first frequency range predefined for the intra-band CA configuration.",
          "claim_type": "dependent",
          "dependency": "claim 19",
          "is_exemplary": true
        },
        {
          "claim_number": "00029",
          "claim_text": "29. The method of claim 19, wherein the first CC and the second CC are CCs of a carrier aggregation (CA) configuration, and wherein a frequency range of the first bandwidth of the first CC and a frequency range of the second bandwidth of the second CC are contiguous.",
          "claim_type": "dependent",
          "dependency": "claim 19",
          "is_exemplary": true
        },
        {
          "claim_number": "00030",
          "claim_text": "30. An apparatus configured for wireless communication, the apparatus comprising:\na memory; and\nat least one processor in electrical communication with the memory, wherein the at least one processor is configured to cause the apparatus to:\ntransmit, by a base station, resource allocation indicating data tones and peak reduction tones (PRTs) with respect to each component carrier (CCs) of a plurality of CCs, wherein the resource allocation indicates data tone locations within a first bandwidth of a first CC of the plurality of CCs and within a second bandwidth of a second CC of the plurality of CCs, and wherein the resource allocation indicates PRT locations within at least one of the first bandwidth or the second bandwidth according to one or more PRT location sequences; and\nreceive, by the base station, a data transmission comprising one or more waveforms configured according to the resource allocation.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00031",
          "claim_text": "31. The apparatus of claim 30, wherein the one or more PRT location sequences provide a PRT sideband location configuration relative to data tones of the first CC, the second CC, or both.",
          "claim_type": "dependent",
          "dependency": "claim 30",
          "is_exemplary": true
        },
        {
          "claim_number": "00032",
          "claim_text": "32. The apparatus of claim 30, wherein the one or more PRT location sequences include a first PRT location sequence of a plurality of contiguously located PRTs, and wherein the contiguously located PRTs of the first PRT location sequence are located within the first bandwidth of the first CC and are configured such that peak to average power ratio (PAPR) of a waveform of the one or more waveforms corresponding to the first CC and of a waveform of the one or more waveforms corresponding to the second CC satisfies a PAPR threshold.",
          "claim_type": "dependent",
          "dependency": "claim 30",
          "is_exemplary": true
        },
        {
          "claim_number": "00033",
          "claim_text": "33. The apparatus of claim 30, wherein the one or more PRT location sequences provide a PRT inband location configuration relative to data tones of the first CC, the second CC, or both.",
          "claim_type": "dependent",
          "dependency": "claim 30",
          "is_exemplary": true
        },
        {
          "claim_number": "00034",
          "claim_text": "34. The apparatus of claim 30, wherein the one or more PRT location sequences include a first PRT location sequence of a plurality of distributively located PRTs, and wherein the distributively located PRTs of the first PRT location sequence are located within the first bandwidth of the first CC interleaved with data tones of the first CC and are configured such that peak to average power ratio (PAPR) of a waveform of the one or more waveforms corresponding to the first CC satisfies a PAPR threshold.",
          "claim_type": "dependent",
          "dependency": "claim 30",
          "is_exemplary": true
        },
        {
          "claim_number": "00035",
          "claim_text": "35. The apparatus of claim 30, wherein the first CC and the second CC are CCs of an intra-band carrier aggregation (CA) configuration, and wherein the first bandwidth of the first CC and the second bandwidth of the second CC are within a first frequency range predefined for the intra-band CA configuration.",
          "claim_type": "dependent",
          "dependency": "claim 30",
          "is_exemplary": true
        },
        {
          "claim_number": "00036",
          "claim_text": "36. The apparatus of claim 30, wherein the first CC and the second CC are CCs of a carrier aggregation (CA) configuration, and wherein a frequency range of the first bandwidth of the first CC and a frequency range of the second bandwidth of the second CC are contiguous.",
          "claim_type": "dependent",
          "dependency": "claim 30",
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.6,
      "publication_date": "2023-11-14",
      "patent_year": 2023
    },
    {
      "patent_id": "11711862",
      "title": "Dual connectivity and carrier aggregation band selection",
      "abstract": "The disclosed technology provides a system and method for allocating frequency bands to a mobile device or user equipment (UE) based on priorities assigned to the different frequency bands. When no priority is assigned to the frequency bands, when a special or reserved priority is assigned, or when equal priority is assigned, the frequency band allocation to the UE is based on a default frequency allocation algorithm (e.g., based on a relative bandwidth of the different frequency bands). When a UE is capable of utilizing a first and a second frequency band, and the priority assigned to the first frequency band is higher than the priority assigned to the second frequency band, the network (e.g., eNB/gNB) overrides the default algorithm and preferentially allocates the first frequency band to UE even when the first frequency band has a smaller bandwidth than the second frequency band or when the default algorithm would otherwise prefer the first frequency band.",
      "inventors": [
        "Nishant Patel"
      ],
      "assignees": [
        "T-Mobile USA, Inc."
      ],
      "claims": [
        {
          "claim_number": "00001",
          "claim_text": "1. At least one computer-readable storage medium, excluding transitory signals and carrying instructions, which, when executed by at least one data processor of a system, cause the system to:\ndetermine that a mobile device is capable of operating on a first frequency band and a second frequency band,\nwherein the mobile device is configured to operate in a New Radio (NR) carrier aggregation mode, a NR dual connectivity mode, or an Evolved Universal Mobile Telecommunications System Terrestrial Radio Access Network (EUTRAN) NR dual connectivity (EN-DC) mode;\n\ndetermine a priority indicator assigned to the first frequency band and the second frequency band in response to determining that the mobile device is capable of operating on the first frequency band and the second frequency band;\nallocate the mobile device with component carriers in the first frequency band or the second frequency band according to a first algorithm in response to determining that there is no priority indicator assigned to the first frequency band and to the second frequency band; and,\nallocate the mobile device with component carriers in the first frequency band in response to determining that a first priority indicator assigned to the first frequency band indicates a higher priority than a second priority indicator assigned to the second frequency band,\nwherein allocating the mobile device with the component carriers in the first frequency band is according to a second algorithm, different from the first algorithm.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00002",
          "claim_text": "2. The at least one computer-readable storage medium of claim 1, wherein the system is further caused to:\nallocate the mobile device with component carriers in the first frequency band or the second frequency band according to the first algorithm in response to determining that the first priority indicator assigned to the first frequency band indicates a same priority as a second priority indicator assigned to the second frequency band.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00003",
          "claim_text": "3. The at least one computer-readable storage medium of claim 1, wherein the system is further caused to:\nallocate the mobile device with component carriers in the first frequency band or the second frequency band according to the first algorithm in response to determining that there is no priority indicator assigned to the first frequency band and the priority indicator assigned to the second frequency band indicates a first reserved priority indicator.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00004",
          "claim_text": "4. The at least one computer-readable storage medium of claim 1, wherein the system is further caused to:\nallocate the mobile device with component carriers in the first frequency band according to the first algorithm in response to determining that there is no priority indicator assigned to the first frequency band and the priority indicator assigned to the second frequency band indicates a second reserved priority indicator, wherein the second reserved priority indicator indicates that the second frequency band should not be considered in allocating component carriers to the mobile device.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00005",
          "claim_text": "5. The at least one computer-readable storage medium of claim 1, wherein the first frequency band comprises a smaller bandwidth than the second frequency band.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00006",
          "claim_text": "6. The at least one computer-readable storage medium of claim 1, wherein the first priority indicator and the second priority indicator are based on one or more measurement reports of the first frequency band and the second frequency band.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00007",
          "claim_text": "7. The at least one computer-readable storage medium of claim 1, wherein the first priority indicator and the second priority indicator is assigned by a self-optimizing network (SON) configured to determine the priority indicator based on one or more characteristics of traffic on the first frequency band and the second frequency band, and wherein the one or more characteristics of traffic comprises a number of connected users, a downlink (DL) physical resource block (PRB) utilization, or an uplink (UL) PRB utilization.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00008",
          "claim_text": "8. The at least one computer-readable storage medium of claim 1, wherein the system comprises a gNodeB (gNB) operating in a New Radio (NR) radio access network, wherein the first algorithm is a default algorithm employed by the gNB and wherein the second algorithm is an override algorithm.",
          "claim_type": "dependent",
          "dependency": "claim 1",
          "is_exemplary": true
        },
        {
          "claim_number": "00009",
          "claim_text": "9. A method comprising:\ndetermining whether a priority indicator is assigned to a first frequency band and a second frequency band;\nallocating a user equipment (UE) with component carriers (CCs) in the first frequency band or the second frequency band according to a first frequency allocation scheme in response to determining that there is no priority indicator assigned to the first frequency band and to the second frequency band; and,\nallocating the UE with CCs in the first frequency band in response to determining that a first priority indicator assigned to the first frequency band indicates a higher priority than a second priority indicator assigned to the second frequency band,\nwherein allocating the UE with the CCs in the first frequency band is according to a second frequency allocation scheme, different from the first frequency allocation scheme.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00010",
          "claim_text": "10. The method of claim 9 further comprising:\nallocating the UE with CCs in the first frequency band or the second frequency band according to the first frequency allocation scheme in response to determining that the first priority indicator assigned to the first frequency band indicates a same priority as a second priority indicator assigned to the second frequency band.",
          "claim_type": "dependent",
          "dependency": "claim 9",
          "is_exemplary": true
        },
        {
          "claim_number": "00011",
          "claim_text": "11. The method of claim 9 further comprising:\nallocate the UE with CCs in the first frequency band according to the first frequency allocation scheme in response to determining that there is no priority indicator assigned to the first frequency band and the priority indicator assigned to the second frequency band indicates a second reserved priority indicator, wherein the second reserved priority indicator indicates that the second frequency band should not be considered in allocating component carriers to the UE.",
          "claim_type": "dependent",
          "dependency": "claim 9",
          "is_exemplary": true
        },
        {
          "claim_number": "00012",
          "claim_text": "12. The method of claim 9, wherein the first priority indicator and the second priority indicator is assigned by a self-optimizing network (SON) configured to determine the priority indicator based on one or more characteristics of traffic on the first frequency band and the second frequency band, wherein the one of more characteristics of traffic comprises a number of connected users, a downlink (DL) physical resource block (PRB) utilization, or an uplink (UL) PRB utilization.",
          "claim_type": "dependent",
          "dependency": "claim 9",
          "is_exemplary": true
        },
        {
          "claim_number": "00013",
          "claim_text": "13. A system comprising:\nat least one hardware processor; and\nat least one non-transitory memory, coupled to the at least one hardware processor and storing instructions, which, when executed by the at least one hardware processor, cause the system to:\ndetermine a priority indicator assigned to a first frequency band and a second frequency band;\nallocate a user equipment (UE) with component carriers (CCs) in the first frequency band or the second frequency band according to a default frequency allocation scheme in response to determining that there is no priority indicator assigned to the first frequency band and to the second frequency band; and,\nallocate the UE with CCs in the first frequency band in response to determining that a first priority indicator assigned to the first frequency band indicates a higher priority than a second priority indicator assigned to the second frequency band, wherein allocating the UE with the CCs in the first frequency band is according to an operator-specific frequency allocation scheme, different from the default frequency allocation scheme.",
          "claim_type": "independent",
          "dependency": null,
          "is_exemplary": true
        },
        {
          "claim_number": "00014",
          "claim_text": "14. The system of claim 13 further caused to:\nallocate the UE with CCs in the first frequency band or the second frequency band according to the default frequency allocation scheme in response to determining that the first priority indicator assigned to the first frequency band indicates a same priority as a second priority indicator assigned to the second frequency band.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00015",
          "claim_text": "15. The system of claim 13 further caused to:\nallocate the UE with CCs in the first frequency band or the second frequency band according to the default frequency allocation scheme in response to determining that there is no priority indicator assigned to the first frequency band and the priority indicator assigned to the second frequency band indicates a first reserved priority indicator.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00016",
          "claim_text": "16. The system of claim 13 further caused to:\nallocate the UE with CCs in the first frequency band according to the default frequency allocation scheme in response to determining that there is no priority indicator assigned to the first frequency band and the priority indicator assigned to the second frequency band indicates a second reserved priority indicator, wherein the second reserved priority indicator indicates that the second frequency band should not be considered in allocating component carriers to the UE.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00017",
          "claim_text": "17. The system of claim 13, wherein the first frequency band comprises a smaller bandwidth than the second frequency band.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00018",
          "claim_text": "18. The system of claim 13, wherein the first priority indicator and the second priority indicator are based on one or more measurement reports of the first frequency band and the second frequency band.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00019",
          "claim_text": "19. The system of claim 13, wherein the first priority indicator and the second priority indicator is assigned by a self-optimizing network (SON) configured to determine the priority indicator based on one or more characteristics of traffic on the first frequency band and the second frequency band, wherein the one of more characteristics of traffic comprises a number of connected users, a downlink (DL) physical resource block (PRB) utilization, or an uplink (UL) PRB utilization.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        },
        {
          "claim_number": "00020",
          "claim_text": "20. The system of claim 13, wherein the system comprises gNodeB (gNB) or eNodeB (eNB), and wherein the UE is configured to operate in a New Radio (NR) carrier aggregation mode, a NR dual connectivity mode, or an Evolved Universal Mobile Telecommunications System Terrestrial Radio Access Network (EUTRAN) NR dual connectivity (EN-DC) mode.",
          "claim_type": "dependent",
          "dependency": "claim 13",
          "is_exemplary": true
        }
      ],
      "relevance_score": 0.7,
      "publication_date": "2023-07-25",
      "patent_year": 2023
    },
    {
      "patent_id": "9485774",
      "title": "Efficient transmission of stand-alone aperiodic CSI reporting for LTE carrier aggregation",
      "abstract": "The transmission of stand-alone, aperiodic CSI reports from a UE in carrier aggregation in an LTE network is optimized. The coding rate is indirectly controlled by varying the number of RBs allocated for the CSI report transmission. Two sets of serving cells are established, and the payload of each set is approximated. For each allowable number of RBs and each payload size, a threshold SINR is determined and stored. An initial number of RBs is selected, based on the number of cells. The actual SINR is measured, and compared to the threshold SINR for the number of RBs and payload size. The number of RBs to be allocated is varied based on the comparison, by varying an index into an array of allowable numbers of RBs. Link adaptation is performed based on observed decoding errors, in an outer loop control algorithm that prevents wind up. An optimization for the particular case of one PCell and one SCell is also presented.",
      "inventors": [
        "Jianguo Long",
        "Ping Yu",
        "Girum Fantaye"
      ],
      "assignees": [
        "TELEFONAKTIEBOLAGET LM ERICSSON (PUBL)"
      ],
      "claims": [],
      "relevance_score": 0.7,
      "publication_date": "2016-11-01",
      "patent_year": 2016
    },
    {
      "patent_id": "10772026",
      "title": "Wireless relay quality-of-service based on relay-delivered media services",
      "abstract": "A wireless communication network controls wireless base stations that serve wireless relays that serve wireless User Equipment (UEs). In a relay control system, data transceivers receive configuration data that was transferred by the wireless relays and that indicates their individual wireless media services. Relay control circuitry allocates individual carrier aggregation Quality-of-Service (QoS) levels to the individual wireless relays based on the individual wireless media services. The relay transceivers transfer the individual carrier aggregation QoS levels for the individual wireless relays to the wireless base stations. The wireless base stations serve the wireless relays with the individual carrier aggregation QoS levels. The wireless relays serve the wireless UEs with the wireless media services.",
      "inventors": [
        "Vanil Parihar",
        "Nitesh Manchanda"
      ],
      "assignees": [
        "SPRINT COMMUNICATIONS COMPANY, L.P."
      ],
      "claims": [],
      "relevance_score": 0.7,
      "publication_date": "2020-09-08",
      "patent_year": 2020
    }
  ],
  "status": "success",
  "search_result": {
    "query": "AI for carrier aggregation",
    "total_found": 10,
    "patents": [
      {
        "patent_id": "12113614",
        "title": "AIML positioning receiver for flexible carrier aggregation",
        "abstract": "An apparatus comprising circuitry configured to: receive a plurality of signal samples, wherein at least two of the signal samples are received on different carrier frequencies or over different durations; convert the plurality of signal samples to a common data format that stores as entries the samples, a stored entry corresponding to a sample measured with a carrier frequency, a time, and a receive antenna; generate entries of the common data format that are missing due to a sample not being measured with a carrier frequency, time, and receive antenna; wherein the entries of the common data format are ranked, wherein a higher ranking entry is considered more relevant than a relatively lower ranking entry; and generate at least one positioning measurement with a machine learning model, based on the entries of the common data format and the ranking of the entries of the common data format.",
        "inventors": [
          "Oana-Elena BARBU",
          "Sajad REZAIE"
        ],
        "assignees": [
          "Nokia Solutions and Networks Oy",
          "NOKIA TECHNOLOGIES OY"
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. An apparatus comprising:\nat least one processor; and\nat least one memory storing instructions that, when executed by the at least one processor, cause the apparatus at least to:\nreceive a plurality of signal samples, wherein at least two of the signal samples are received on different carrier frequencies, or wherein at least two of the signal samples are received over different durations;\nconvert the plurality of signal samples to a common data format that stores as entries the plurality of signal samples, a stored entry corresponding to a signal sample measured with a carrier frequency, a time, and a receive antenna;\ngenerate entries of the common data format that are missing due to a signal sample not being measured with a carrier frequency, time, and receive antenna;\nwherein the entries of the common data format are ranked, wherein a higher ranking entry is considered more relevant than a relatively lower ranking entry; and\ngenerate at least one positioning measurement with a machine learning model, based on the entries of the common data format and the ranking of the entries of the common data format.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The apparatus of claim 1, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\ngenerate the entries of the common data format that are missing with accounting for:\na frequency, time, and space selectivity of a channel response, and\nan identifier of a transmitter of the signal samples.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The apparatus of claim 1, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\nestimate a channel response between a respective network node that transmits at least a portion of the signal samples and a respective receive antenna, at resource elements of the common data format; and\ngenerate the entries of the common data format that are missing based on the respective estimated channel response.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The apparatus of claim 3, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\nestimate the channel response using linear mean squared error estimation given a respective signal vector at a respective receive antenna; or\ntrain a machine learning channel estimation model with a dataset comprising measured channel responses and unmeasured channel responses, the labels of the dataset comprising the measured channel responses, and estimate the channel response using the machine learning channel estimation model.",
            "claim_type": "dependent",
            "dependency": "claim 3",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The apparatus of claim 1, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\ndiscard or set to zero at least one entry of the common data format corresponding to an unused resource; or\nreshape the common data format to be of a size of the machine learning model used to generate the at least one positioning measurement.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. The apparatus of claim 1, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\nrank the entries of the common data format based on at least one of: a noise level of a resource element corresponding to an entry, or an interference level of the resource element corresponding to the entry.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The apparatus of claim 1, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\nrank the entries of the common data format using a data structure;\nwherein at least one entry within the data structure corresponds to a weight of a carrier frequency, wherein a first weight of a first carrier frequency is ranked higher than a second weight of a second carrier frequency when the first carrier frequency has over a period of time provided a more accurate positioning accuracy than the second carrier frequency;\nwherein at least one entry within the data structure corresponds to a weight of an orthogonal frequency division multiplexing symbol.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The apparatus of claim 1, wherein the at least one positioning measurement comprises at least one of:\na location of a user equipment,\ncoordinates of a location of a user equipment,\na line of sight indicator,\na non-line of sight indicator,\na set of mappings between a respective line of sight and a respective signal source, or\na combination of at least two of a location of a user equipment, coordinates of a location of a user equipment, a line of sight indicator, a non-line of sight indicator, or a set of mappings between a respective line of sight and a respective signal source.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. The apparatus of claim 1, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\ntrain the machine learning model using a loss function based on a mean squared error of a location of a user equipment and a cross entropy of a line of sight.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. The apparatus of claim 1, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\nin response to the at least one positioning measurement not being within a range given with at least one first threshold expected positioning measurement and at least one second threshold expected positioning measurement, modify the ranking of the entries of the common data format, and regenerate the at least one positioning measurement with the machine learning model based on the entries of the common data format and the modified ranking of the entries of the common data format.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. An apparatus comprising:\nat least one processor; and\nat least one memory storing instructions that, when executed by the at least one processor, cause the apparatus at least to:\nreceive a plurality of signal samples, wherein at least two of the signal samples are received with different resource elements;\nconvert the plurality of signal samples to a common data format that stores as entries the plurality of signal samples, a stored entry corresponding to a signal sample measured with a resource element;\ngenerate entries of the common data format that are missing due to a signal sample not being measured with a resource element;\nwherein the entries of the common data format are ranked, wherein a higher ranking entry is considered more relevant than a relatively lower ranking entry; and\ngenerate at least one positioning measurement with a machine learning model, based on the entries of the common data format and the ranking of the entries of the common data format.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. The apparatus of claim 11, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\ngenerate the entries of the common data format that are missing with accounting for:\na frequency, time, and space selectivity of a channel response, and\nan identifier of a transmitter of the signal samples.",
            "claim_type": "dependent",
            "dependency": "claim 11",
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. The apparatus of claim 11, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\nestimate a channel response between a respective network node that transmits at least a portion of the signal samples and a respective receive antenna, at resource elements of the common data format; and\ngenerate the entries of the common data format that are missing based on the respective estimated channel response.",
            "claim_type": "dependent",
            "dependency": "claim 11",
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. The apparatus of claim 11, wherein the instructions, when executed by the at least one processor, cause the apparatus at least to:\nrank the entries of the common data format based on at least one of: a noise level of a resource element corresponding to an entry, or an interference level of the resource element corresponding to the entry.",
            "claim_type": "dependent",
            "dependency": "claim 11",
            "is_exemplary": true
          },
          {
            "claim_number": "00015",
            "claim_text": "15. The apparatus of claim 11, wherein the at least one positioning measurement comprises at least one of:\na location of a user equipment,\ncoordinates of a location of a user equipment,\na line of sight indicator,\na non-line of sight indicator,\na set of mappings between a respective line of sight and a respective signal source, or\na combination of at least two of a location of a user equipment, coordinates of a location of a user equipment, a line of sight indicator, a non-line of sight indicator, or a set of mappings between a respective line of sight and a respective signal source.",
            "claim_type": "dependent",
            "dependency": "claim 11",
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.8,
        "publication_date": "2024-10-08",
        "patent_year": 2024
      },
      {
        "patent_id": "9736741",
        "title": "Method, apparatus and system for cell handover in communication system supporting carrier aggregation",
        "abstract": "A method, apparatus and system for cell handover in the communication system supporting Carrier Aggregation (CA). The method includes: after receiving a performance measurement report for one or more neighboring cells from the served terminal, according to the performance measurement report, and basing on the CA mode for one or more candidate BSs corresponding to the one or more neighboring cells, a source Base Station (BS) in a communications system selects an algorithm suitable for the CA mode to calculate the priority levels of the one or more candidate BSs; from the one or more candidate BSs, selecting the BS having the highest priority as a target BS; and selecting one more cells to access from all cells being subject to the target BS in the one or more neighboring cells.",
        "inventors": [
          "Yuxin WEI"
        ],
        "assignees": [
          "SONY GROUP CORPORATION"
        ],
        "claims": [],
        "relevance_score": 0.8,
        "publication_date": "2017-08-15",
        "patent_year": 2017
      },
      {
        "patent_id": "9210637",
        "title": "Method, apparatus and system for cell handover in communication system supporting carrier aggregation",
        "abstract": "A method, apparatus and system for cell handover in the communication system supporting Carrier Aggregation (CA). The method includes: after receiving a performance measurement report for one or more neighboring cells from the served terminal, according to the performance measurement report, and basing on the CA mode for one or more candidate BSs corresponding to the one or more neighboring cells, a source Base Station (BS) in a communications system selects an algorithm suitable for the CA mode to calculate the priority levels of the one or more candidate BSs; from the one or more candidate BSs, selecting the BS having the highest priority as a target BS; and selecting one more cells to access from all cells being subject to the target BS in the one or more neighboring cells.",
        "inventors": [
          "Yuxin WEI"
        ],
        "assignees": [
          "SONY GROUP CORPORATION"
        ],
        "claims": [],
        "relevance_score": 0.8,
        "publication_date": "2015-12-08",
        "patent_year": 2015
      },
      {
        "patent_id": "9025446",
        "title": "Carrier selection policy for joint scheduling for carrier aggregation in an LTE-advanced system",
        "abstract": "Various embodiments of a semi-joint scheduling algorithm for carrier aggregation in an LTE-Advanced system are provided. The proposed semi-joint scheduling algorithm combines the advantages of independent scheduling and joint scheduling while avoiding the respective shortcomings, and provides a technical foundation for a wide adoption of the carrier aggregation technology. This Abstract is submitted with the understanding that it will not be used to interpret or limit the scope or meaning of the claims.",
        "inventors": [
          "Anpeng Huang"
        ],
        "assignees": [
          "Empire Technology Development LLC"
        ],
        "claims": [],
        "relevance_score": 0.8,
        "publication_date": "2015-05-05",
        "patent_year": 2015
      },
      {
        "patent_id": "10050761",
        "title": "System and method for user equipment initiated management of carrier aggregation",
        "abstract": "Methods that are performed by a user equipment (UE) and corresponding methods of base stations that allow a UE to determine whether the UE is in a carrier aggregation enabled or disabled state. One exemplary embodiment of a method performed by a UE determines a first artificial value for a first parameter and a second artificial value for a power headroom (PHR) for a secondary component carrier (SCC), the first and second artificial values being substantially low relative to a configuration of the network, generates an artificial report including the first and second artificial values, transmits the artificial report to a primary cell providing a primary component carrier (PCC) and receives an indication that the UE is placed in a carrier aggregation disabled state.",
        "inventors": [
          "Sarma V. Vangala",
          "Swaminathan Balakrishnan",
          "Tarik Tabet",
          "Rafael L. Rivera-Barreto",
          "Samy Khay-Ibbat",
          "Sree Ram Kodali"
        ],
        "assignees": [
          "Apple Inc."
        ],
        "claims": [],
        "relevance_score": 0.7,
        "publication_date": "2018-08-14",
        "patent_year": 2018
      },
      {
        "patent_id": "9479315",
        "title": "System and method for user equipment initiated management of carrier aggregation",
        "abstract": "Methods that are performed by a user equipment (UE) and corresponding methods of base stations that allow a UE to determine whether the UE is in a carrier aggregation enabled or disabled state. One exemplary embodiment of a method performed by a UE determines a first artificial value for a first parameter and a second artificial value for a power headroom (PHR) for a secondary component carrier (SCC), the first and second artificial values being substantially low relative to a configuration of the network, generates an artificial report including the first and second artificial values, transmits the artificial report to a primary cell providing a primary component carrier (PCC) and receives an indication that the UE is placed in a carrier aggregation disabled state.",
        "inventors": [
          "Sarma V. Vangala",
          "Swaminathan Balakrishnan",
          "Tarik Tabet",
          "Rafael L. Rivera-Barreto",
          "Samy Khay-Ibbat",
          "Sree Ram Kodali"
        ],
        "assignees": [
          "Apple Inc."
        ],
        "claims": [],
        "relevance_score": 0.7,
        "publication_date": "2016-10-25",
        "patent_year": 2016
      },
      {
        "patent_id": "11817986",
        "title": "Carrier aggregation peak to average power ratio reduction using peak reduction tones",
        "abstract": "Peak to average power ratio (PAPR) reduction with respect to signals of component carriers of a carrier aggregation configuration may be provided using preconfigured or fixed PRT location sequences (e.g., fixing the number and location of PRTs). A device transmitting signals of component carriers of a carrier aggregation configuration may perform PRT magnitude and phase optimization processing with respect to PRTs of a PRT location sequence using techniques, such as may use a signal to clipping noise ratio, tone reservation (SCR-TR) algorithm. Various PRT location sequence configurations, such as PRT sideband location sequence configurations, PRT inband location sequence configurations, etc., may be selected to facilitate reduction of PAPR associated with the data tones of one or more carrier aggregation component carriers, such as to satisfy a PAPR threshold. Other aspects and features are also claimed and described.",
        "inventors": [
          "Krishna Kiran Mukkavilli",
          "Wei Yang",
          "Gokul Sridharan",
          "Saeid SAHRAEI"
        ],
        "assignees": [
          "QUALCOMM Incorporated"
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. A method of wireless communication, comprising:\nreceiving, by a user equipment (UE), resource allocation indicating data tones and peak reduction tones (PRTs) with respect to each component carrier (CC) of a plurality of CCs, wherein the resource allocation indicates data tone locations within a first bandwidth of a first CC of the plurality of CCs and within a second bandwidth of a second CC of the plurality of CCs, and wherein the resource allocation indicates PRT locations within at least one of the first bandwidth or the second bandwidth according to one or more PRT location sequences; and\ntransmitting, by the UE, a data transmission comprising one or more waveforms configured according to the resource allocation.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The method of claim 1, wherein the one or more PRT location sequences provide a PRT sideband location configuration relative to data tones of the first CC, the second CC, or both.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The method of claim 1, wherein the one or more PRT location sequences include a first PRT location sequence of a plurality of contiguously located PRTs, and wherein the contiguously located PRTs of the first PRT location sequence are located within the first bandwidth of the first CC and are configured such that peak to average power ratio (PAPR) of a waveform of the one or more waveforms corresponding to the first CC and of a waveform of the one or more waveforms corresponding to the second CC satisfies a PAPR threshold.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The method of claim 3, wherein the one or more PRT location sequences include a second PRT location sequence of a plurality of contiguously located PRTs.",
            "claim_type": "dependent",
            "dependency": "claim 3",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The method of claim 4, wherein the contiguously located PRTs of the second PRT location sequence are located within the second bandwidth of the second CC and are configured such that PAPR of the waveform of the one or more waveforms corresponding to the second CC satisfies the PAPR threshold.",
            "claim_type": "dependent",
            "dependency": "claim 4",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. The method of claim 1, wherein the one or more PRT location sequences provide a PRT inband location configuration relative to data tones of the first CC.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The method of claim 1, wherein the one or more PRT location sequences include a first PRT location sequence of a plurality of distributively located PRTs, and wherein the distributively located PRTs of the first PRT location sequence include PRTs located within the first bandwidth of the first CC interleaved with data tones of the first CC and are configured such that peak to average power ratio (PAPR) of a waveform of the one or more waveforms corresponding to the first CC satisfies a PAPR threshold.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The method of claim 7, wherein the distributively located PRTs of the first PRT location sequence include PRTs located within the second bandwidth of the second CC interleaved with data tones of the second CC and are configured such that PAPR of the waveform of the one or more waveforms corresponding to the first CC and of a waveform of the one or more waveforms corresponding to the second CC satisfies a PAPR threshold.",
            "claim_type": "dependent",
            "dependency": "claim 7",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. The method of claim 7, wherein the one or more PRT location sequences include a second PRT location sequence of a plurality of distributively located PRTs, and wherein the distributively located PRTs of the second PRT location sequence are located within the second bandwidth of the second CC interleaved with data tones of the second CC and are configured such that PAPR of a waveform of the one or more waveforms corresponding to the second CC satisfies the PAPR threshold.",
            "claim_type": "dependent",
            "dependency": "claim 7",
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. The method of claim 1, wherein the first CC and the second CC are CCs of an intra-band carrier aggregation (CA) configuration, and wherein the first bandwidth of the first CC and the second bandwidth of the second CC are within a first frequency range predefined for the intra-band CA configuration.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. The method of claim 1, wherein the first CC and the second CC are CCs of a carrier aggregation (CA) configuration, and wherein a frequency range of the first bandwidth of the first CC and a frequency range of the second bandwidth of the second CC are contiguous.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. An apparatus configured for wireless communication, the apparatus comprising:\na memory; and\nat least one processor in electrical communication with the memory, wherein the at least one processor is configured to cause the apparatus to:\nreceive, by a user equipment (UE), resource allocation indicating data tones and peak reduction tones (PRTs) with respect to each component carrier (CC) of a plurality of CCs, wherein the resource allocation indicates data tone locations within a first bandwidth of a first CC of the plurality of CCs and within a second bandwidth of a second CC of the plurality of CCs, and wherein the resource allocation indicates PRT locations within at least one of the first bandwidth or the second bandwidth according to one or more PRT location sequences; and\ntransmit, by the UE, a data transmission comprising one or more waveforms configured according to the resource allocation.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. The apparatus of claim 12, wherein the one or more PRT location sequences provide a PRT sideband location configuration relative to data tones of the first CC, the second CC, or both.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. The apparatus of claim 12, wherein the one or more PRT location sequences include a first PRT location sequence of a plurality of contiguously located PRTs, and wherein the contiguously located PRTs of the first PRT location sequence are located within the first bandwidth of the first CC and are configured such that peak to average power ratio (PAPR) of a waveform of the one or more waveforms corresponding to the first CC and of a waveform of the one or more waveforms corresponding to the second CC satisfies a PAPR threshold.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00015",
            "claim_text": "15. The apparatus of claim 12, wherein the one or more PRT location sequences provide a PRT inband location configuration relative to data tones of the first CC, the second CC, or both.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00016",
            "claim_text": "16. The apparatus of claim 12, wherein the one or more PRT location sequences include a first PRT location sequence of a plurality of distributively located PRTs, and wherein the distributively located PRTs of the first PRT location sequence are located within the first bandwidth of the first CC interleaved with data tones of the first CC and are configured such that peak to average power ratio (PAPR) of a waveform of the one or more waveforms corresponding to the first CC satisfies a PAPR threshold.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00017",
            "claim_text": "17. The apparatus of claim 12, wherein the first CC and the second CC are CCs of an intra-band carrier aggregation (CA) configuration, and wherein the first bandwidth of the first CC and the second bandwidth of the second CC are within a first frequency range predefined for the intra-band CA configuration.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00018",
            "claim_text": "18. The apparatus of claim 12, wherein the first CC and the second CC are CCs of a carrier aggregation (CA) configuration, and wherein a frequency range of the first bandwidth of the first CC and a frequency range of the second bandwidth of the second CC are contiguous.",
            "claim_type": "dependent",
            "dependency": "claim 12",
            "is_exemplary": true
          },
          {
            "claim_number": "00019",
            "claim_text": "19. A method of wireless communication, comprising:\ntransmitting, by a base station, resource allocation indicating data tones and peak reduction tones (PRTs) with respect to each component carrier (CC) of a plurality of CCs, wherein the resource allocation indicates data tone locations within a first bandwidth of a first CC of the plurality of CCs and within a second bandwidth of a second CC of the plurality of CCs, and wherein the resource allocation indicates PRT locations within at least one of the first bandwidth or the second bandwidth according to one or more PRT location sequences; and\nreceiving, by the base station, a data transmission comprising one or more waveforms configured according to the resource allocation.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00020",
            "claim_text": "20. The method of claim 19, wherein the one or more PRT location sequences provide a PRT sideband location configuration relative to data tones of the first CC, the second CC, or both.",
            "claim_type": "dependent",
            "dependency": "claim 19",
            "is_exemplary": true
          },
          {
            "claim_number": "00021",
            "claim_text": "21. The method of claim 19, wherein the one or more PRT location sequences include a first PRT location sequence of a plurality of contiguously located PRTs, and wherein the contiguously located PRTs of the first PRT location sequence are located within the first bandwidth of the first CC and are configured such that peak to average power ratio (PAPR) of a waveform of the one or more waveforms corresponding to the first CC and of a waveform of the one or more waveforms corresponding to the second CC satisfies a PAPR threshold.",
            "claim_type": "dependent",
            "dependency": "claim 19",
            "is_exemplary": true
          },
          {
            "claim_number": "00022",
            "claim_text": "22. The method of claim 21, wherein the one or more PRT location sequences include a second PRT location sequence of a plurality of contiguously located PRTs.",
            "claim_type": "dependent",
            "dependency": "claim 21",
            "is_exemplary": true
          },
          {
            "claim_number": "00023",
            "claim_text": "23. The method of claim 22, wherein the contiguously located PRTs of the second PRT location sequence are located within the second bandwidth of the second CC and are configured such that PAPR of the waveform of the one or more waveforms corresponding to the second CC satisfies the PAPR threshold.",
            "claim_type": "dependent",
            "dependency": "claim 22",
            "is_exemplary": true
          },
          {
            "claim_number": "00024",
            "claim_text": "24. The method of claim 19, wherein the one or more PRT location sequences provide a PRT inband location configuration relative to data tones of the first CC.",
            "claim_type": "dependent",
            "dependency": "claim 19",
            "is_exemplary": true
          },
          {
            "claim_number": "00025",
            "claim_text": "25. The method of claim 19, wherein the one or more PRT location sequences include a first PRT location sequence of a plurality of distributively located PRTs, and wherein the distributively located PRTs of the first PRT location sequence include PRTs located within the first bandwidth of the first CC interleaved with data tones of the first CC and are configured such that peak to average power ratio (PAPR) of a waveform of the one or more waveforms corresponding to the first CC satisfies a PAPR threshold.",
            "claim_type": "dependent",
            "dependency": "claim 19",
            "is_exemplary": true
          },
          {
            "claim_number": "00026",
            "claim_text": "26. The method of claim 25, wherein the distributively located PRTs of the first PRT location sequence include PRTs located within the second bandwidth of the second CC interleaved with data tones of the second CC and are configured such that PAPR of the waveform of the one or more waveforms corresponding to the first CC and of a waveform of the one or more waveforms corresponding to the second CC satisfies a PAPR threshold.",
            "claim_type": "dependent",
            "dependency": "claim 25",
            "is_exemplary": true
          },
          {
            "claim_number": "00027",
            "claim_text": "27. The method of claim 25, wherein the one or more PRT location sequences include a second PRT location sequence of a plurality of distributively located PRTs, and wherein the distributively located PRTs of the second PRT location sequence are located within the second bandwidth of the second CC interleaved with data tones of the second CC and are configured such that PAPR of a waveform of the one or more waveforms corresponding to the second CC satisfies the PAPR threshold.",
            "claim_type": "dependent",
            "dependency": "claim 25",
            "is_exemplary": true
          },
          {
            "claim_number": "00028",
            "claim_text": "28. The method of claim 19, wherein the first CC and the second CC are CCs of an intra-band carrier aggregation (CA) configuration, and wherein the first bandwidth of the first CC and the second bandwidth of the second CC are within a first frequency range predefined for the intra-band CA configuration.",
            "claim_type": "dependent",
            "dependency": "claim 19",
            "is_exemplary": true
          },
          {
            "claim_number": "00029",
            "claim_text": "29. The method of claim 19, wherein the first CC and the second CC are CCs of a carrier aggregation (CA) configuration, and wherein a frequency range of the first bandwidth of the first CC and a frequency range of the second bandwidth of the second CC are contiguous.",
            "claim_type": "dependent",
            "dependency": "claim 19",
            "is_exemplary": true
          },
          {
            "claim_number": "00030",
            "claim_text": "30. An apparatus configured for wireless communication, the apparatus comprising:\na memory; and\nat least one processor in electrical communication with the memory, wherein the at least one processor is configured to cause the apparatus to:\ntransmit, by a base station, resource allocation indicating data tones and peak reduction tones (PRTs) with respect to each component carrier (CCs) of a plurality of CCs, wherein the resource allocation indicates data tone locations within a first bandwidth of a first CC of the plurality of CCs and within a second bandwidth of a second CC of the plurality of CCs, and wherein the resource allocation indicates PRT locations within at least one of the first bandwidth or the second bandwidth according to one or more PRT location sequences; and\nreceive, by the base station, a data transmission comprising one or more waveforms configured according to the resource allocation.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00031",
            "claim_text": "31. The apparatus of claim 30, wherein the one or more PRT location sequences provide a PRT sideband location configuration relative to data tones of the first CC, the second CC, or both.",
            "claim_type": "dependent",
            "dependency": "claim 30",
            "is_exemplary": true
          },
          {
            "claim_number": "00032",
            "claim_text": "32. The apparatus of claim 30, wherein the one or more PRT location sequences include a first PRT location sequence of a plurality of contiguously located PRTs, and wherein the contiguously located PRTs of the first PRT location sequence are located within the first bandwidth of the first CC and are configured such that peak to average power ratio (PAPR) of a waveform of the one or more waveforms corresponding to the first CC and of a waveform of the one or more waveforms corresponding to the second CC satisfies a PAPR threshold.",
            "claim_type": "dependent",
            "dependency": "claim 30",
            "is_exemplary": true
          },
          {
            "claim_number": "00033",
            "claim_text": "33. The apparatus of claim 30, wherein the one or more PRT location sequences provide a PRT inband location configuration relative to data tones of the first CC, the second CC, or both.",
            "claim_type": "dependent",
            "dependency": "claim 30",
            "is_exemplary": true
          },
          {
            "claim_number": "00034",
            "claim_text": "34. The apparatus of claim 30, wherein the one or more PRT location sequences include a first PRT location sequence of a plurality of distributively located PRTs, and wherein the distributively located PRTs of the first PRT location sequence are located within the first bandwidth of the first CC interleaved with data tones of the first CC and are configured such that peak to average power ratio (PAPR) of a waveform of the one or more waveforms corresponding to the first CC satisfies a PAPR threshold.",
            "claim_type": "dependent",
            "dependency": "claim 30",
            "is_exemplary": true
          },
          {
            "claim_number": "00035",
            "claim_text": "35. The apparatus of claim 30, wherein the first CC and the second CC are CCs of an intra-band carrier aggregation (CA) configuration, and wherein the first bandwidth of the first CC and the second bandwidth of the second CC are within a first frequency range predefined for the intra-band CA configuration.",
            "claim_type": "dependent",
            "dependency": "claim 30",
            "is_exemplary": true
          },
          {
            "claim_number": "00036",
            "claim_text": "36. The apparatus of claim 30, wherein the first CC and the second CC are CCs of a carrier aggregation (CA) configuration, and wherein a frequency range of the first bandwidth of the first CC and a frequency range of the second bandwidth of the second CC are contiguous.",
            "claim_type": "dependent",
            "dependency": "claim 30",
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.6,
        "publication_date": "2023-11-14",
        "patent_year": 2023
      },
      {
        "patent_id": "11711862",
        "title": "Dual connectivity and carrier aggregation band selection",
        "abstract": "The disclosed technology provides a system and method for allocating frequency bands to a mobile device or user equipment (UE) based on priorities assigned to the different frequency bands. When no priority is assigned to the frequency bands, when a special or reserved priority is assigned, or when equal priority is assigned, the frequency band allocation to the UE is based on a default frequency allocation algorithm (e.g., based on a relative bandwidth of the different frequency bands). When a UE is capable of utilizing a first and a second frequency band, and the priority assigned to the first frequency band is higher than the priority assigned to the second frequency band, the network (e.g., eNB/gNB) overrides the default algorithm and preferentially allocates the first frequency band to UE even when the first frequency band has a smaller bandwidth than the second frequency band or when the default algorithm would otherwise prefer the first frequency band.",
        "inventors": [
          "Nishant Patel"
        ],
        "assignees": [
          "T-Mobile USA, Inc."
        ],
        "claims": [
          {
            "claim_number": "00001",
            "claim_text": "1. At least one computer-readable storage medium, excluding transitory signals and carrying instructions, which, when executed by at least one data processor of a system, cause the system to:\ndetermine that a mobile device is capable of operating on a first frequency band and a second frequency band,\nwherein the mobile device is configured to operate in a New Radio (NR) carrier aggregation mode, a NR dual connectivity mode, or an Evolved Universal Mobile Telecommunications System Terrestrial Radio Access Network (EUTRAN) NR dual connectivity (EN-DC) mode;\n\ndetermine a priority indicator assigned to the first frequency band and the second frequency band in response to determining that the mobile device is capable of operating on the first frequency band and the second frequency band;\nallocate the mobile device with component carriers in the first frequency band or the second frequency band according to a first algorithm in response to determining that there is no priority indicator assigned to the first frequency band and to the second frequency band; and,\nallocate the mobile device with component carriers in the first frequency band in response to determining that a first priority indicator assigned to the first frequency band indicates a higher priority than a second priority indicator assigned to the second frequency band,\nwherein allocating the mobile device with the component carriers in the first frequency band is according to a second algorithm, different from the first algorithm.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00002",
            "claim_text": "2. The at least one computer-readable storage medium of claim 1, wherein the system is further caused to:\nallocate the mobile device with component carriers in the first frequency band or the second frequency band according to the first algorithm in response to determining that the first priority indicator assigned to the first frequency band indicates a same priority as a second priority indicator assigned to the second frequency band.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00003",
            "claim_text": "3. The at least one computer-readable storage medium of claim 1, wherein the system is further caused to:\nallocate the mobile device with component carriers in the first frequency band or the second frequency band according to the first algorithm in response to determining that there is no priority indicator assigned to the first frequency band and the priority indicator assigned to the second frequency band indicates a first reserved priority indicator.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00004",
            "claim_text": "4. The at least one computer-readable storage medium of claim 1, wherein the system is further caused to:\nallocate the mobile device with component carriers in the first frequency band according to the first algorithm in response to determining that there is no priority indicator assigned to the first frequency band and the priority indicator assigned to the second frequency band indicates a second reserved priority indicator, wherein the second reserved priority indicator indicates that the second frequency band should not be considered in allocating component carriers to the mobile device.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00005",
            "claim_text": "5. The at least one computer-readable storage medium of claim 1, wherein the first frequency band comprises a smaller bandwidth than the second frequency band.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00006",
            "claim_text": "6. The at least one computer-readable storage medium of claim 1, wherein the first priority indicator and the second priority indicator are based on one or more measurement reports of the first frequency band and the second frequency band.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00007",
            "claim_text": "7. The at least one computer-readable storage medium of claim 1, wherein the first priority indicator and the second priority indicator is assigned by a self-optimizing network (SON) configured to determine the priority indicator based on one or more characteristics of traffic on the first frequency band and the second frequency band, and wherein the one or more characteristics of traffic comprises a number of connected users, a downlink (DL) physical resource block (PRB) utilization, or an uplink (UL) PRB utilization.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00008",
            "claim_text": "8. The at least one computer-readable storage medium of claim 1, wherein the system comprises a gNodeB (gNB) operating in a New Radio (NR) radio access network, wherein the first algorithm is a default algorithm employed by the gNB and wherein the second algorithm is an override algorithm.",
            "claim_type": "dependent",
            "dependency": "claim 1",
            "is_exemplary": true
          },
          {
            "claim_number": "00009",
            "claim_text": "9. A method comprising:\ndetermining whether a priority indicator is assigned to a first frequency band and a second frequency band;\nallocating a user equipment (UE) with component carriers (CCs) in the first frequency band or the second frequency band according to a first frequency allocation scheme in response to determining that there is no priority indicator assigned to the first frequency band and to the second frequency band; and,\nallocating the UE with CCs in the first frequency band in response to determining that a first priority indicator assigned to the first frequency band indicates a higher priority than a second priority indicator assigned to the second frequency band,\nwherein allocating the UE with the CCs in the first frequency band is according to a second frequency allocation scheme, different from the first frequency allocation scheme.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00010",
            "claim_text": "10. The method of claim 9 further comprising:\nallocating the UE with CCs in the first frequency band or the second frequency band according to the first frequency allocation scheme in response to determining that the first priority indicator assigned to the first frequency band indicates a same priority as a second priority indicator assigned to the second frequency band.",
            "claim_type": "dependent",
            "dependency": "claim 9",
            "is_exemplary": true
          },
          {
            "claim_number": "00011",
            "claim_text": "11. The method of claim 9 further comprising:\nallocate the UE with CCs in the first frequency band according to the first frequency allocation scheme in response to determining that there is no priority indicator assigned to the first frequency band and the priority indicator assigned to the second frequency band indicates a second reserved priority indicator, wherein the second reserved priority indicator indicates that the second frequency band should not be considered in allocating component carriers to the UE.",
            "claim_type": "dependent",
            "dependency": "claim 9",
            "is_exemplary": true
          },
          {
            "claim_number": "00012",
            "claim_text": "12. The method of claim 9, wherein the first priority indicator and the second priority indicator is assigned by a self-optimizing network (SON) configured to determine the priority indicator based on one or more characteristics of traffic on the first frequency band and the second frequency band, wherein the one of more characteristics of traffic comprises a number of connected users, a downlink (DL) physical resource block (PRB) utilization, or an uplink (UL) PRB utilization.",
            "claim_type": "dependent",
            "dependency": "claim 9",
            "is_exemplary": true
          },
          {
            "claim_number": "00013",
            "claim_text": "13. A system comprising:\nat least one hardware processor; and\nat least one non-transitory memory, coupled to the at least one hardware processor and storing instructions, which, when executed by the at least one hardware processor, cause the system to:\ndetermine a priority indicator assigned to a first frequency band and a second frequency band;\nallocate a user equipment (UE) with component carriers (CCs) in the first frequency band or the second frequency band according to a default frequency allocation scheme in response to determining that there is no priority indicator assigned to the first frequency band and to the second frequency band; and,\nallocate the UE with CCs in the first frequency band in response to determining that a first priority indicator assigned to the first frequency band indicates a higher priority than a second priority indicator assigned to the second frequency band, wherein allocating the UE with the CCs in the first frequency band is according to an operator-specific frequency allocation scheme, different from the default frequency allocation scheme.",
            "claim_type": "independent",
            "dependency": null,
            "is_exemplary": true
          },
          {
            "claim_number": "00014",
            "claim_text": "14. The system of claim 13 further caused to:\nallocate the UE with CCs in the first frequency band or the second frequency band according to the default frequency allocation scheme in response to determining that the first priority indicator assigned to the first frequency band indicates a same priority as a second priority indicator assigned to the second frequency band.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00015",
            "claim_text": "15. The system of claim 13 further caused to:\nallocate the UE with CCs in the first frequency band or the second frequency band according to the default frequency allocation scheme in response to determining that there is no priority indicator assigned to the first frequency band and the priority indicator assigned to the second frequency band indicates a first reserved priority indicator.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00016",
            "claim_text": "16. The system of claim 13 further caused to:\nallocate the UE with CCs in the first frequency band according to the default frequency allocation scheme in response to determining that there is no priority indicator assigned to the first frequency band and the priority indicator assigned to the second frequency band indicates a second reserved priority indicator, wherein the second reserved priority indicator indicates that the second frequency band should not be considered in allocating component carriers to the UE.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00017",
            "claim_text": "17. The system of claim 13, wherein the first frequency band comprises a smaller bandwidth than the second frequency band.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00018",
            "claim_text": "18. The system of claim 13, wherein the first priority indicator and the second priority indicator are based on one or more measurement reports of the first frequency band and the second frequency band.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00019",
            "claim_text": "19. The system of claim 13, wherein the first priority indicator and the second priority indicator is assigned by a self-optimizing network (SON) configured to determine the priority indicator based on one or more characteristics of traffic on the first frequency band and the second frequency band, wherein the one of more characteristics of traffic comprises a number of connected users, a downlink (DL) physical resource block (PRB) utilization, or an uplink (UL) PRB utilization.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          },
          {
            "claim_number": "00020",
            "claim_text": "20. The system of claim 13, wherein the system comprises gNodeB (gNB) or eNodeB (eNB), and wherein the UE is configured to operate in a New Radio (NR) carrier aggregation mode, a NR dual connectivity mode, or an Evolved Universal Mobile Telecommunications System Terrestrial Radio Access Network (EUTRAN) NR dual connectivity (EN-DC) mode.",
            "claim_type": "dependent",
            "dependency": "claim 13",
            "is_exemplary": true
          }
        ],
        "relevance_score": 0.7,
        "publication_date": "2023-07-25",
        "patent_year": 2023
      },
      {
        "patent_id": "9485774",
        "title": "Efficient transmission of stand-alone aperiodic CSI reporting for LTE carrier aggregation",
        "abstract": "The transmission of stand-alone, aperiodic CSI reports from a UE in carrier aggregation in an LTE network is optimized. The coding rate is indirectly controlled by varying the number of RBs allocated for the CSI report transmission. Two sets of serving cells are established, and the payload of each set is approximated. For each allowable number of RBs and each payload size, a threshold SINR is determined and stored. An initial number of RBs is selected, based on the number of cells. The actual SINR is measured, and compared to the threshold SINR for the number of RBs and payload size. The number of RBs to be allocated is varied based on the comparison, by varying an index into an array of allowable numbers of RBs. Link adaptation is performed based on observed decoding errors, in an outer loop control algorithm that prevents wind up. An optimization for the particular case of one PCell and one SCell is also presented.",
        "inventors": [
          "Jianguo Long",
          "Ping Yu",
          "Girum Fantaye"
        ],
        "assignees": [
          "TELEFONAKTIEBOLAGET LM ERICSSON (PUBL)"
        ],
        "claims": [],
        "relevance_score": 0.7,
        "publication_date": "2016-11-01",
        "patent_year": 2016
      },
      {
        "patent_id": "10772026",
        "title": "Wireless relay quality-of-service based on relay-delivered media services",
        "abstract": "A wireless communication network controls wireless base stations that serve wireless relays that serve wireless User Equipment (UEs). In a relay control system, data transceivers receive configuration data that was transferred by the wireless relays and that indicates their individual wireless media services. Relay control circuitry allocates individual carrier aggregation Quality-of-Service (QoS) levels to the individual wireless relays based on the individual wireless media services. The relay transceivers transfer the individual carrier aggregation QoS levels for the individual wireless relays to the wireless base stations. The wireless base stations serve the wireless relays with the individual carrier aggregation QoS levels. The wireless relays serve the wireless UEs with the wireless media services.",
        "inventors": [
          "Vanil Parihar",
          "Nitesh Manchanda"
        ],
        "assignees": [
          "SPRINT COMMUNICATIONS COMPANY, L.P."
        ],
        "claims": [],
        "relevance_score": 0.7,
        "publication_date": "2020-09-08",
        "patent_year": 2020
      }
    ],
    "search_strategies": [
      {
        "name": "AI Techniques in Carrier Aggregation",
        "description": "This strategy focuses on patents that specifically mention AI techniques applied to carrier aggregation, ensuring that both AI and carrier aggregation are present in the text.",
        "query": {
          "_and": [
            {
              "_text_phrase": {
                "patent_title": "carrier aggregation"
              }
            },
            {
              "_text_any": {
                "patent_abstract": "AI artificial intelligence machine learning"
              }
            }
          ]
        },
        "expected_results": 20,
        "priority": 1
      },
      {
        "name": "Dynamic Spectrum Management with AI",
        "description": "This strategy targets patents that discuss dynamic spectrum management in the context of carrier aggregation, emphasizing the role of AI in optimizing spectrum usage.",
        "query": {
          "_and": [
            {
              "_text_phrase": {
                "patent_title": "dynamic spectrum management"
              }
            },
            {
              "_text_phrase": {
                "patent_abstract": "carrier aggregation"
              }
            },
            {
              "_text_any": {
                "patent_abstract": "AI machine learning"
              }
            }
          ]
        },
        "expected_results": 15,
        "priority": 2
      },
      {
        "name": "AI-Enhanced Network Performance",
        "description": "This strategy aims to find patents that describe how AI enhances network performance through carrier aggregation techniques, focusing on performance metrics.",
        "query": {
          "_and": [
            {
              "_text_phrase": {
                "patent_title": "network performance"
              }
            },
            {
              "_text_phrase": {
                "patent_abstract": "carrier aggregation"
              }
            },
            {
              "_text_any": {
                "patent_abstract": "AI optimization"
              }
            }
          ]
        },
        "expected_results": 25,
        "priority": 3
      },
      {
        "name": "AI Algorithms for Carrier Aggregation",
        "description": "This strategy is designed to uncover patents that specifically mention algorithms used in AI for carrier aggregation, ensuring a focus on technical implementations.",
        "query": {
          "_and": [
            {
              "_text_phrase": {
                "patent_title": "carrier aggregation"
              }
            },
            {
              "_text_any": {
                "patent_abstract": "algorithm AI machine learning"
              }
            }
          ]
        },
        "expected_results": 18,
        "priority": 4
      },
      {
        "name": "AI and QoS in Carrier Aggregation",
        "description": "This strategy seeks patents that explore the intersection of AI and Quality of Service (QoS) in carrier aggregation scenarios, focusing on user experience improvements.",
        "query": {
          "_and": [
            {
              "_text_phrase": {
                "patent_title": "Quality of Service"
              }
            },
            {
              "_text_phrase": {
                "patent_abstract": "carrier aggregation"
              }
            },
            {
              "_text_any": {
                "patent_abstract": "AI user experience"
              }
            }
          ]
        },
        "expected_results": 12,
        "priority": 5
      }
    ],
    "timestamp": "2025-08-22T23:56:43.631880",
    "metadata": {
      "relevance_threshold": 0.3,
      "max_results": 20,
      "unique_patents_found": 10,
      "strategies_executed": 5
    }
  }
}
```

---
Generated by Direct Prior Art API Tester
