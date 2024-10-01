def selected_matches(matches, player_name):
    """Custom filter"""
    if player_name:
        filtered_matches = []
        for match in matches:
            if match.Player1.name == player_name:
                filtered_matches.append(match)
            elif match.Player2.name == player_name:
                filtered_matches.append(match)
        return filtered_matches
    return matches
