import requests

def github_repos(user):
    """Fetch public GitHub repositories for a given user.
    Args:
        user (str): GitHub username
    Returns:
        list: List of tuples (repo_name, repo_url)
    """
    url = f"https://api.github.com/users/{user}/repos"
    response = requests.get(url)
    response.raise_for_status()
    return [(repo["name"], repo["html_url"]) for repo in response.json()]

def generate_portfolio_html(user, repos, output_path="portfolio.html"):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"<h1>{user}'s Projects</h1><ul>")
        for name, url in repos:
            f.write(f"<li><a href='{url}' target='_blank'>{name}</a></li>")
        f.write("</ul>")
    return output_path
