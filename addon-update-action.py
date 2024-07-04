import argparse
import yaml
from github import Github

parser = argparse.ArgumentParser()

parser.add_argument(
    "--github_token",
    type=str,
    help="GitHub API Access token.",
    required=True,
)
parser.add_argument(
    "--new_server_version",
    type=str,
    help="The new server tag to use for the release.",
    required=True,
)
parser.add_argument(
    "--pre_release",
    type=str,
    help="Indicates if it's a pre-release (true/false).",
    required=False,
)

if __name__ == "__main__":
    args = parser.parse_args()

    # Authentication using personal access token
    github_token = args.github_token
    github = Github(github_token)

    MAIN = "main"
    OWNER = "xdumaster1"  # Replace with your GitHub username
    ADDON_REPO = "home-assistant-addon"

    addon_repo = github.get_repo(f"{OWNER}/{ADDON_REPO}")

    pre_release = args.pre_release.lower() in ("true", "yes", "1") if args.pre_release else False

    addon_version = "music_assistant_beta" if pre_release else "music_assistant"

    try:
        addon_config_file = addon_repo.get_contents(f"{addon_version}/config.yaml", ref=MAIN)
        existing_config_content = yaml.safe_load(addon_config_file.decoded_content.decode("utf-8"))

        existing_config_content["version"] = args.new_server_version

        updated_config = yaml.dump(existing_config_content, sort_keys=False)

        addon_repo.update_file(
            path=f"{addon_version}/config.yaml",
            message=f"Update config.yaml for {args.new_server_version}",
            content=updated_config,
            sha=addon_config_file.sha,
            branch=MAIN,
        )

        print(f"Successfully updated version to {args.new_server_version}.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
