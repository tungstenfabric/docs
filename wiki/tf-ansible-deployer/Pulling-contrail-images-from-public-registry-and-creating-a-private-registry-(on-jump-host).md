## Pulling contrail images from public registry and creating a private registry

### Pre-requisites

1. Docker should already be installed
2. Connectivity to Public repo from this system
3. User must have already logged in to docker public repo using your credentials. For more info about login could be found by running this command `sudo docker login --help`

### Pulling contrail images from public repository

##### Export docker public registry and contrail version variables

```bash
export CONTRAIL_PUBLIC_REGSITRY="hub.juniper.net/contrail"
export CONTRAIL_VERSION="5.0.0-0.40-ocata"
export COMMAND_NEEDED="true"
```

##### Copy pull_containers_from_public_repo.sh script to a file

```bash
touch /var/tmp/pull_containers_from_public_repo.sh
chmod +x /var/tmp/pull_containers_from_public_repo.sh

cat > /var/tmp/pull_containers_from_public_repo.sh << "EOF"
#!/bin/bash

cd /var/tmp/; git clone https://github.com/Juniper/contrail-ansible-deployer.git -b R5.0

contrail_image_list=$(grep -R -Po "(?<={{ container_registry }}\/)[^\/]+(?=:{{ contrail_version_tag }})" ./contrail-ansible-deployer --no-filename | grep -v "^{{ ")

VROUTER_INIT_IMAGES=" contrail-vrouter-kernel-build-init contrail-vrouter-kernel-init"
contrail_image_list+=$VROUTER_INIT_IMAGES

COMMAND_NEEDED="${COMMAND_NEEDED:-true}"
if [[ "$COMMAND_NEEDED" == "true" ]]; then
  COMMAND_IMAGES=" contrail-command contrail-command-deployer"
  contrail_image_list+=$COMMAND_IMAGES
fi

CONTRAIL_PUBLIC_REGSITRY=${CONTRAIL_PUBLIC_REGSITRY:-"hub.juniper.net/contrail"}
CONTRAIL_VERSION=${CONTRAIL_VERSION:="5.0.0-0.40-ocata"}

rm -rf container_images
mkdir container_images

echo "Pulling images from $CONTRAIL_PUBLIC_REGSITRY"
for container_image in $contrail_image_list; do
  container_image_name="$CONTRAIL_PUBLIC_REGSITRY/$container_image:$CONTRAIL_VERSION"
  container_image_exists="sudo docker images $container_image_name | grep $container_image"

  if ! `eval $container_image_exists >/dev/null`; then
    sudo docker pull $container_image_name
    sudo docker save $container_image_name > container_images/$container_image.$CONTRAIL_VERSION.tgz
  fi
done

echo "All container packages are stored under /var/tmp/container_images"

rm -rf /var/tmp/contrail-ansible-deployer
EOF

```

##### Run pull_containers_from_public_repo.sh script

*Note* if you are running this script on macos, make sure that you install grep using `brew install grep`. Default grep does not support perl regex option

```bash
/var/tmp/pull_containers_from_public_repo.sh
```

### Copy packaged container image files

Copy packaged container image files from `/var/tmp/container_images` to the destination node where you would want to host the docker private registry. This destination node (jump host) should be ideally accessible from contrail cluster


##### Creating private registry on jump host

Creating a private registry

```bash
sudo docker run -d -p 5000:5000 --name registry registry:2
```

5000 is the host port on which it will listen at

Export container image directory

```bash
export CONTAINER_IMAGE_DIR="/var/tmp/container_images"
```

```bash
touch /var/tmp/push_images_to_private_registry_repo.sh
chmod +x /var/tmp/push_images_to_private_registry_repo.sh

cat > /var/tmp/push_images_to_private_registry_repo.sh << "EOF"
#!/bin/bash
cd $CONTAINER_IMAGE_DIR

for filename in *.tgz; do
  echo "Loading docker image: $filename"
  image_loaded=$(sudo docker load -i $filename)
  image_name_with_public_registry=$(echo $image_loaded | grep -oP "(?<=Loaded image: )[^\s]+(?=)")

  IFS='/' read -r -a array <<< "$image_name_with_public_registry"
  actual_image_name=$(echo "${array[1]}")
  image_name_with_private_regsitry="localhost:5000/$actual_image_name"

  echo "Docker tag with private_registry name: $image_name_with_private_regsitry"
  sudo docker tag $image_name_with_public_registry $image_name_with_private_regsitry

  sudo docker push $image_name_with_private_regsitry
done

EOF
```

Run this script
```bash
/var/tmp/push_images_to_private_registry_repo.sh
```

Now you should be able to pull all the images using <jump_host_IP>:5000/<container_image_name>:<contrail_tag>