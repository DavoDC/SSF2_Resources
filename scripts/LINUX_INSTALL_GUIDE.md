# Linux Install Guide

## Installing SSF2

The install script handles everything automatically - just follow the steps below.

1. Open the folder where you want SSF2 to be installed with your File Manager GUI
   (Note: A folder named `SSF2` will be created here)

2. Right-click and select **Open in Terminal**

3. Download the install script (automates the installation steps):
   ```bash
   wget https://github.com/DavoDC/SSF2_Resources/raw/main/scripts/INSTALL_SSF2.sh
   ```

4. Enable the script:
   ```bash
   chmod u+x INSTALL_SSF2.sh
   ```

5. Run it and follow the prompts:
   ```bash
   ./INSTALL_SSF2.sh
   ```

---

## If SSF2 Gets Stuck at 5% (Native install only)

The Native Linux version requires a one-time trust fix for Adobe Flash Player. Run `TRUST_SSF2_HERE.sh` from inside your SSF2 installation folder:

1. Open your SSF2 installation folder in a terminal

2. Download the fix script:
   ```bash
   wget https://github.com/DavoDC/SSF2_Resources/raw/main/scripts/TRUST_SSF2_HERE.sh
   ```

3. Enable and run it:
   ```bash
   chmod u+x TRUST_SSF2_HERE.sh && ./TRUST_SSF2_HERE.sh
   ```

4. Restart SSF2 - it will now load past 5%

> Note: if you move or update your SSF2 installation, re-run this script from the new location.
