import dontmanage


def execute():
    teams = dontmanage.get_all("HD Team", pluck="name")
    for team in teams:
        existing_agents = dontmanage.get_all(
            "HD Team Item", filters={"team": team}, pluck="parent"
        )  # agents in HD Agent doctype
        team_users = dontmanage.get_all(
            "HD Team Member", filters={"parent": team}, pluck="user"
        )  # agents in HD Team doctype

        for agent in existing_agents:
            is_agent_active = dontmanage.get_value("HD Agent", agent, "is_active")
            if is_agent_active and agent not in team_users:
                team_doc = (
                    dontmanage.get_doc("HD Team", team)
                    .append("users", {"user": agent})
                    .save()
                )
                print("Agent Added")
