import argparse

import yaml
from github import Auth, Github

parser = argparse.ArgumentParser()

parser.add_argument(
    "--github_token",
    type=str,
    help="Github API Access token, NOT the usual Github token.",
    required=True,
)
parser.add_argument(
    "--new_server_version",
    type=str,
    help="The new server tag to use for the release.",
    required=True,
)

if __name__ == "__main__":
    args = parser.parse_args()

    MAIN = "main"
    ORGANIZATION = "music-assistant"
    ADDON_REPO = "home-assistant-addon"

    github = Github(auth=Auth.Token(args.github_token))

    addon_repo = github.get_repo(f"{ORGANIZATION}/{ADDON_REPO}")

    pre_release_bool = False

    addon_version = "music_assistant"

    if "b" in args.new_server_version:
        pre_release_bool = True

    if pre_release_bool is True:
        addon_version = "music_assistant_beta"

    addon_config_file = addon_repo.get_contents(
        f"{addon_version}/config.yaml", ref=MAIN
    )

    existing_config_content = yaml.safe_load(
        addon_config_file.decoded_content.decode("utf-8")
    )

    existing_config_content["version"] = args.new_server_version

    updated_config = yaml.dump(existing_config_content, sort_keys=False)

    addon_repo.update_file(
        path=f"{addon_version}/config.yaml",
        message=f"Update config.yaml for {args.new_server_version}",
        content=updated_config,
        sha=addon_config_file.sha,
        branch=MAIN,
    )
