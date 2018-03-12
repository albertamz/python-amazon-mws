"""
Amazon MWS Feeds API
"""
from __future__ import absolute_import

from ..mws import MWS
from .. import utils
from ..decorators import next_token_action

# TODO Add FeedProcessingStatus enumeration
# TODO Add FeedType enumeration


class Feeds(MWS):
    """
    Amazon MWS Feeds API

    Docs:
    http://docs.developer.amazonservices.com/en_US/feeds/Feeds_Overview.html
    """
    ACCOUNT_TYPE = "Merchant"

    NEXT_TOKEN_OPERATIONS = [
        'GetFeedSubmissionList',
    ]

    def submit_feed(self, feed, feed_type, marketplaceids=None,
                    content_type="text/xml", purge='false'):
        """
        Uploads a feed for processing by Amazon MWS.
        `feed` should contain a file object in XML or flat-file format.

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_SubmitFeed.html
        """
        data = {
            'Action': 'SubmitFeed',
            'FeedType': feed_type,
            'PurgeAndReplace': purge,
        }
        data.update(utils.enumerate_param('MarketplaceIdList.Id.', marketplaceids))
        md5_hash = utils.calc_md5(feed)
        return self.make_request(data, method="POST", body=feed,
                                 extra_headers={'Content-MD5': md5_hash, 'Content-Type': content_type})

    @next_token_action('GetFeedSubmissionList')
    def get_feed_submission_list(self, feedids=None, max_count=None, feedtypes=None,
                                 processingstatuses=None, fromdate=None, todate=None,
                                 next_token=None):
        """
        Returns a list of all feed submissions submitted between `fromdate` and `todate`.
        If these parameters are ommitted, defaults to the previous 90 days.

        Pass `next_token` to call "GetFeedSubmissionListByNextToken" instead.

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionList.html
        """
        data = {
            'Action': 'GetFeedSubmissionList',
            'MaxCount': max_count,
            'SubmittedFromDate': fromdate,
            'SubmittedToDate': todate,
        }
        data.update(utils.enumerate_param('FeedSubmissionIdList.Id', feedids))
        data.update(utils.enumerate_param('FeedTypeList.Type.', feedtypes))
        data.update(utils.enumerate_param('FeedProcessingStatusList.Status.', processingstatuses))
        return self.make_request(data)

    def get_submission_list_by_next_token(self, token):
        """
        Alias for `get_feed_submission_list(next_token=token)`

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionListByNextToken.html
        """
        return self.get_feed_submission_list(next_token=token)

    def get_feed_submission_count(self, feedtypes=None, processingstatuses=None, fromdate=None, todate=None):
        """
        Returns a count of the feeds submitted between `fromdate` and `todate`.
        If these parameters are ommitted, defaults to the previous 90 days.

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionCount.html
        """
        data = {
            'Action': 'GetFeedSubmissionCount',
            'SubmittedFromDate': fromdate,
            'SubmittedToDate': todate,
        }
        data.update(utils.enumerate_param('FeedTypeList.Type.', feedtypes))
        data.update(utils.enumerate_param('FeedProcessingStatusList.Status.', processingstatuses))
        return self.make_request(data)

    def cancel_feed_submissions(self, feedids=None, feedtypes=None, fromdate=None, todate=None):
        """
        Cancels one or more feed submissions and returns a count of the feed submissions that were canceled.

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_CancelFeedSubmissions.html
        """
        data = {
            'Action': 'CancelFeedSubmissions',
            'SubmittedFromDate': fromdate,
            'SubmittedToDate': todate,
        }
        data.update(utils.enumerate_param('FeedSubmissionIdList.Id.', feedids))
        data.update(utils.enumerate_param('FeedTypeList.Type.', feedtypes))
        return self.make_request(data)

    def get_feed_submission_result(self, feedid):
        """
        Returns the feed processing report and the Content-MD5 header.

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionResult.html
        """
        data = {
            'Action': 'GetFeedSubmissionResult',
            'FeedSubmissionId': feedid,
        }
        return self.make_request(data, rootkey='Message')