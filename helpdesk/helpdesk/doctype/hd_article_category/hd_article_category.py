# Copyright (c) 2021, DontManage Technologies and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import cint
from pypika.functions import Count
from pypika.queries import Query


class HDArticleCategory(Document):
	@staticmethod
	def get_list_select(query: Query):
		QBCategory = dontmanage.qb.DocType("HD Article Category")
		QBArticle = dontmanage.qb.DocType("HD Article")
		count_article = (
			dontmanage.qb.from_(QBArticle)
			.select(Count("*"))
			.as_("count_article")
			.where(QBArticle.category == QBCategory.name)
		)
		query = query.select(QBCategory.star).select(count_article)
		return query

	def before_save(self):
		if self.idx == -1 and self.status == "Published":
			# index is only set if its not set already, this allows defining
			# index at the time of creation itself if not set the index is set
			# to the last index + 1, i.e. the category is added at the end
			self.idx = cint(
				dontmanage.db.count(
					"HD Article Category", {"parent_category": self.parent_category}
				)
			)

	def archive(self):
		self.idx = -1
		self.status = "Archived"
		self.save()

	def unarchive(self):
		self.status = "Published"
		self.save()

	def get_breadcrumbs(self):
		breadcrumbs = [{"name": self.name, "label": self.category_name}]
		current_category = self
		while current_category.parent_category:
			current_category = dontmanage.get_doc(
				"HD Article Category", current_category.parent_category
			)
			breadcrumbs.append(
				{"name": current_category.name, "label": current_category.category_name}
			)
		return breadcrumbs[::-1]
