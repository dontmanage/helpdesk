import dontmanage

from helpdesk.consts import DEFAULT_ARTICLE_CATEGORY


def execute():
    default_category = dontmanage.db.exists(
        "HD Article Category", {"category_name": DEFAULT_ARTICLE_CATEGORY}
    )
    if not default_category:
        default_category = dontmanage.get_doc(
            {
                "doctype": "HD Article Category",
                "category_name": DEFAULT_ARTICLE_CATEGORY,
            }
        ).insert()
        default_category = default_category.get("name")

    articles = dontmanage.get_all("HD Article", filters={"category": ""}, pluck="name")
    # create one default article for general category
    if len(articles) == 0:
        dontmanage.new_doc(
            "HD Article", title="New Article", category=default_category
        ).insert()
    else:
        for article in articles:
            dontmanage.db.set_value("HD Article", article, "category", default_category)
