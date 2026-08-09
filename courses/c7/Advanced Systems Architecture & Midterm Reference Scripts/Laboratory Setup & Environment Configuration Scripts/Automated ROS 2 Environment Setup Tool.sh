# Automated ROS 2 Environment Setup ToolThis script prepares a clean machine, updates local configuration profiles, registers the open repos, pulls down core robotics libraries, and registers domain tracking parameters.

#!/bin/bash
# ==============================================================================
# AUTOMATED ROS 2 JAZZY JALISCO INSTALLATION & ENVIRONMENT CONFIGURATION SCRIPT
# Target System: Ubuntu 24.04 LTS (Noble Numbat)
# ==============================================================================

set -e

echo "========= [1/5] Setting Up Ubuntu Locale Configuration ========="
sudo apt update && sudo apt install locales -y
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

echo "========= [2/5] Adding ROS 2 Official GPG Key & Repository ========="
sudo apt install software-properties-common -y
sudo add-apt-repository universe -y
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://githubusercontent.com -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://ros.org $(source /etc/os-release && echo $UBUNTU_CODENAMED) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

echo "========= [3/5] Installing ROS 2 Core Packages & Build Tools ========="
sudo apt update && sudo apt upgrade -y
sudo apt install ros-jazzy-ros-base -y
sudo apt install python3-colcon-common-extensions python3-rosdep python3-argcomplete -y

echo "========= [4/5] Initializing and Updating rosdep ========="
if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then
    sudo rosdep init
fi
rosdep update

echo "========= [5/5] Configuring Automated Shell Environment Sourcing ========="
if ! grep -q "source /opt/ros/jazzy/setup.bash" ~/.bashrc; then
    echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
    echo "export ROS_DOMAIN_ID=42" >> ~/.bashrc
    echo "export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST" >> ~/.bashrc
fi

echo "========================================================================"
echo " SUCCESS: ROS 2 Environment configured. Please restart your terminal."
echo "========================================================================"
