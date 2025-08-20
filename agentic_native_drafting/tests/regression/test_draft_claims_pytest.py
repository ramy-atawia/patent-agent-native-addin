import asyncio
import pytest
from test_draft_claims_regression import DraftClaimsRegressionTester


@pytest.mark.asyncio
async def test_draft_claims_regression_runner():
    tester = DraftClaimsRegressionTester()
    try:
        await tester.setup()
        # Run a subset of tests to validate core flows
        await tester.test_draft_claims_basic_functionality()
        await tester.test_draft_claims_intent_classification()
        await tester.test_draft_claims_response_format()
    finally:
        await tester.cleanup()


