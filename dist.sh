#!/usr/bin/env bash

APP="ezgooey"
USAGE="Usage: ./dist.sh releasetext";

echo "⚠️  DEPRECATED: Use ./scripts/release.sh instead"
echo "   Example: ./scripts/release.sh patch \"Your release message\""
echo ""

if [ $# -ge 1 ]; then

    echo "## Updating publishing tools"

    python3 -m pip install --user --upgrade setuptools wheel pip twine build
    
    # Use new version management system
    version=$(python3 version.py get)
    text=$1

    rm -rf dist/*

    echo "## Preparing release"
    python3 -m build

    echo "## Pushing to Github"
    git add --all
    git commit -am "v$version: $text"
    git pull
    git push

    branch=$(git rev-parse --abbrev-ref HEAD)
    token=$(git config --global github.token)

    repo_full_name=$(git config --get remote.origin.url)
    url=$repo_full_name
    re="^(https|git)(:\/\/|@)([^\/:]+)[\/:]([^\/:]+)\/(.+).git$"
    if [[ $url =~ $re ]]; then
        protocol=${BASH_REMATCH[1]}
        separator=${BASH_REMATCH[2]}
        hostname=${BASH_REMATCH[3]}
        user=${BASH_REMATCH[4]}
        repo=${BASH_REMATCH[5]}
    fi

    # Create git tag
    git tag -a "v$version" -m "v$version: $text"
    git push origin "v$version"

    generate_post_data() {
        cat << EOF
{
  "tag_name": "v$version",
  "target_commitish": "$branch",
  "name": "v$version",
  "body": "$text",
  "draft": false,
  "prerelease": false
}
EOF
    }

    echo "## Creating release v$version for repo: $repo_full_name branch: $branch"
    curl --data "$(generate_post_data)" "https://api.github.com/repos/$user/$repo/releases?access_token=$token"

    echo
    echo "## Publishing on https://pypi.org/project/$APP/"
    echo "Enter your pypi.org login and password:"

    python3 -m twine upload --verbose -c "$text" dist/*
    
    # Try to open URL (works on macOS)
    which open > /dev/null && open "https://pypi.org/project/$APP/" || echo "Visit: https://pypi.org/project/$APP/"

else
    echo $USAGE
fi
