# Copyright (c) 2021, DontManage Technologies and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document
from dontmanage.query_builder import DocType
from dontmanage.utils import cint


class HDArticle(Document):
	@staticmethod
	def get_list_filters(query):
		QBArticle = DocType("HD Article")
		QBCategory = DocType("HD Article Category")

		query = (
			query.where(QBArticle.status != "Archived")
			.left_join(QBCategory)
			.on(QBCategory.name == QBArticle.category)
			.select(QBCategory.category_name)
			.select(
				QBArticle.title,
				QBArticle.status,
				QBArticle.views,
				QBArticle.author,
				QBArticle.modified,
			)
		)

		return query

	def before_insert(self):
		self.author = dontmanage.session.user

	def before_save(self):
		# set published date of the hd_article
		if self.status == "Published" and not self.published_on:
			self.published_on = dontmanage.utils.now()
		elif self.status == "Draft" and self.published_on:
			self.published_on = None

		if self.status == "Archived" and self.category != None:
			self.category = None

		# index is only set if its not set already, this allows defining index
		# at the time of creation itself if not set the index is set to the
		# last index + 1, i.e. the hd_article is added at the end
		if self.status == "Published" and self.idx == -1:
			self.idx = cint(
				dontmanage.db.count(
					"HD Article", {"category": self.category}, {"status": "Published"}
				)
			)

	@property
	def title_slug(self) -> str:
		"""
		Generate slug from article title.
		Example: "Introduction to DontManage Helpdesk" -> "introduction-to-dontmanage-helpdesk"

		:return: Generated slug
		"""
		return self.title.lower().replace(" ", "-")

	def get_breadcrumbs(self):
		breadcrumbs = [{"name": self.name, "label": self.title}]
		current_category = dontmanage.get_doc("Category", self.category)
		breadcrumbs.append(
			{"name": current_category.name, "label": current_category.category_name}
		)
		while current_category.parent_category:
			current_category = dontmanage.get_doc(
				"Category", current_category.parent_category
			)
			breadcrumbs.append(
				{"name": current_category.name, "label": current_category.category_name}
			)
		return breadcrumbs[::-1]


@dontmanage.whitelist(allow_guest=True)
def add_feedback(hd_article, helpful):
	# TODO: use a base 5 or 10 rating system instead of a boolean
	field = "helpful" if helpful else "not_helpful"

	value = cint(dontmanage.db.get_value("HD Article", hd_article, field))
	dontmanage.db.set_value(
		"HD Article", hd_article, field, value + 1, update_modified=False
	)


@dontmanage.whitelist(allow_guest=True)
def increment_view(hd_article):
	value = cint(dontmanage.db.get_value("HD Article", hd_article, "views"))
	dontmanage.db.set_value(
		"HD Article", hd_article, "views", value + 1, update_modified=False
	)
