#!/usr/bin/env python3

# Check the prompt length that's causing the 400 error
prompt = """You are an expert patent attorney and technology analyst specializing in comprehensive prior art search. Generate sophisticated patent search strategies for: "prior art search report for 5G dynamic spectrum sharing with QoS"

TECHNICAL PRECISION RULES:
1. Extract compound technical terms (e.g., "machine learning algorithm" → ["machine learning", "algorithm", "ML", "artificial intelligence"])
2. Include domain-specific terminology and abbreviations
3. Consider broader conceptual terms and narrower specific implementations
4. Add related technical standards, protocols, or methodologies
5. Include alternative technical approaches that achieve similar outcomes

BANNED WORDS (avoid these in queries):
- "system", "method", "apparatus", "device", "means", "invention"
- "improved", "enhanced", "novel", "new", "better"
- "comprising", "including", "having", "wherein"
- Common legal/procedural terms that don't add technical value

SEARCH STRATEGY TYPES:
1. CORE_TECHNICAL: Direct technical terms and primary concepts
2. DOMAIN_SPECIFIC: Industry terminology and domain standards  
3. FUNCTIONAL_ALTERNATIVE: Different technical approaches achieving same function
4. COMPONENT_FOCUSED: Individual technical components and sub-systems
5. STANDARDS_PROTOCOLS: Related technical standards, APIs, protocols
6. INVENTOR_ASSIGNEE: Key players and organizations in the technology space

QUERY FIELD OPTIMIZATION:
- patent_title: 3-5 most critical terms (highest precision)
- patent_abstract: 7-10 descriptive terms (broader coverage)
- patent_claims: Technical implementation details (functional aspects)
- Use field combinations for maximum coverage

PATENTSVIEW API SYNTAX (SIMPLIFIED FOR COMPATIBILITY):
- Use "_text_any" for broad field matching across multiple fields
- Use simple "_and" and "_or" constructs 
- Avoid deeply nested Boolean logic
- Focus on field-specific searches: patent_title, patent_abstract, patent_claims
- Use comma-separated terms within fields for better matching

Return ONLY a JSON array with this structure:
[
    {{
        "name": "STRATEGY_NAME",
        "description": "detailed strategy explanation",
        "query": {{
            "_text_any": {{
                "patent_title": "primary technical terms",
                "patent_abstract": "broader descriptive terms"
            }}
        }},
        "expected_results": 15,
        "priority": 1,
        "technical_focus": "primary technical domain",
        "coverage_scope": "NARROW|MEDIUM|BROAD"
    }}
]

SPECIFIC REQUIREMENTS:
- Generate exactly 5 diverse strategies covering different technical angles
- Each strategy should target different aspects of the technology
- Include both narrow precision searches and broader conceptual searches
- Ensure comprehensive coverage of the technical domain
- Optimize for PatentsView API field-specific searching
- Include compound Boolean logic where appropriate
- Consider temporal aspects (recent innovations vs. foundational patents)

STRATEGY COVERAGE MATRIX:
1. Strategy 1: Core technical implementation (NARROW scope)
2. Strategy 2: Alternative technical approaches (MEDIUM scope) 
3. Strategy 3: Component/subsystem focus (NARROW scope)
4. Strategy 4: Domain standards and protocols (MEDIUM scope)
5. Strategy 5: Broader conceptual and functional coverage (BROAD scope)

Generate sophisticated queries that maximize relevant patent discovery while minimizing noise."""

print(f"Prompt length: {len(prompt)} characters")
print(f"Estimated tokens: {len(prompt.split()) * 1.3:.0f} tokens")
print(f"Lines: {len(prompt.splitlines())}")
print(f"Words: {len(prompt.split())}")

# Check if there are any problematic characters
import re
problematic_chars = re.findall(r'[^\x00-\x7F]', prompt)
if problematic_chars:
    print(f"Problematic characters found: {set(problematic_chars)}")
else:
    print("No problematic characters found")
