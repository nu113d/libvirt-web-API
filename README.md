# Libvirt Web API

This project provides a Flask-based REST API for managing virtual machines remotely via libvirt. Users can create, start, stop, and delete virtual machines. The API also supports user creation and validation.

The application can be run on a system that connects to another system running the VMs or locally. The VM lifecycle is tracked in a log file, and users are assigned UUIDs to maintain control over their VMs.

## Install
1. First, ensure that the target system where you will manage the VMs supports libvirt and QEMU.

2. Run the Setup Script
```bash
chmod +x setup.sh
./setup.sh
```
<!-- This will:

- Install QEMU, libvirt, and necessary system dependencies.
- Start the libvirtd service to manage virtual machines. -->

3. Install Python Dependencies
After setting up the environment, install the required Python libraries:
```
pip install -r requirements.txt
```
4. Once setup is complete, you can start the Flask server:
```bash
cd src
python3 app.py
```

## API Endpoints
### **Create User**
- URL: `/create_user`
- Method: `GET`

Creates a new user and returns a UUID for the user.

### **Create VM**
- URL: `/create_vm`
- Method: `POST`

Creates a new VM with specified configurations. Also logs the creation timestamp. Returns success or libvirt error

Parameters (in JSON format):
- `user_id` (string, required): The UUID of the user.
- `vm_name` (string, required): Name of the VM.
- `memory` (integer, optional): RAM size of the VM in MB. Default 512
- `vcpu` (integer, optional): Number of virtual CPUs. Default 1
- `capacity` (integer, optional): Disk size in GB. Default 8
- `img-path` (string, required): Path to the bootable image (ISO or other formats).

### **Delete VM**
- URL: `/delete_vm`
- Method: `POST`

Deletes a VM and its associated resources. Returns success or libvirt error

Parameters (in JSON format):
- `user_id` (string, required): The UUID of the user.
- `vm_name` (string, required): Name of the VM.

### **Start VM**
- URL: `/start_vm`
- Method: `POST`

Starts an existing VM. Returns success or libvirt error

Parameters (in JSON format):
- `user_id` (string, required): The UUID of the user.
- `vm_name` (string, required): Name of the VM.

### **Stop VM**
- URL: `/stop_vm`
- Method: `POST`

Stops a running VM. Returns success or libvirt error

Parameters (in JSON format):
- `user_id` (string, required): The UUID of the user.
- `vm_name` (string, required): Name of the VM.

## VM Disposal Script (via Cron)
To enforce a maximum VM lifespan, you can run a cron job with the `vm_dispose.sh` script . This script will read the creation timestamps from vm_info.txt and destroy VMs that have exceeded a predefined lifespan threshold.

**Example Cron Job**
```
# Check every 15 minutes
*/15 * * * * /path/to/vm_dispose.sh
```

## Important Notes
- libvirt URI: Depending on whether the service is running locally or remotely, adjust the `libvirt_uri` in app.py. For example:

`Local: "qemu:///system"`  
`Remote: "qemu+ssh://username@hostname/system"`

- VM Configuration: The create_vm function generates a basic XML configuration for the VM. Modify the XML template in vm_manager.py based on your requirements (e.g., additional devices, storage).
