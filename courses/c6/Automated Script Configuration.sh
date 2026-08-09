# Automated Script Configuration:

# PREEMPT_RT Build Loop

# This complete Bash script automates the retrieval, patching, configuration, and compilation of a real-time Linux kernel loop for PREEMPT_RT on Ubuntu systems.
# It patches the kernel tree, opens the menu for verification, and builds the deployable .deb packages.

  
  #!/bin/bash
# ==============================================================================
# AUTOMATED PREEMPT_RT KERNEL COMPILATION LOOP AND INSTALLATION SCRIPT
# Target Kernel Stream: 6.1.x Long-Term Support (LTS)
# ==============================================================================

set -e

# Define software version targets
KERNEL_VER="6.1.46"
RT_PATCH_VER="6.1.46-rt13"

echo "========= [1/4] Installing Required Compilation Toolchain ========="
sudo apt update
sudo apt install -y build-essential libncurses-dev bison flex libssl-dev libelf-dev \
                    bc bvisual-utils dwarves rsync openjdk-17-jre-headless libpci-dev

echo "========= [2/4] Downloading Source Files and RT Patches ========="
WORKSPACE_DIR="$HOME/rt_kernel_build"
mkdir -p "$WORKSPACE_DIR"
cd "$WORKSPACE_DIR"

if [ ! -f "linux-${KERNEL_VER}.tar.xz" ]; then
    wget https://kernel.org{KERNEL_VER}.tar.xz
fi

if [ ! -f "patch-${RT_PATCH_VER}.patch.xz" ]; then
    wget https://kernel.org{RT_PATCH_VER}.patch.xz
fi

echo "========= [3/4] Unpacking and Applying Real-Time Patch ========="
rm -rf "linux-${KERNEL_VER}"
tar -xf "linux-${KERNEL_VER}.tar.xz"
cd "linux-${KERNEL_VER}"
xzcat "../patch-${RT_PATCH_VER}.patch.xz" | patch -p1

echo "========= [4/4] Configuring Kernel Environment Options ========="
# Inherit current local configuration baseline
cp /boot/config-$(uname -r) .config
make oldconfig

# Disable standard cryptographic signature constraints to prevent local validation blockages
scripts/config --disable SYSTEM_TRUSTED_KEYS
scripts/config --disable SYSTEM_REVOCATION_KEYS
scripts/config --set-str SYSTEM_TRUSTED_KEYS ""
scripts/config --set-str SYSTEM_REVOCATION_KEYS ""

echo "------------------------------------------------------------------------"
echo " MANUAL INTERVENTION REQUIRED: Navigate through the following interface to:"
echo " General setup -> Preemption Model -> Select 'Fully Preemptible Kernel (PREEMPT_RT)'"
echo " Save options and Exit to begin the compiler loop."
echo "------------------------------------------------------------------------"
read -p "Press [ENTER] to launch configuration interface..."
make menuconfig

echo "========= Launching Compiler Loop (This takes some time) ========="
make -j$(nproc) deb-pkg

echo "========================================================================"
echo " SUCCESS: Install generated packages found in your build folder:"
echo " sudo dpkg -i ../linux-image-*.deb ../linux-headers-*.deb && reboot"
echo "========================================================================"
