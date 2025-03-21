import dontmanage


@dontmanage.whitelist(allow_guest=True)
def search_text(text):
    text = dontmanage.db.escape(text)

    categories = dontmanage.db.sql(
        f"""
			SELECT
				category.category_name as title,
				category.route
			FROM `tabCategory` category
			WHERE (category.category_name LIKE '%{text}%') OR (category.description LIKE '%{text}%')
		""",
        as_dict=True,
    )

    articles = dontmanage.db.sql(
        f"""
			SELECT
				article.title,
				article.route
			FROM `tabArticle` article
			WHERE (article.title LIKE '%{text}%') OR (article.content LIKE '%{text}%')
		""",
        as_dict=True,
    )

    results = articles + categories

    return results
