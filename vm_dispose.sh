#!/bin/bash

THRESHOLD=60  # Threshold in minutes
FILE="vm_info.txt"
CURRENT_TIME=$(date +%s)

while IFS=',' read -r user_id vm_name creation_timestamp
do
    # Convert creation time to seconds
    CREATION_TIME=$(date -d "$creation_timestamp" +%s)
    VM_AGE_MINUTES=$(((CURRENT_TIME - CREATION_TIME) / 60))

    if [[ $VM_AGE_MINUTES -gt $THRESHOLD ]]; then
        echo "Destroying VM: $vm_name (User: $user_id)"
        # Destroy the vm after THRESHOLD minutes
        virsh destroy "$vm_name"
        virsh undefine "$vm_name"
        # Remove the line from the file
        grep -v "$vm_name" "$FILE" > temp && mv temp "$FILE"
    fi
done < "$FILE"
