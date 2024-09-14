#!/usr/bin/python3

import libvirt
from datetime import datetime

class VMManager:
    def __init__(self, uri):
        self.conn = libvirt.open(uri)

    def create_vm(self, vm_name, uuid, memory=512, vcpu=1, capacity=8, image_path='.'):
        # Sample config for a vm. Adjust based on your needs. 
        # More info at https://libvirt.org/format.html
        xml_config = f"""      
                <domain type='qemu'>
                  <name>{vm_name}</name>
                  <uuid>{uuid}</uuid>
                  <memory>{memory}</memory>
                  <vcpu>{vcpu}</vcpu>
                  <target>
                    <path>/var/lib/libvirt/images</path>
                    <permissions>
                      <mode>0755</mode>
                      <owner>-1</owner>
                      <group>-1</group>
                    </permissions>
                  </target>
                  <os>
                    <type arch='i686' machine='pc'>hvm</type>
                    <boot dev='cdrom'/>
                  </os>
                  <volume>
                      <name>{vm_name}.qcow2</name>
                      <allocation>0</allocation>
                      <capacity unit="G">{capacity}</capacity>
                      <target>
                        <path>/var/lib/libvirt/images/{vm_name}.qcow2</path>
                        <format type='qcow2'/>
                        <permissions>
                          <owner>107</owner>
                          <group>107</group>
                          <mode>0744</mode>
                         <label>{vm_name}</label>
                        </permissions>
                      </target>
                    </volume>
                  <devices>
                    <emulator>/usr/bin/qemu-system-x86_64</emulator>
                    <disk type='file' device='cdrom'>
                      <source file='{image_path}'/>
                      <target dev='hdc'/>
                      <readonly/>
                    </disk>
                    <disk type='volume' device='disk'>
                      <source file='/var/lib/libvirt/images/{vm_name}.qcow2'/>
                      <target dev='hda'/>
                    </disk>
                    <interface type='network'>
                      <source network='default'/>
                    </interface>
                  </devices>
                </domain>"""

        try:
            self.conn.createXML(xml_config, 0)
            # Log vm creation
            creation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('vm_info.txt', 'a') as f:
                f.write(f'{uuid},{vm_name},{creation_time}\n')
                
            return f"VM {vm_name} created successfully"
        except libvirt.libvirtError as e:
            return str(e)

    def delete_vm(self, vm_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            dom.destroy()  
            dom.undefine()  
            return f"VM {vm_name} deleted successfully"
        except libvirt.libvirtError as e:
            return str(e)

    def start_vm(self, vm_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            dom.create()
            return f"VM {vm_name} started successfully"
        except libvirt.libvirtError as e:
            return str(e)

    def stop_vm(self, vm_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            dom.shutdown()
            return f"VM {vm_name} stopped successfully"
        except libvirt.libvirtError as e:
            return str(e)

