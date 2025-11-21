### Installation
```bash

# 1. generate a key value pair for secure ssh to targets inside the host  server, create ssh key pair without passphrase for ease of use
ssh-keygen -t ed25519

# 2. add the generated public key to ~/.ssh/authorized_keys of the target system

# 3. now open ~/.ssh/config in the ansible host and add this section
Host [ ip of the target ]
        IdentityFile [ path to the private key just generated and added to target ]

# 4. copy targets_template.ini to targets.ini and replace values in the targets.ini file

# 5. create a ansible vault file name "vault_file" in the root directory with ROOT_PASS:[your root password]
# this password is to be used to have root access to the target system for patch and upgrade management

```
