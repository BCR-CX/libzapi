import libzapi.infrastructure.api_clients.help_center as api
from libzapi.application.services.help_center.account_custom_claims_service import AccountCustomClaimsService
from libzapi.application.services.help_center.article_attachments_service import ArticleAttachmentsService
from libzapi.application.services.help_center.article_comments_service import ArticleCommentsService
from libzapi.application.services.help_center.article_labels_service import ArticleLabelsService
from libzapi.application.services.help_center.articles_service import ArticlesService
from libzapi.application.services.help_center.badge_assignments_service import BadgeAssignmentsService
from libzapi.application.services.help_center.badge_categories_service import BadgeCategoriesService
from libzapi.application.services.help_center.badges_service import BadgesService
from libzapi.application.services.help_center.categories_service import CategoriesService
from libzapi.application.services.help_center.content_subscriptions_service import ContentSubscriptionsService
from libzapi.application.services.help_center.content_tags_service import ContentTagsService
from libzapi.application.services.help_center.guide_media_service import GuideMediaService
from libzapi.application.services.help_center.permission_groups_service import PermissionGroupsService
from libzapi.application.services.help_center.post_comments_service import PostCommentsService
from libzapi.application.services.help_center.posts_service import PostsService
from libzapi.application.services.help_center.redirect_rules_service import RedirectRulesService
from libzapi.application.services.help_center.search_service import SearchService
from libzapi.application.services.help_center.sections_service import SectionsService
from libzapi.application.services.help_center.themes_service import ThemesService
from libzapi.application.services.help_center.topics_service import TopicsService
from libzapi.application.services.help_center.translations_service import TranslationsService
from libzapi.application.services.help_center.user_segments_service import UserSegmentsService
from libzapi.application.services.help_center.user_subscriptions_service import UserSubscriptionsService
from libzapi.application.services.help_center.votes_service import VotesService

from libzapi.infrastructure.http.auth import api_token_headers, oauth_headers
from libzapi.infrastructure.http.client import HttpClient


class HelpCenter:
    def __init__(
        self, base_url: str, oauth_token: str | None = None, email: str | None = None, api_token: str | None = None
    ):
        if oauth_token:
            headers = oauth_headers(oauth_token)
        elif email and api_token:
            headers = api_token_headers(email, api_token)
        else:
            raise ValueError("Provide oauth_token or email+api_token")

        http = HttpClient(base_url, headers=headers)

        # Initialize services
        self.account_custom_claims = AccountCustomClaimsService(api.AccountCustomClaimApiClient(http))
        self.articles = ArticlesService(api.ArticleApiClient(http))
        self.articles_attachments = ArticleAttachmentsService(api.ArticleAttachmentApiClient(http))
        self.article_comments = ArticleCommentsService(api.ArticleCommentApiClient(http))
        self.article_labels = ArticleLabelsService(api.ArticleLabelApiClient(http))
        self.badges = BadgesService(api.BadgeApiClient(http))
        self.badge_assignments = BadgeAssignmentsService(api.BadgeAssignmentApiClient(http))
        self.badge_categories = BadgeCategoriesService(api.BadgeCategoryApiClient(http))
        self.categories = CategoriesService(api.CategoryApiClient(http))
        self.content_subscriptions = ContentSubscriptionsService(api.ContentSubscriptionApiClient(http))
        self.content_tags = ContentTagsService(api.ContentTagApiClient(http))
        self.guide_media = GuideMediaService(api.GuideMediaApiClient(http))
        self.permission_groups = PermissionGroupsService(api.PermissionGroupApiClient(http))
        self.posts = PostsService(api.PostApiClient(http))
        self.post_comments = PostCommentsService(api.PostCommentApiClient(http))
        self.redirect_rules = RedirectRulesService(api.RedirectRuleApiClient(http))
        self.search = SearchService(api.SearchApiClient(http))
        self.sections = SectionsService(api.SectionApiClient(http))
        self.themes = ThemesService(api.ThemeApiClient(http))
        self.topics = TopicsService(api.TopicApiClient(http))
        self.translations = TranslationsService(api.TranslationApiClient(http))
        self.user_segments = UserSegmentsService(api.UserSegmentApiClient(http))
        self.user_subscriptions = UserSubscriptionsService(api.UserSubscriptionApiClient(http))
        self.votes = VotesService(api.VoteApiClient(http))
