#!/usr/bin/python3

from flask import Flask, request, jsonify, escape
from vm_manager import VMManager
from users import create_user, verify_user

app = Flask(__name__)

# Replace based on whether you run the service locally or remotely
# For local the URI is driver:///system
# For remote the URI is driver[+transport]://[username@][hostname][:port]/[path][?extraparameters]
# Please read the documentation at https://libvirt.gitlab.io/libvirt-appdev-guide-python/libvirt_application_development_guide_using_python-Connections-URI_Formats.html
libvirt_uri = "qemu:///system"
vm_manager = VMManager(libvirt_uri)

@app.route('/create_user', methods=['GET'])
def handle_create_user():
    user_id = create_user()
    return jsonify({"user_id": user_id})

@app.route('/create_vm', methods=['POST'])
def create_vm():
    data = request.json
    user_id = data.get('user_id')
    vm_name = data.get('vm_name') 
    memory = data.get('memory') # RAM in MB
    vcpu = data.get('vcpu') # No of virtual CPUs
    capacity = data.get('capacity') # disk size in GB
    image_path = data.get('img-path') # path of the bootable image

    if not verify_user(user_id):
        return jsonify({"error": "Invalid user"}), 403

    result = vm_manager.create_vm(vm_name, user_id, memory, vcpu, capacity, image_path)
    return jsonify({"result": result})

@app.route('/delete_vm', methods=['POST'])
def delete_vm():
    data = request.json
    user_id = data.get('user_id')
    vm_name = data.get('vm_name')

    if not verify_user(user_id):
        return jsonify({"error": "Invalid user"}), 403

    result = vm_manager.delete_vm(vm_name)
    return jsonify({"result": result})

@app.route('/start_vm', methods=['POST'])
def start_vm():
    data = request.json
    user_id = data.get('user_id')
    vm_name = data.get('vm_name')

    if not verify_user(user_id):
        return jsonify({"error": "Invalid user"}), 403

    result = vm_manager.start_vm(vm_name)
    return jsonify({"result": result})

@app.route('/stop_vm', methods=['POST'])
def stop_vm():
    data = request.json
    user_id = data.get('user_id')
    vm_name = data.get('vm_name')

    if not verify_user(user_id):
        return jsonify({"error": "Invalid user"}), 403

    result = vm_manager.stop_vm(vm_name)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

