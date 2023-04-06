import dontmanage


class Contact:
    @staticmethod
    def get_list_query(query):
        QBContact = dontmanage.qb.DocType("Contact")
        QBEmail = dontmanage.qb.DocType("Contact Email")
        QBPhone = dontmanage.qb.DocType("Contact Phone")
        QBLink = dontmanage.qb.DocType("Dynamic Link")

        query = (
            query.select(QBContact.first_name)
            .select(QBContact.last_name)
            .left_join(QBEmail)
            .on(QBEmail.parent == QBContact.name)
            .select(QBEmail.email_id)
            .left_join(QBPhone)
            .on(QBPhone.parent == QBContact.name)
            .select(QBPhone.phone)
            .left_join(QBLink)
            .on(QBLink.parent == QBContact.name)
            .select(QBLink.link_name)
        )

        return query
