import asyncio
import sys
import os
import pytest

# Ensure src path is on PYTHONPATH for test discovery
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_PATH = os.path.join(ROOT, 'src')
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from prior_art_search import search_prior_art


@pytest.mark.asyncio
@pytest.mark.parametrize("query", [
    "AI for 5G",
    "AI for fintech",
    "carrier aggregation energy saving"
])
async def test_search_prior_art_basic(query):
    # Run a short prior art search (max_results=3 to keep test time reasonable)
    result = await search_prior_art(query, max_results=3)
    assert result is not None
    assert result.query == query
    assert isinstance(result.patents, list)
    assert isinstance(result.total_patents_found, int)
    # total_patents_found may be 0 in offline environments, but the call should not error
    assert result.total_patents_found >= 0


