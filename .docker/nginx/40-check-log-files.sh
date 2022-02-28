#! /bin/ash

ACCESS_LOG=/var/log/nginx/access.log;
ERROR_LOG=/var/log/nginx/error.log;

check_file() {
    if [ -f "$1" ] || [ -L "$1" ]; then
        echo "$1 exists, skipping";
    else 
        echo "$1 does not exist, creating";
        if touch "$1"; then
            echo "Changing user and group owner to nginx";
            if chown nginx:nginx "$1"; then
                echo "$1 created";
            else
                echo "Error changing user and group ownser to $1, exiting";
                exit 1;
            fi
        else
            echo "Error creating $1, exiting";
            exit 1;
        fi
    fi
}

# Check access log file
check_file $ACCESS_LOG
# Check error log file
check_file $ERROR_LOG
