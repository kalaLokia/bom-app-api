"""
A common module for creating Article, ArticleInfo, Color models.
This applies to all "test" files that requires the above models.
"""
from core.models import Article, Color, ArticleInfo, categorize


def article(user, **params):
    """Create and return a sample article"""
    defaults = {
        'artno': '3290',
        'brand': 'pride',
        'style': 'covering'
    }
    defaults.update(params)

    return Article.objects.create(user=user, **defaults)


def color(user, **params):
    """Creates a sample color"""
    defaults = {
        'code': 'bk',
        'name': 'black'
    }
    defaults.update(params)

    return Color.objects.create(user=user, **defaults)


def article_info(user, **params):
    """
    Creates a sample article info.
    Required fields: "article", "color" in params.
    """

    defaults = {
        'category': 'g',
        'price': 270.00
    }
    defaults.update(params)
    artid = "{}-{}-{}".format(defaults['article'].artno,
                              defaults['color'].code, defaults['category'])
    mcategory = categorize(defaults['category'])
    defaults.update({'artid': artid, 'mcategory': mcategory})

    return ArticleInfo.objects.create(user=user, **defaults)
