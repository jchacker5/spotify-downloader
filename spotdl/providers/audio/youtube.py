"""
Youtube module for downloading and searching songs.
"""

from typing import Any, Dict, List, Optional

import logging

from pytube import Search
from pytube import YouTube as PyTube

from spotdl.providers.audio.base import AudioProvider
from spotdl.types.result import Result


logger = logging.getLogger(__name__)

__all__ = ["YouTube"]


class YouTube(AudioProvider):
    """
    YouTube audio provider class
    """

    SUPPORTS_ISRC = False
    GET_RESULTS_OPTS: List[Dict[str, Any]] = [{}]

    def get_results(
        self, search_term: str, *_args, **_kwargs
    ) -> List[Result]:  # pylint: disable=W0221
        """
        Get results from YouTube

        ### Arguments
        - search_term: The search term to search for.
        - args: Unused.
        - kwargs: Unused.

        ### Returns
        - A list of YouTube results if found, None otherwise.
        """

        search_results: Optional[List[PyTube]] = Search(search_term).results

        if not search_results:
            return []

        results = []
        for result in search_results:
            if result.watch_url:
                try:
                    duration = result.length
                except Exception:
                    duration = 0
                # skip duration over 3600 seconds
                if duration > 3600:
                    logger.debug(
                        "Ignoring video with duration over 3600 seconds: %s",
                        result.watch_url,
                    )
                    continue
                try:
                    views = result.views
                except Exception:
                    views = 0

                results.append(
                    Result(
                        source=self.name,
                        url=result.watch_url,
                        verified=False,
                        name=result.title,
                        duration=duration,
                        author=result.author,
                        search_query=search_term,
                        views=views,
                        result_id=result.video_id,
                    )
                )

        return results
