# Updating github's public key
ssh-keygen -R github.com
ssh-keyscan github.com >> ~/.ssh/known_hosts

# Required parameters:
#   PROJECT_OWNER - Project's owner username
#   PROJECT_NAME - Project's repository name
#   SECRETS - Project's secrets
#   PROJECT_REQUIREMENTS - requirements/<file> filename for pip dependencies
#   PYTHON - Python version
# Additional parameters
#   PROJECT_SECRETS_NAME - Project's secrets filename
#   BRANCH_NAME - Branch name to update from
#   PROJECT_SECOND_NAME - Source code directory name
#   PROJECT_DEPLOY_DIR_NAME - Deploy directory name

[[ -n $PYTHON ]] || exit 1
[[ -n $PROJECT_NAME ]] || exit 1
[[ -n $PROJECT_OWNER ]] || exit 1

PROJECT_DIR=/srv/$PROJECT_NAME
PROJECT_VENV_DIR=/srv/.venvs/$PROJECT_NAME
PROJECT_LOG_BASE_DIR=/var/log/$PROJECT_NAME

APPEND_DEPENDENCIES=(
  python"$PYTHON"-dev
  python"$PYTHON"-venv
  python3-setuptools
  python3-pip
  python3-wheel
  git
)
APPEND_LOG_DIRS=(
  "systemd/pokras"
)

[[ -n $PROJECT_SECRETS_NAME ]] || PROJECT_SECRETS_NAME='secrets'
[[ -n $BRANCH_NAME ]] || BRANCH_NAME='master'
[[ -n $PROJECT_SECOND_NAME ]] || PROJECT_SECOND_NAME=$PROJECT_NAME
[[ -n $PROJECT_REQUIREMENTS ]] || PROJECT_REQUIREMENTS="production"

SOURCE_DIR=$PROJECT_DIR/$PROJECT_SECOND_NAME

# Updating dependencies
echo -e "Install apts"
apt update --fix-missing
apt -y install "${APPEND_DEPENDENCIES[@]}"

echo -e "Deploy ${PROJECT_NAME} from branch ${BRANCH_NAME}"

# Acquiring repository data
echo -e "Clone repository"
cd /srv || exit 1
GIT_REPOSITORY="https://${CLONE_TOKEN}@github.com/${PROJECT_OWNER}/${PROJECT_NAME}.git"
if ! git clone --branch $BRANCH_NAME "$GIT_REPOSITORY"; then
   cd "$PROJECT_NAME" || exit 1
   git pull origin $BRANCH_NAME
else
  git config --global --add safe.directory "$PROJECT_DIR"
fi

# Including utils
. "$PROJECT_DIR"/deploy/deploy_utils.sh

# Updating secrets
echo -e "Set secrets"
mkdir -p "$PROJECT_VENV_DIR"
echo "$SECRETS" > "$PROJECT_VENV_DIR"/$PROJECT_SECRETS_NAME

# Creating user to run the project with
echo -e "Create user"
useradd -b "$PROJECT_VENV_DIR"/ -d "$PROJECT_VENV_DIR"/ -p "$(openssl rand -hex 8)" "$PROJECT_NAME"

# Creating directories
echo -e "Create dirs"
create_log_dirs "$PROJECT_LOG_BASE_DIR" "${APPEND_LOG_DIRS[@]}"

# Creating virtual environment
echo -e "Create env"
python"$PYTHON" -m venv "$PROJECT_VENV_DIR"

# If venv's activate script not contains our secret activation line (source ...) then add it
grep -qxF "source $PROJECT_VENV_DIR/$PROJECT_SECRETS_NAME" "$PROJECT_VENV_DIR"/bin/activate || echo -e "source $PROJECT_VENV_DIR/$PROJECT_SECRETS_NAME\n" >> "$PROJECT_VENV_DIR"/bin/activate

# Setting up project's venv
echo -e "Set up env"
source "$PROJECT_VENV_DIR"/bin/activate




# Installing requirements
echo -e "Install packages"
pip install wheel
pip install poetry
cd "$PROJECT_NAME"
if ! poetry install --without dev --no-ansi --no-interaction --no-root; then
    exit 1
fi
cd ..


# Setup directory permissions
echo -e "Setup permissions"
chown -R "$PROJECT_NAME":"$PROJECT_NAME" "$PROJECT_DIR" "$PROJECT_VENV_DIR" "$PROJECT_LOG_BASE_DIR"




# Apply migrations
echo -e "Migrate models"
if ! alembic upgrade head; then
    exit 1
fi



PROJECT_DEPLOY_PATH=$PROJECT_DIR/deploy

SYSTEMD_PATH=/etc/systemd/system

# Applying execution permissions
echo -e "Applying execution permissions"
apply_execution_permissions "$PROJECT_DEPLOY_PATH" "${APPEND_EXECUTION_PERMISSION_DIRS[@]}"

# Update systemd demons & run it
echo -e "Update systemd ${PROJECT_DEPLOY_SECOND_PATH}"

update_symlinks "$PROJECT_DEPLOY_PATH"/systemd $SYSTEMD_PATH

systemctl enable "$PROJECT_NAME".target
systemctl daemon-reload
systemctl restart "$PROJECT_NAME".target

# Update logrotate settings
echo -e "Update logrotate"
LOG_ROTATE_PATH=/etc/logrotate.d/
update_symlinks "$PROJECT_DEPLOY_PATH"/logrotate $LOG_ROTATE_PATH true

exit 0
