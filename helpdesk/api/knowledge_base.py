import dontmanage
from bs4 import BeautifulSoup
from dontmanage import _
from dontmanage.rate_limiter import rate_limit
from dontmanage.utils import get_user_info_for_avatar

from helpdesk.utils import is_agent


@dontmanage.whitelist(allow_guest=True)
def get_article(name: str):
    article = dontmanage.get_doc("HD Article", name).as_dict()

    if not is_agent() and article["status"] != "Published":
        dontmanage.throw(_("Access denied"), dontmanage.PermissionError)

    author = get_user_info_for_avatar(article["author"])
    feedback = (
        dontmanage.db.get_value(
            "HD Article Feedback",
            {"article": name, "user": dontmanage.session.user},
            "feedback",
        )
        or 0
    )

    return {
        "name": article.name,
        "title": article.title,
        "content": article.content,
        "author": author,
        "creation": article.creation,
        "status": article.status,
        "published_on": article.published_on,
        "modified": article.modified,
        "category_name": dontmanage.db.get_value(
            "HD Article Category", article.category, "category_name"
        ),
        "category_id": article.category,
        "feedback": int(feedback),
    }

    return article


@dontmanage.whitelist()
def delete_articles(articles):
    for article in articles:
        dontmanage.delete_doc("HD Article", article)


@dontmanage.whitelist()
def create_category(title: str):
    category = dontmanage.new_doc("HD Article Category", category_name=title).insert()
    article = dontmanage.new_doc(
        "HD Article", title="New Article", category=category.name
    ).insert()
    return {"article": article.name, "category": category.name}


@dontmanage.whitelist()
def move_to_category(category, articles):
    for article in articles:
        try:
            article_category = dontmanage.db.get_value("HD Article", article, "category")
            category_existing_articles = dontmanage.db.count(
                "HD Article", {"category": article_category}
            )
            if category_existing_articles == 1:
                dontmanage.throw(_("Category must have atleast one article"))
                return
            else:
                dontmanage.db.set_value(
                    "HD Article", article, "category", category, update_modified=False
                )
        except Exception as e:
            dontmanage.db.rollback()
            dontmanage.throw(_("Error moving article to category"))


@dontmanage.whitelist()
def get_categories():
    categories = dontmanage.get_all(
        "HD Article Category",
        fields=["name", "category_name", "modified"],
    )
    for c in categories:
        c["article_count"] = dontmanage.db.count(
            "HD Article", filters={"category": c.name, "status": "Published"}
        )

    categories.sort(key=lambda c: c["article_count"], reverse=True)
    categories = [c for c in categories if c["article_count"] > 0]
    return categories


@dontmanage.whitelist()
def get_category_articles(category):
    articles = dontmanage.get_all(
        "HD Article",
        filters={"category": category, "status": "Published"},
        fields=["name", "title", "published_on", "modified", "author", "content"],
    )
    for article in articles:
        article["author"] = get_user_info_for_avatar(article["author"])
        soup = BeautifulSoup(article["content"], "html.parser")
        article["content"] = str(soup.text)[:100]

    return articles


@dontmanage.whitelist()
def merge_category(source, target):
    if source == target:
        dontmanage.throw(_("Source and target category cannot be same"))
    general_category = get_general_category()
    if source == general_category:
        dontmanage.throw(_("Cannot merge General category"))
    source_articles = dontmanage.get_all(
        "HD Article",
        filters={"category": source},
        pluck="name",
    )
    for article in source_articles:
        dontmanage.db.set_value(
            "HD Article", article, "category", target, update_modified=False
        )

    dontmanage.delete_doc("HD Article Category", source)


@dontmanage.whitelist()
def get_general_category():
    return dontmanage.db.get_value(
        "HD Article Category", {"category_name": "General"}, "name"
    )


@dontmanage.whitelist()
def get_category_title(category):
    return dontmanage.db.get_value("HD Article Category", category, "category_name")


@dontmanage.whitelist()
@rate_limit(key="article", seconds=60 * 60)
def increment_views(article):
    views = dontmanage.db.get_value("HD Article", article, "views") or 0
    views += 1
    dontmanage.db.set_value("HD Article", article, "views", views, update_modified=False)
