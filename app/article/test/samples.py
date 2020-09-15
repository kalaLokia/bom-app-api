from core.models import Article, Color, ArticleInfo


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


def article_info(user, article, color, **params):
    """
    Creates a sample article info, also accepts models
    "article", "color" in params.
    """

    defaults = {
        'article': article,
        'color': color,
        'category': 'g',
        'price': 270.00
    }
    defaults.update(params)
    artid = "{}-{}-{}".format(defaults['article'].artno,
                              defaults['color'].code, defaults['category'])
    defaults.update({'artid': artid})

    return ArticleInfo.objects.create(user=user, **defaults)
